##---------------------------------------------
## PROJECT: Cattest   FILE NAME: messageHash
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 8/18/17:8:41 AM
##---------------------------------------------

import sys
from Crypto.Cipher import AES


class Mask(object):
	def __init__(self, msg):
		self.msg = msg
		self.objE = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
		self.objD = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')

	def encrypt(self):
		enc = self.objE.encrypt(self.msg)
		return enc

	def decrypt(self, enc):
		dec = self.objD.decrypt(enc).decode("utf-8")
		return dec


def main():
	psw = Mask('password')
	enc = psw.encrypt()
	dec = psw.decrypt(enc)


if __name__ == "__main__":
	main()
	sys.exit(0)