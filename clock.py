import tkinter as tk
import time

def update_time():
    current_time = time.strftime('%H:%M:%S')
    label.config(text=current_time)
    root.after(1000, update_time)

root = tk.Tk()
root.title("현재 시간")
root.attributes('-topmost', True)  # 항상 위에 표시 (원하지 않으면 이 줄 삭제)
root.geometry("350x100+100+100")    # 창 크기와 위치

label = tk.Label(root, font=('Arial', 40), fg='black')
label.pack(expand=True)

update_time()
root.mainloop()