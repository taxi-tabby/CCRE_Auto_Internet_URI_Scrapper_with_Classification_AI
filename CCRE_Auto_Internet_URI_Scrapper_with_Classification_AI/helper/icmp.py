import socket
import struct
import time
import select
import os


class ICMPHelper:
    ICMP_ECHO_REQUEST = 8
    ICMP_ECHO_REPLY = 0

    def __init__(self, timeout=1, packet_size=64):
        self.timeout = timeout
        self.packet_size = packet_size

    def checksum(self, source_string):
        """Calculate the checksum of the packet."""
        sum = 0
        count_to = (len(source_string) // 2) * 2
        count = 0

        while count < count_to:
            this_val = source_string[count + 1] * 256 + source_string[count]
            sum = sum + this_val
            sum = sum & 0xFFFFFFFF
            count = count + 2

        if count_to < len(source_string):
            sum = sum + source_string[len(source_string) - 1]
            sum = sum & 0xFFFFFFFF

        sum = (sum >> 16) + (sum & 0xFFFF)
        sum = sum + (sum >> 16)
        answer = ~sum
        answer = answer & 0xFFFF
        answer = answer >> 8 | (answer << 8 & 0xFF00)
        return answer

    def create_packet(self, id):
        """Create a new ICMP echo request packet."""
        header = struct.pack('bbHHh', self.ICMP_ECHO_REQUEST, 0, 0, id, 1)
        data = (192 - struct.calcsize('d')) * b'Q'
        data = struct.pack('d', time.time()) + data
        checksum = self.checksum(header + data)
        header = struct.pack('bbHHh', self.ICMP_ECHO_REQUEST, 0, checksum, id, 1)
        return header + data

    def send_ping(self, dest_addr):
        """Send an ICMP echo request to the specified destination."""
        try:
            dest_addr = socket.gethostbyname(dest_addr)
        except socket.gaierror as e:
            return f"Failed to resolve host: {e}"

        icmp = socket.getprotobyname("icmp")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except PermissionError as e:
            return "Permission denied: ICMP messages can only be sent by processes running as root."

        packet_id = os.getpid() & 0xFFFF
        packet = self.create_packet(packet_id)

        try:
            sock.sendto(packet, (dest_addr, 1))
            start_time = time.time()
            while True:
                ready = select.select([sock], [], [], self.timeout)
                if ready[0] == []:  # Timeout
                    return "Request timed out."

                time_received = time.time()
                recv_packet, addr = sock.recvfrom(1024)
                icmp_header = recv_packet[20:28]
                type, code, checksum, p_id, sequence = struct.unpack('bbHHh', icmp_header)

                if p_id == packet_id and type == self.ICMP_ECHO_REPLY:
                    return f"Reply from {addr[0]}: time={(time_received - start_time) * 1000:.2f}ms"
        finally:
            sock.close()

