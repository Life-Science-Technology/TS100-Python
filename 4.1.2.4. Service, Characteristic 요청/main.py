import asyncio # 비동기화 모듈
from typing import Optional # 타입 어노테이션 관련 모듈

from bleak import BleakScanner, BleakClient # BLE 관련 모듈

import tkinter as tk # GUI 라이브러리

# 비동기 형태로 BLE 장치 검색
async def scan():
    ts100_device = []

    print('Scan Start')
    # scan start
    scan_devices = await BleakScanner.discover()
    print('Scan End')

    # 스캔된 device 탐색
    for device in scan_devices:
        # 이름이 없는 Device "Unknown Device로 변경"
        device_name = device.name if device.name else "Unknown Device"
        # 이름에 TS100을 포함하면 콘솔에 출력
        if "TS100" in device_name:
            ts100_device.append(device)
            print(device_name)
    
    return ts100_device

# GUI로 화면에 나타내는 함수
def show_scan_devices(devices):
    if not devices:
        return False

    window = tk.Tk()
    # 화면 제목
    window.title("TS100 Scan List")

    buttons = []
    for device in devices:
        text = device.name
        # 버튼 이벤트 추가(button_click 함수 호출)
        button = tk.Button(window, text=text, command=lambda device=device: button_click(device, window))
        button.pack()
        buttons.append(button)

    # 윈도우 종료까지 실행
    window.mainloop()

# 버튼 클릭 시 호출되는 함수
def button_click(device, window):
    global selected_device # 전역변수 함수내 사용하도록 설정
    selected_device = device # 선택한 Device selected_device 변수에 담기

    # remove gui
    window.quit()

# 선택한 TS100에 연결하는 함수
async def connect(candidate_device):
    print('connect start')

    selected_client = BleakClient(candidate_device)

    try:
        # 장치 연결 시작
        await selected_client.connect()
        print('connected')
    except Exception as e:
        # 연결 실패시 발생
        print('error: ', e, end='')
        return None

    return selected_client

# Service, Characteristic 확인하는 함수
async def get_service_and_characteristic(connected_device):
    # Service 확인
    for service in connected_device.services:
        print(service)
        # Characteristic 확인
        for characteristic in service.characteristics:
            print(characteristic)
        
        print()

selected_device = None

if __name__ == '__main__':
    # 비동기 이벤트 루프 생성
    loop = asyncio.get_event_loop()
    # 비동기 형태로 Scan함수 실행
    scan_devices = loop.run_until_complete(scan())
    # Scan된 기기 화면으로 출력
    show_scan_devices(scan_devices)

    connected_device = None
    # 선택한 기기가 None이 아니라면
    if selected_device is not None:
        # connect 요청 후 함수가 끝날때까지 기다림
        connected_device = loop.run_until_complete(connect(selected_device))
    # TS100과 연결되어 있다면
    if connected_device is not None:
        # Service, Characteristic 출력하는 함수 호출
        loop.run_until_complete(get_service_and_characteristic(connected_device))