import tkinter as tk
from tkinter import *

scan_frame = None
scroll_frame = None

def create_ui(root):
    global scan_frame
    global scroll_frame

    # UI 제목
    root.title("TS100-Project")

    # Bottom 프레임, Scan TS100, Temperature Information을 포함함
    bottom_frame = Frame(root)

    # Scan리스트 Frame
    scan_ts100_frame = LabelFrame(bottom_frame, relief="solid", bd=1, text="Scan TS100", width=115)
    scan_ts100_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # 전역변수 할당
    scan_frame = scan_ts100_frame

    # 온도정보 Frame
    temperature_information_frame = LabelFrame(bottom_frame, relief="solid", bd=1, text="Temperature Information")
    canvas = Canvas(temperature_information_frame, borderwidth=0)
    scrollbar = Scrollbar(temperature_information_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    # 전역변수 할당
    scroll_frame = scrollable_frame

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    temperature_information_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y", expand=True)

    # Scan 버튼
    scan_button = Button(root, text="Scan", command=scan_button_click)
    scan_button.pack()

    # 하위 프레임
    bottom_frame.pack(side="bottom", fill="both", expand=True)

# Scan 버튼클릭 시 호출되는 함수
def scan_button_click(scan_frame):
    print("Scan Button Click")

if __name__ == "__main__":
    root = tk.Tk()

    create_ui(root)

    # 이벤트루프 생성
    loop = asyncio.get_event_loop()

    # 비동기로 UI 계속 업데이트
    def asyncio_loop():
        loop.call_soon(loop.stop)
        loop.run_forever()
        root.after(100, asyncio_loop)

    root.after(100, asyncio_loop)
    root.mainloop()