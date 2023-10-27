#!/usr/bin/env python
"""
USB32をテストします。
2023/01/21  start
2023/10/18  start
            複数のUSB32をテストするため、USB32の番号を入力し
            その番号のUSB32のテストを実行する。
"""

import USB32_n
import time

# cmd_no_list = []
# for i in range(0,32):
#     cmd_no_list.append(i)
# print(cmd_no_list)

print()
while True:
    USB32_s = input("USB32の番号を入力:")
    USB32_No = int(USB32_s)
    print('USB32のテストをします。')
    print(' 1:全てのリレーを若番から順次on,offします。')
    print(' 2:指定Noのリレーをon,offします。')
    print(' q:プログラム終了')
    cmd = input('  input = ')
    print()

    if cmd == '1' :
        for cmd_no in range(0,32):
            USB32_n.usb_gpio(USB32_No,cmd_no)
            print(USB32_No,cmd_no)
            time.sleep(1)

    if cmd == '2' :
        cmd_no = int(input('Noを指定してください。'))
        if cmd_no >= 0 and cmd_no < 32:
            time.sleep(1)
            USB32_n.usb_gpio(USB32_No,cmd_no)
            print(USB32_No,cmd_no)
        else:
            print('範囲外のNoです。')

    if cmd == 'q' :
        break
    
        