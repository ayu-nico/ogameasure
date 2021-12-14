# coding:utf_8
import time
import datetime
import sys
import socket
from ..SCPI import scpi

class APSYN420(scpi.scpi_family):
    manufacturer = 'AnaPico'
    product_name = 'APSYN420'
    classification = 'Signal Generator'


    def query(self,cmd):
        self.send(cmd)
        time.sleep(0.05)
        recv = self.recv()
        return recv

	def send(self,cmd):
		try: self.com.send(cmd.encode("utf-8"))
		except: sys.exit("APSYN420_03")
		return True

	def recv(self,byte=1024):
		try: recv = self.com.recv(byte).decode("utf-8")
		except: sys.exit("APSYN420_04")
		return recv

	def get_ID(self):
		cmd = "*IDN?\n"
		id = self.query(cmd).rstrip("\n")
		return id

	def get_option(self):
		cmd = "*OPT?\n"
		res = self.query(cmd).split('"')
		if res[1] == "0": res = "None"
		elif res[1] == "B3": res = "Rechargeable Battery Pack"
		else : res = "Complex"
		return res

	def show_ID(self):
		ID = self.get_ID()
		option = self.get_option()
		print( "\n Device ID : %s" %ID)
		print( " Device Option : %s\n" %option)
		return True

	def get_IP(self):
		cmd = ":SYSTEM:COMMunicate:LAN:IP?\n"
		res = self.query(cmd).replace('"',"").rstrip("\n")
		return res

	def show_IP(self):
		res = self.get_IP()
		print("\n IPv4 Address = %s\n"%res)
		return True
    
    def set_IP(self,IP="192.168.10.151"):
		try:
			cmd = ':SYSTEM:COMMunicate:LAN:IP "%s"\n'%IP
		except:
			print("\n 有効な IPv4 Address が指定されていません。IP Address は文字列で指定してください。例 : '157.16.88.254")
			sys.exit("set_IP_01")
		try:
			self.send(cmd)
			res = self.get_IP()
			if IP == res:pass
			else:
				print("\n 指定された IPv4 Address を設定出来ませんでした。指定形式が間違っている可能性があります。現 IP = %s です。"%res)
				sys.exit("set_IP_02")
		except:
			print("\n 指定された IPv4 Address を設定出来ませんでした。指定形式が間違っているか、または通信タイムアウトです。")
			sys.exit("set_IP_03")
		return True
    
    
    	def get_LAN_mode(self):
		cmd = ":SYSTEM:COMMunicate:LAN:CONFig?\n"
		res = self.query(cmd).rstrip("\n")
		return res

	def show_LAN_mode(self):
		res = self.get_LAN_mode()
		print("\n LAN IPv4 Mode = %s\n"%res)
		return True

	def set_LAN_mode(self,mode="DHCP"):
		cmd = ":SYSTEM:COMMunicate:LAN:CONFig %s\n"%mode
		try:
			self.send(cmd)
			res = self.get_LAN_mode()
			if mode == res:pass
			else:
				print("\n 指定された LAN IPv4 Mode を設定出来ませんでした。指定形式が間違っている可能性があります。現 mode = %s です。"%res)
				sys.exit("set_LAN_mode_01")
		except:
			print("\n 指定された LAN IPv4 Mode を設定出来ませんでした。指定形式が間違っているか、または通信タイムアウトです。")
			sys.exit("set_LAN_mode_02")
		return True

	def get_RF_onoff(self):
		cmd = ":OUTPut?\n"
		res = self.query(cmd).rstrip("\n")
		if res == "0" : res = "OFF"
		elif res == "1" : res = "ON"
		else:
			print("\n RF の On/Off 状態を確認出来ませんでした。通信エラーの可能性があります。")
			sys.exit("get_RF_onoff")
		return res

	def show_RF(self):
		onoff = self.get_RF_onoff()
		mode = self.get_RF_mode()
		if mode == "FIX": mode = "CW"
		print("\n RF Output : %s"%onoff)
		print(" RF Output Mode : %s"%mode)
		self.show_freq()
		return True

	def RF_on(self):
		cmd = ":OUTPut ON\n"
		res = self.send(cmd)
		if res == True:
			stat = self.get_RF_onoff()
			if stat == "ON":pass
			else:
				print("\n RF を 正常に On 状態に出来ませんでした。通信エラーの可能性があります。")
				sys.exit("set_RF_on_01")
		else:pass
		return res

	def RF_off(self):
		cmd = ":OUTPut OFF\n"
		res = self.send(cmd)
		if res == True:
			stat = self.get_RF_onoff()
			if stat == "OFF":pass
			else:
				print("\n RF を 正常に Off 状態に出来ませんでした。通信エラーの可能性があります。")
				sys.exit("set_RF_on_01")
		else:pass
		return res

	def set_RF_mode(self,mode="CW"):
		mode_list = ["CW","FIXed","SWEep","LIST","CHIRp"]
		find = mode in mode_list
		if find == True:
			cmd = ":FREQuency:MODE %s\n"%mode
		elif find == False:
			print('\n RF mode の設定値が不正です。 mode は "CW","FIXed","SWEep","LIST","CHIRp" のいずれかで指定してください。')
			sys.exit("set_RF_mode_01")
		res = self.send(cmd)
		return res

	def get_RF_mode(self):
		cmd = ":FREQuency:MODE?\n"
		res = self.query(cmd).rstrip("\n")
		return res

	def show_RF_mode(self):
		res = self.get_RF_mode()
		if res == "FIX": res = "CW"
		print("\n RF Output Mode : %s\n"%res)
		return True

	def get_freq(self):
		cmd = ":FREQuency?\n"
		freq = self.query(cmd)
		return freq

	def show_freq(self):
		freq = float(self.get_freq())
		if freq >= 5.0*10**8 :
			freq = freq/10**9
			print("\n Output Frequceny = %.3f [GHz]\n"%freq)
		elif freq < 5.0*10**8 and freq >= 5.0*10**5:
			freq = freq/10**6
			print("\n Output Frequceny = %.3f [MHz]\n"%freq)
		elif freq < 5.0*10**5 and freq >= 5.0*10**2:
			freq = freq/10**3
			print("\n Output Frequceny = %.3f [kHz]\n"%freq)
		elif freq < 5.0*10**2:
			print("\n Output Frequceny = %.3f [Hz]\n"%freq)
		else:
			print("\n 有効な発振周波数を取得出来ませんでした。通信エラーの可能性があります。")
			sys.exit("show_freq_01")
		return True

	def show_freq_prec(self):
		freq = float(self.get_freq())
		if freq >= 5.0*10**8 :
			freq = freq/10**9
			print("\n Output Frequceny = %f [GHz]\n"%freq)
		elif freq < 5.0*10**8 and freq >= 5.0*10**5:
			freq = freq/10**6
			print("\n Output Frequceny = %f [MHz]\n"%freq)
		elif freq < 5.0*10**5 and freq >= 5.0*10**2:
			freq = freq/10**3
			print("\n Output Frequceny = %f [kHz]\n"%freq)
		elif freq < 5.0*10**2:
			print("\n Output Frequceny = %f [Hz]\n"%freq)
		else:
			print("\n 有効な発振周波数を取得出来ませんでした。通信エラーの可能性があります。")
			sys.exit("show_freq_prec_01")
		return True

	def set_freq(self,freq=1.0,unit="GHz"):
		if unit == "GHz": freq = freq*10**9
		elif unit == "MHz": freq = freq*10**6
		elif unit == "kHz": freq = freq*10**3
		elif unit == "Hz": pass
		else :
			print('\n 発振周波数設定値の単位が有効ではありません。引数 unit は "GHz","MHz""kHz","Hz" のいずれかを指定してください。')
			sys.exit("set_freq_01")
		cmd = ":FREQuency %.3f\n"%freq
		self.send(cmd)
		res = float(self.get_freq())
		if freq == res: pass
		else:
			print("\n [Caution] SG の発振周波数(%.3f)と、設定値(%.3f)が異なります。"%(res,freq))
		return True

	def sweep_test1(self,start,stop,step,unit="GHz"):
		point = math.ceil((stop-start)/step)
		i=0
		while i <= point:
			freq = start+step*i
			self.set_freq(freq,unit)
			self.show_freq()
			i +=1
			if i < point:
				a = input("次の準備 OK ? : ")
			else:pass

		return True
