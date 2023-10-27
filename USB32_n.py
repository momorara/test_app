"""
2023/01/21	USB32をラズパイで使用するために作りました。
	# on , off とも1回の指令では、動作する時もあるが、動作しない場合もある
	# on , off とも2回指令を出せば確実なようだ
	# なので、それぞれ同方向指令を2回、念の為3回出す事とする。
	# offについては、readすれば、offになるようなので、
	# 2回off指令を出した後、readしてoffを確認するのもいいかな。
	# もし仮に0のはずが、1だった場合、あと2回off指令を出すのも良い。
	# 上記挙動はgpio iodir xxxxxxxx による方向制御をせずにやっているので、
	# 発生しているのかもしれない。ただ set read を複数行う事で個別GPIO単位で
	# 方向決定できているので、今回の使い方では問題ないと思う。
	と言うことで、かなり冗長というか無駄な動きをしています。
2023/10/16  複数USB32に対応した改造スタート
			USB32ナンバーと商品ナンバーを1対だけ受け取ってロック解除するようにする
2023/10/18  チェック
"""
import serial
import time

def usb_gpio(USB32_No,e_lock_No):
	# USB32_No で指定したUSB32に対して、e_lock_Noの番号のGPIOを約1秒弱onにします。
	# USB32_Noに対してもない番号が切ると、無視
	# 現在は 0 - 31 の番号にのみ反応します。他は無視
	try:
		USB32 = '/dev/ttyACM' + str(USB32_No)
		serPort = serial.Serial(USB32, 19200, timeout=1) 
		# print(USB32)
	except:
		print('USB接続がないかもです。')
		return

	GPIO  = [b'0',b'1',b'2',b'3',b'4',b'5',b'6',b'7',b'8',b'9']
	GPIO1 = (b'A',b'B',b'C',b'D',b'E',b'F',b'G',b'H',b'I',b'J',b'K')
	GPIO2 = (b'L',b'M',b'N',b'O',b'P',b'Q',b'R',b'S',b'T',b'U',b'V')
	GPIO.extend(GPIO1)
	GPIO.extend(GPIO2)

	# GPIO ON
	for i in range(3):
		word = b"gpio set " + GPIO[e_lock_No] + b" \r"
		serPort.write(word)
		# print(word)
		time.sleep(0.1)

	time.sleep(0.5)

	# GPIO OFF
	for i in range(2):
		word = b"gpio clear " + GPIO[e_lock_No] + b" \r"
		serPort.write(word)
		time.sleep(0.1)

	# GPIO OFF 確認
	word = b"gpio read " + GPIO[e_lock_No] + b" \r"
	serPort.write(word)
	response = serPort.read(25)
	if ("1" in str(response[-4:-3])):# offのはずが、onなら再度clearする。
		for i in range(2):
			print('offのはずが、onなら再度clearする。')
			word = b"gpio clear " + GPIO[e_lock_No] + b" \r"
			serPort.write(word)
			time.sleep(0.1)

	# ダメ押しでclearしておく
	word = b"gpio clear " + GPIO[e_lock_No] + b" \r"
	serPort.write(word)
	time.sleep(0.1)

	serPort.close()

def main():
	USB32_No  = 0
	e_lock_No = 3
	usb_gpio(USB32_No,e_lock_No)

if __name__ == '__main__':
    main()