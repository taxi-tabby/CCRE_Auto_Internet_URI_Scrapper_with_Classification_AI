import curses
import threading
import time


class CommandHandler:
    def __init__(self, max_output_lines=100):
        self.output_buffer = []  # 출력 버퍼 초기화
        self.max_output_lines = max_output_lines  # 최대 출력 개수 설정
        self.command_history = []  # 명령어 기록
        self.history_index = -1  # 명령어 히스토리 인덱스

    def refresh_output(self, stdscr):
        """
        출력 버퍼의 내용을 curses 화면에 갱신하는 함수
        """
        stdscr.clear()  # 화면 초기화
        y = 0  # 출력 라인 위치
        output_lines = len(self.output_buffer)  # 출력된 총 줄 수

        print(output_lines)

        # 출력은 화면 크기에서 입력 부분을 제외한 부분에 출력
        for line in self.output_buffer[-self.max_output_lines:]:
            if y < curses.LINES - 1:  # 입력란을 제외한 영역에만 출력
                # 화면 너비를 초과하지 않도록 텍스트 자르기
                if len(line) > curses.COLS:
                    line = line[:curses.COLS - 1]
                stdscr.addstr(y, 0, line)
                y += 1

        # 화면 갱신
        stdscr.refresh()

    def input_thread(self, stdscr):
        """
        사용자 입력을 처리하고, 화면을 갱신하는 함수
        """
        input_line = ''  # 사용자 입력 초기화
        input_pos = 0  # 입력 위치
        while True:
            try:
                # 화면에서 입력창 부분을 지운다.
                self.clear_input_field(stdscr)

                # 입력된 텍스트를 화면에 표시
                stdscr.addstr(curses.LINES - 1, 0, input_line)  # 입력된 텍스트 표시
                stdscr.refresh()

                key = stdscr.getch()  # 사용자가 입력한 문자
                if key == 10:  # Enter 키
                    if input_line:
                        self.handle_input(input_line)  # 입력된 명령어 처리
                        input_line = ''  # 명령어 처리 후 입력창 비우기
                elif key == 27:  # ESC 키 (프로그램 종료)
                    break
                elif key == curses.KEY_LEFT:  # 왼쪽 방향키
                    if input_pos > 0:
                        input_pos -= 1
                elif key == curses.KEY_RIGHT:  # 오른쪽 방향키
                    if input_pos < len(input_line):
                        input_pos += 1
                elif key == curses.KEY_UP:  # 위쪽 방향키 (이전 명령어)
                    if self.history_index > 0:
                        self.history_index -= 1
                        input_line = self.command_history[self.history_index]
                elif key == curses.KEY_DOWN:  # 아래쪽 방향키 (다음 명령어)
                    if self.history_index < len(self.command_history) - 1:
                        self.history_index += 1
                        input_line = self.command_history[self.history_index]
                elif isinstance(key, str):  # 한글 및 다른 문자는 모두 문자열로 입력됨
                    input_line += key  # 다른 키는 입력에 추가
                else:
                    input_line += chr(key)  # 다른 키는 입력에 추가

            except curses.error as e:
                # 예외 처리 (입력 위치나 화면 크기 문제로 발생한 예외 처리)
                pass

    def clear_input_field(self, stdscr):
        """
        입력 필드를 지우는 함수.
        이 함수는 화면의 하단 입력 필드를 공백으로 덮어씌워서 이전 텍스트를 지웁니다.
        """
        try:
            max_col = curses.COLS - 1  # 마지막 컬럼은 공백이 들어가야 해서 -1을 해줍니다.
            max_row = curses.LINES - 1  # 마지막 행은 입력 필드가 있으므로 이전 텍스트가 있을 수 있습니다.
            stdscr.addnstr(max_row, 0, ' ' * max_col, max_col)  # 마지막 줄을 공백으로 덮음
            stdscr.refresh()  # 화면 갱신
        except curses.error as e:
            # 예외 처리 (에러가 발생해도 계속 실행되도록)
            pass

    def handle_input(self, user_input):
        # 명령어 처리하는 로직 (간단히 출력)
        self.print_output(f"입력된 명령어: {user_input}")

    def print_output(self, *args):
        """
        print와 동일한 방식으로 출력 버퍼에 메시지를 추가
        *args로 받는 이유는 print와 동일한 파라미터로 처리하기 위해
        """
        output = " ".join(map(str, args))  # 입력받은 인자들을 문자열로 변환하여 합침
        self.output_buffer.append(output)  # 버퍼에 추가
        # 버퍼 크기가 최대 개수를 초과하면 가장 오래된 항목을 제거
        if len(self.output_buffer) > self.max_output_lines:
            self.output_buffer.pop(0)

    def start(self, stdscr):
        # 입력을 받는 스레드 실행
        threading.Thread(target=self.input_thread, args=(stdscr,), daemon=True).start()

        while True:
            # 출력 버퍼 내용 갱신
            self.refresh_output(stdscr)
            time.sleep(0.1)  # 화면 갱신 주기

