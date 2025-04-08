#https://i.ytimg.com/vi/HbvjfRPFjyg/hqdefault.jpg

import sys
import os


# 테스트용 루트 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Source start line

import curses
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.console import CommandHandler
console: CommandHandler = CommandHandler()
curses.wrapper(lambda stdscr: console.start(stdscr))