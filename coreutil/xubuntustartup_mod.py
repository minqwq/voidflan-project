import time
import curses
import colorama

def center_text(stdscr, y, text):
    """在指定行 y 居中显示文本"""
    height, width = stdscr.getmaxyx()
    x = max(0, (width - len(text)) // 2)
    try:
        stdscr.addstr(y, x, text)
    except curses.error:
        pass  # 防止窗口太小导致报错

def animate_dots(stdscr):
    showdotloop = 0
    curses.curs_set(0)  # 隐藏光标
    height, width = stdscr.getmaxyx()
    
    # 居中显示 "Xubuntu 25.04"
    # center_text(stdscr, height // 2 - 1, "Xubuntu 25.04")
    center_text(stdscr, height // 2 - 4, "Codename \"Hata no Kokoro\"")
    center_text(stdscr, height // 2 - 3, "VoidFlan Project II")
    center_text(stdscr, height // 2 - 2, "Beta 2 Sep. Release")
    
    # 计算四个点的起始位置（居中）
    dots_x = (width - 7) // 2  # 4个点 + 3个空格 = 7字符宽度
    
    # 在四个点下面加一行字
    center_text(stdscr, height // 2 + 2, "(C) Flandre Studio 2024--2026")
    center_text(stdscr, height // 2 + 3, "(C) 0x1c Studio 2022--2023")
    
    try:
        while showdotloop < 2:
            # 四个点依次出现（从左到右）
            for i in range(4):
                stdscr.addstr(height // 2, dots_x + i * 2, ".")
                stdscr.refresh()
                time.sleep(0.5)
            
            # 短暂停留
            # time.sleep(0.5)
            
            # 四个点依次消失（从左到右）
            for i in range(4):
                stdscr.addstr(height // 2, dots_x + i * 2, " ")
                stdscr.refresh()
                time.sleep(0.5)
            
            # 短暂停留
            # time.sleep(0.3)
            showdotloop += 1
    
    except KeyboardInterrupt:
        pass  # 按 Ctrl+C 退出

# if __name__ == "__main__":
curses.wrapper(animate_dots)
