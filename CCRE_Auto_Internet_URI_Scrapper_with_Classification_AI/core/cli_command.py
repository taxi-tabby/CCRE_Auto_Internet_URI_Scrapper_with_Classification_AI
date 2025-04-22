from typing import Callable, List, Optional, Union
import requests

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.console import CommandHandler
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.migrate import RunMigrationsProtocol
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models.roots import Roots
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.pika_rabbitmq import PikaRabbitMQ
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.sqlalchemy import SQLAlchemyConnection
import platform
from datetime import datetime
import socket
import uuid
import hashlib

import CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.rds as rds
import CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.local as local_rds
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.udp_client import UDPClient
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.udp_server import UDPServer
class CLICommand:
    def __init__(self, 
                 console_handler: CommandHandler, 
                 roots: List['Roots'], 
                 mq_sessions: List['PikaRabbitMQ'], 
                 db_session: 'SQLAlchemyConnection', 
                 local_session: 'SQLAlchemyConnection',
                 master_socket: 'UDPServer',
                 slave_socket: 'UDPClient',
                 run_migrations: RunMigrationsProtocol):
        
        self.console_handler = console_handler
        self.roots = roots
        self.mq_sessions = mq_sessions
        self.db_session = db_session
        self.local_session = local_session
        self.master_socket = master_socket
        self.slave_socket = slave_socket
        self.run_migrations = run_migrations
        
        # Constants for profile keys as dictionary
        self.PROFILE_KEYS = {
            'GUILD_UNIQUE_ID': 'guild_unique_id',
            'GUILD_IS': 'guild_available',
            'GUILD_ADDRESS_OUTER_IP': 'guild_ip_address_in_string',
            'GUILD_ADDRESS_INNER_IP': 'guild_ip_address_out_string',
            'GUILD_ADDRESS_MAC': 'guild_mac_address_string',
            'GUILD_LAST_RG_AT': 'guild_last_registration_at',
            'GUILD_TOKEN': 'guild_token',
            'GUILD_MASTER_TOKEN': 'guild_master_token',
            'GUILD_MASTER_NODE_IS': 'guild_master_node_is',
            'GUILD_SLAVE_NODE_IS': 'guild_slave_node_is',
        }


    def empty(self):
        """
        Not available command.
        """
        return
    
    
    # def dev__migrate(self, db_type: str, action: str, message: Optional[str] = None, revision: Optional[str] = None):
    #     """
    #     [DEV] Run the migration command.
    #     """
    #     print = self.console_handler.print_formatted
        
    #     if db_type not in ['main', 'local']:
    #         print(f"Unknown database type: {db_type}", 'error')
    #         return
        
    #     if action not in ['upgrade', 'revision', 'downgrade']:
    #         print(f"Unknown action: {action}", 'error')
    #         return
        
    #     # Run the migration
    #     self.run_migrations(db_type, self.db_session.engine.url, action, message, revision)
        
    #     # Print success message
    #     print(f"Migration {action} for {db_type} database completed successfully.", 'success')
    
    
    
    def dev__master_node_stop(self):
        """
        [DEV] Stop the master node.
        """
        print = self.console_handler.print_formatted
        
        if self.master_socket is None:
            print('Master node not available.', 'error')
            return
        
        if self.master_socket.stop():
            print('Master node stopped successfully.', 'success')
            self.master_socket = None
        else:
            print('Failed to stop master node.', 'error')
    
    
    
    
    def be_a_master_node(self):
        """
        Start the master node.
        """
        print = self.console_handler.print_formatted
        
        
        def callback(socket: socket.socket, data: str, _RetAddress: tuple[str, int]):
            print(f"Received data: {data} from {_RetAddress}", 'info')
        
        def init_callback(success: bool, message: str, ip: str):
            print(f"Master node initialized: {message} / open is {success} / address is {ip}", 'info')
        
        self.master_socket.set_callback(callback)
        self.master_socket.set_init_callback(init_callback)


        # Keys
        key_guild_master_is = self.PROFILE_KEYS['GUILD_MASTER_NODE_IS']
        
        with self.local_session.get_db() as db:
            local_rds.save_local_profile(db, key_guild_master_is, '1')


        if self.master_socket.listen():
            if not self.master_socket.is_running():
                print('Master node not available.', 'error')
            else:
                print('Master node started successfully.', 'success')
        else:
            print('Failed to start master node.', 'error')
        
        
    
    
    def ping_to_slaves(self):
        """
        Ping the slaves to check their status. (작업 전)
        """
        
        if self.master_socket.is_running():
            self.master_socket.broadcast('ping')
            print('Ping sent to slaves.', 'info')
        else:
            print('Master node is not running.', 'error')
            
            
            
    def quit_master_node(self):
        """
        Stop the master node.
        """
        print = self.console_handler.print_formatted
        
        if self.master_socket is None:
            print('Master node not available.', 'error')
            return
        
        
        # Keys
        key_guild_master_is = self.PROFILE_KEYS['GUILD_MASTER_NODE_IS']
        
        with self.local_session.get_db() as db:
            local_rds.save_local_profile(db, key_guild_master_is, '0')
        
        
        if self.master_socket.stop():
            print('Master node stopped successfully.', 'success')
            self.master_socket = None
        else:
            print('Failed to stop master node.', 'error')
            
            
            
    #guild-join --ip 127.0.0.1 --port 12345 --token 000
    def guild_join(self, ip: str, port: str, token: str):
        """
        Join the guild with the given IP and port.
        """
        
        print = self.console_handler.print_formatted
        
        if self.slave_socket is None:
            print('Slave node not available.', 'error')
            return
        
        
        if self.slave_socket.is_running():
            print('Slave node already running.', 'error')
            return
        
        
        with self.local_session.get_db() as db:


            guild_is = local_rds.get_latest_local_profile(db, self.PROFILE_KEYS['GUILD_IS'])
            
            if guild_is is None or guild_is == '0':
                print('You are not registered in guild', 'error')
                return

            guild_master_node_is = local_rds.get_latest_local_profile(db, self.PROFILE_KEYS['GUILD_MASTER_NODE_IS'])
            
            if guild_master_node_is is not None and guild_master_node_is == '1':
                print('You are not allowed to be a slave. you are the master node. sir', 'error')
                return

        
        
        
        def callback(data: str, _RetAddress: tuple[str, int]):
            print(f"Received data: {data} from {_RetAddress}", 'info')
            
        def init_callback(success: bool, message: str, ip: str):
            print(f"Slave node initialized: {message} / open is {success} / address is {ip}", 'info')
        
        
        self.slave_socket.set_init_callback(init_callback)
        self.slave_socket.set_callback(callback)
        
        
        self.slave_socket.init_connection()
        # self.slave_socket.connect('127.0.0.1', 12345, 12346)
        self.slave_socket.connect(ip, int(port), 12346)
        
        
        if self.master_socket.is_running():
            if self.master_socket.add_to_whitelist(ip):
                print(f"{ip} added to whitelist.", 'info')
            
        
        
        if self.slave_socket.start_listening():
            if not self.slave_socket.is_running():
                print('Slave node not available.', 'error')
            else:
                self.slave_socket.send_message('hello master!')
                print('Slave node started successfully.', 'success')
        else:
            print('Failed to start slave node.', 'error')
        
        
        
        
        
        # if self.slave_socket.join(guild_ip, guild_port, guild_token):
        #     print('Joined the guild successfully.', 'success')
        # else:
        #     print('Failed to join the guild.', 'error')
    
    
    
    
    
    def motd(self):
        """
        print welcome message of the day.
        """
        
        print = self.console_handler.print_formatted
        
        banner = """
        ╔════════════════════════════════════════════════════════╗
        ║                                                        ║
        ║   CCRE Auto Internet URI Scrapper with Classification  ║
        ║                                                        ║
        ╚════════════════════════════════════════════════════════╝
        """
        
        self.console_handler.print_formatted(banner)
        print()
        print(f"System: {platform.system()} {platform.release()}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print('[This client stat]')
        with self.local_session.get_db() as db:
            def print_profile(message, key):
                # print(f'xxxxxxxxxxxxx: {db.in_transaction()}')
                value = local_rds.get_latest_local_profile(db, key)
                if value is not None:
                    print(f'{message}: {value}', 'info')

            # print_profile('guild activated', self.PROFILE_KEYS['GUILD_IS'])
            # print_profile('guild unique id', self.PROFILE_KEYS['GUILD_UNIQUE_ID'])
            # Print all profile keys
            for key_name, key_value in self.PROFILE_KEYS.items():
                print_profile(key_name, key_value)














    def guild_registration(self):
        """
        Register the guild with network information including IPs, MAC address, and registration timestamp.
        """
        
        print = self.console_handler.print_formatted
        
        # Get network information
        hostname = socket.gethostname()
        inner_ip = socket.gethostbyname(hostname)
        # Get external IP using a public IP service
        outer_ip = ""
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            if response.status_code == 200:
                outer_ip = response.text
            else:
                # Fallback to local IP detection
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                outer_ip = s.getsockname()[0]
                s.close()
        except Exception as e:
            print(f"Could not determine external IP: {e}")
            # Attempt fallback
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                outer_ip = s.getsockname()[0]
                s.close()
            except:
                pass
            pass
            
        # Get MAC address
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                        for elements in range(0, 8*6, 8)][::-1])
            
        # Current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Keys
        key_guild_is = self.PROFILE_KEYS['GUILD_IS']
        key_name = self.PROFILE_KEYS['GUILD_UNIQUE_ID']
        key_outer_ip = self.PROFILE_KEYS['GUILD_ADDRESS_OUTER_IP']
        key_inner_ip = self.PROFILE_KEYS['GUILD_ADDRESS_INNER_IP']
        key_mac = self.PROFILE_KEYS['GUILD_ADDRESS_MAC']
        key_last_reg = self.PROFILE_KEYS['GUILD_LAST_RG_AT']
        key_token = self.PROFILE_KEYS['GUILD_TOKEN']
        
        with self.local_session.get_db() as db:
            local_rds.save_local_profile(db, key_guild_is, '1')
            
            existing_name = local_rds.get_latest_local_profile(db, key_name)
            local_rds.save_local_profile(db, key_name, 'noname' if existing_name is None else existing_name)
            
            local_rds.save_local_profile(db, key_outer_ip, outer_ip)
            local_rds.save_local_profile(db, key_inner_ip, inner_ip)
            local_rds.save_local_profile(db, key_mac, mac)
            local_rds.save_local_profile(db, key_last_reg, timestamp)
            
            # Generate a unique token based on UUID v4 and network information

            # Create a UUID v4
            unique_uuid = str(uuid.uuid4())

            # Combine all components to make a unique string
            unique_components = f"{unique_uuid}:{inner_ip}:{outer_ip}:{timestamp}:{mac}"

            # Hash this string for a consistently formatted token
            token_hash = hashlib.sha512(unique_components.encode()).hexdigest()

            # Save the token
            print(f'xxx1 {db.in_transaction()}')
            local_rds.save_local_profile(db, key_token, token_hash)
            print(f'xxx2 {db.in_transaction()}')


            # Display saved values
            (lambda r: print(f'Guild is: {r}', 'info') if r is not None else None)(local_rds.get_latest_local_profile(db, key_guild_is))
            (lambda r: print(f'Alias name: {r}', 'info') if r is not None else None)(local_rds.get_latest_local_profile(db, key_name))
            (lambda r: print(f'External IP: {r}', 'info') if r is not None else None)(local_rds.get_latest_local_profile(db, key_outer_ip))
            (lambda r: print(f'Internal IP: {r}', 'info') if r is not None else None)(local_rds.get_latest_local_profile(db, key_inner_ip))
            (lambda r: print(f'MAC Address: {r}', 'info') if r is not None else None)(local_rds.get_latest_local_profile(db, key_mac))
            (lambda r: print(f'Registered at: {r}', 'info') if r is not None else None)(local_rds.get_latest_local_profile(db, key_last_reg))
            
            # Add display of token to the output
            (lambda r: print(f'Guild Token: {r}', 'success') if r is not None else None)(local_rds.get_latest_local_profile(db, key_token))
            
    
    
    
    
    
    
    
    
    
    
    
    def guild_unique_change(self, name: str):
        """
        Change the unique alias id.
        """
        
        print = self.console_handler.print_formatted
        
        key = self.PROFILE_KEYS['GUILD_UNIQUE_ID']
        r: str = ''
        with self.local_session.get_db() as db:
            local_rds.save_local_profile(db, key, name)
            
            response = local_rds.get_latest_local_profile(db, key)
            if response is not None:
                r = response
                
        print(f"Party alias name changed to: {r}", 'success', True) 
            
