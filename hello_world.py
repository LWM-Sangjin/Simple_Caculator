import tkinter as tk
import math
from tkinter import simpledialog
import tkinter.font as tkfont

BG_COLOR = "#ffffff"  # 전체 배경색 (흰색)
BTN_COLOR = "#e0e0e0"  # 버튼 배경색 (연한 회색)
BTN_TEXT_COLOR = "#000000"  # 버튼 글씨색 (검은색)
ENTRY_BG = "#ffffff"  # 입력창 배경색 (흰색)
ENTRY_FG = "#000000"  # 입력창 글씨색 (검은색)

# 색상 변수들을 전역으로 관리
colors = {
    'bg': BG_COLOR,
    'btn': BTN_COLOR,
    'btn_text': BTN_TEXT_COLOR,
    'entry_bg': ENTRY_BG,
    'entry_fg': ENTRY_FG
}

def apply_colors():
    root.configure(bg=colors['bg'])
    entry.configure(bg=colors['entry_bg'], fg=colors['entry_fg'], insertbackground=colors['entry_fg'])
    for btn, text in zip(button_widgets, buttons):
        if text == "설정":
            btn.configure(bg="#bdbdbd", fg="#263238", activebackground="#eeeeee", activeforeground="#263238")
        else:
            btn.configure(bg=colors['btn'], fg=colors['btn_text'], activebackground="#bbdefb", activeforeground=colors['btn_text'])

def open_settings():
    settings = tk.Toplevel(root)
    settings.title("설정")
    settings.geometry("340x340")
    settings.configure(bg=colors['bg'])

    # 설정창 폰트는 고정
    set_font = tkfont.Font(family="Arial", size=13)
    label_fg = "#000000"

    def enter_hex(key, label, entry):
        hex_code = entry.get()
        if hex_code and hex_code.startswith('#') and (len(hex_code) == 7 or len(hex_code) == 4):
            colors[key] = hex_code
            label.config(bg=hex_code)
            apply_colors()
            settings.configure(bg=colors['bg'])

    def color_row(name, key):
        frame = tk.Frame(settings, bg=colors['bg'])
        frame.pack(pady=5, fill='x')
        tk.Label(frame, text=name, bg=colors['bg'], fg=label_fg, width=12, anchor='w', font=set_font).pack(side='left', padx=2)
        color_label = tk.Label(frame, bg=colors[key], width=6, height=1, relief='ridge', bd=2)
        color_label.pack(side='left', padx=2)
        hex_entry = tk.Entry(frame, width=10, font=set_font)
        hex_entry.insert(0, colors[key])
        hex_entry.pack(side='left', padx=2)
        tk.Button(frame, text="적용", command=lambda: enter_hex(key, color_label, hex_entry), font=set_font).pack(side='left', padx=2)

    color_row("배경색", 'bg')
    color_row("버튼색", 'btn')
    color_row("버튼 글씨색", 'btn_text')
    color_row("입력창 배경색", 'entry_bg')
    color_row("입력창 글씨색", 'entry_fg')


def click(btn_text):
    if btn_text == "=":
        try:
            result = str(eval(entry.get()))
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "오류")
    elif btn_text == "C":
        entry.delete(0, tk.END)
    elif btn_text == "√":
        try:
            value = float(entry.get())
            result = str(math.sqrt(value))
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "오류")
    elif btn_text == "x²":
        try:
            value = float(entry.get())
            result = str(value ** 2)
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "오류")
    elif btn_text == ".":
        current = entry.get()
        if not current:
            return
        last_op = max(current.rfind(op) for op in '+-*/')
        if "." in current[last_op+1:]:
            return
        # 마지막 입력이 연산자나 소숫점이면 소숫점 입력 불가
        if current[-1] in '+-*/.':
            return
        entry.insert(tk.END, ".")
    elif btn_text in "+-*/":
        current = entry.get()
        if not current:
            return
        # 마지막 입력이 연산자나 소숫점이면 연산자 입력 불가
        if current[-1] in '+-*/.':
            return
        entry.insert(tk.END, btn_text)
    elif btn_text == "설정":
        open_settings()
    else:
        entry.insert(tk.END, btn_text)

def on_key(event):
    key = event.keysym
    char = event.char
    if char in '+-*/.':
        current = entry.get()
        if not current:
            return
        # 마지막 입력이 연산자나 소숫점이면 연산자/소숫점 입력 불가
        if current[-1] in '+-*/.':
            return
        if char == ".":
            last_op = max(current.rfind(op) for op in '+-*/')
            if "." in current[last_op+1:]:
                return
        entry.insert(tk.END, char)
    elif char in '0123456789':
        entry.insert(tk.END, char)
    elif key == 'Return':
        click('=')
    elif key == 'BackSpace':
        entry.delete(len(entry.get())-1, tk.END)
    elif char.lower() == 'c':
        click('C')
    elif char == '^':
        try:
            value = float(entry.get())
            result = str(value ** 2)
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "오류")

def resize_fonts(event=None):
    w = root.winfo_width()
    h = root.winfo_height()
    btn_rows = total_rows - 1
    btn_height = h // total_rows
    btn_width = w // 4
    size = max(12, min(48, int(min(btn_height, btn_width) * 0.4)))
    entry_font = tkfont.Font(family="Arial", size=size)
    btn_font = tkfont.Font(family="Arial", size=size, weight="bold")
    entry.configure(font=entry_font)
    for btn in button_widgets:
        btn.configure(font=btn_font)

root = tk.Tk()
root.title("간단한 계산기")
root.configure(bg=colors['bg'])

entry = tk.Entry(root, width=20, font=("Arial", 18), justify="right",
                 bg=colors['entry_bg'], fg=colors['entry_fg'], insertbackground=colors['entry_fg'], relief='ridge', bd=4)
entry.grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky="nsew")

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "=", "+",
    "C", "√", "x²", "설정"
]

button_widgets = []
for i, text in enumerate(buttons):
    row = 1 + i // 4
    col = i % 4
    if text == "설정":
        btn = tk.Button(root, text=text, width=5, height=2, font=("Arial", 16),
                        command=open_settings, relief='groove', bd=2, highlightthickness=0, borderwidth=0)
    else:
        btn = tk.Button(root, text=text, width=5, height=2, font=("Arial", 16),
                        command=lambda t=text: click(t), relief='groove', bd=2, highlightthickness=0, borderwidth=0)
    # 둥근 버튼 효과
    btn.configure(overrelief='ridge')
    btn.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
    btn.configure(borderwidth=0, highlightbackground=colors['btn'], highlightcolor=colors['btn'])
    btn.configure(cursor="hand2")
    btn.configure(bg=colors['btn'], fg=colors['btn_text'])
    btn.configure(font=("Arial", 16, "bold"))
    btn.configure(relief="groove")
    btn.configure(highlightthickness=0)
    btn.configure(activebackground="#bbdefb", activeforeground=colors['btn_text'])
    btn.configure(highlightbackground=colors['btn'])
    # 둥글게 보이도록 radius 효과 (실제 완전한 원은 아니지만, 최대한 비슷하게)
    btn.configure(borderwidth=0)
    btn.configure(highlightthickness=0)
    btn.configure(pady=10)
    button_widgets.append(btn)

# grid row/column weight로 자동 리사이즈
total_rows = 1 + len(buttons) // 4  # 1은 입력창 row
for r in range(total_rows):
    root.grid_rowconfigure(r, weight=1)
for c in range(4):
    root.grid_columnconfigure(c, weight=1)

apply_colors()
root.bind('<Key>', on_key)
root.bind('<Configure>', resize_fonts)

root.mainloop()