import tkinter as tk

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
    else:
        entry.insert(tk.END, btn_text)

def on_key(event):
    key = event.keysym
    char = event.char
    if char in '0123456789+-*/':
        entry.insert(tk.END, char)
    elif key == 'Return':
        click('=')
    elif key == 'BackSpace':
        entry.delete(len(entry.get())-1, tk.END)
    elif char.lower() == 'c':
        click('C')

root = tk.Tk()
root.title("간단한 계산기")

entry = tk.Entry(root, width=20, font=("Arial", 18), justify="right")
entry.grid(row=0, column=0, columnspan=4)

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", "C", "=", "+"
]

for i, text in enumerate(buttons):
    btn = tk.Button(root, text=text, width=5, height=2, font=("Arial", 16),
                    command=lambda t=text: click(t))
    btn.grid(row=1 + i // 4, column=i % 4)

root.bind('<Key>', on_key)

root.mainloop()