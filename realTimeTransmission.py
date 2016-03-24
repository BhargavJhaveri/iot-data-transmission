import curses
import sys
import socket

#screen initialization
stdscr = curses.initscr()
curses.noecho()

scr_size = stdscr.getmaxyx()
begin_x = 0
begin_y = 0
scr_height = scr_size[0]
scr_width = scr_size[1]
writableMaxX = scr_width - 1
writableMinX = 0
writableMaxY = scr_height-1
writableMinY = 1

win = curses.newwin(scr_height, scr_width, begin_y, begin_x)
title = "CURRENT TRANSMISSION MODE: TERMINAL"
stdscr.addstr(0, scr_width/2-len(title)/2,"CURRENT TRANSMISSION MODE: TERMINAL", curses.A_BOLD)
stdscr.move(writableMinY,writableMinX)
cursorLocation = (writableMinY,writableMinX)

#create TCP connection with RaspberryPi
TCP_IP = '10.139.61.61'
TCP_PORT = 5005
BUFFER_SIZE = 20

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))     
except:
    curses.endwin()
    e = sys.exc_info()[0]     
    print e
    sys.exit(1)

while 1:
    c = stdscr.getch()
    if c == 127: #if backspace character seen
        if cursorLocation[0] == writableMinY and cursorLocation[1] == writableMinX:
            cursorLocation = (cursorLocation[0], cursorLocation[1])
        elif cursorLocation[1] == writableMinX:
            cursorLocation = (cursorLocation[0]-1, writableMaxX)
        else:
            cursorLocation = (cursorLocation[0], cursorLocation[1]-1)
        stdscr.delch(cursorLocation[0], cursorLocation[1])
    else:
        stdscr.addstr(cursorLocation[0], cursorLocation[1], chr(c))
        if cursorLocation[1] == writableMaxX:
            cursorLocation = (cursorLocation[0]+1, writableMinX)
        else:
            cursorLocation = (cursorLocation[0], cursorLocation[1]+1)
    
    s.send(chr(c))	      

curses.endwin()
