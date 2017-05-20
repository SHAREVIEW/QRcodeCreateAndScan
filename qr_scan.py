#coding=utf-8

#此版本为阉割版，生成的ini有多个值每次每次显示文件名和对应的扫描值
import zbar
from PIL import Image
import sys
import os
import re
import time

reload(sys)
#设置系统默认编码方式，避免中文乱码
sys.setdefaultencoding('utf-8')

#创建zbar扫描器
class Scaner:
	def __init__(self, file_name):
		self.file_name = file_name
		#配置ini文件的section和key
		self.section = "[Qrdata]"
	
	#扫描图片
	def qrScan(self):
		scanner = zbar.ImageScanner()
		#打开zbar解析配置
		scanner.parse_config('enable')
		#打开需要扫描的二维码
		img = Image.open(self.file_name).convert('L')
		#获取二维码图片的宽和高
		w, h = img.size
		#将图片数据传入扫描器
		zimg = zbar.Image(w, h, 'Y800', img.tobytes())
		scanner.scan(zimg)
		for s in zimg:
			if not s.data:
				print "error:This is not QRcode!\nPlease select another photo."
			else:
				dir,file = os.path.split(self.file_name)
				data_file = open("./output/qr_data.ini", "a")
				data_file.write(str(file) + "=" + s.data.decode('utf-8').encode('gbk') + "\n")
				print "Scan QrCode successed!"
				print s.data
				data_file.close()
		
	#创建ini数据库
	def createIni(self):
		#判断ini文件是否有section,和重复的value
		match_section = re.compile(self.section)
		#判断是否存在output文件夹，若不存在则创建
		if not os.path.exists("./output"):
			os.mkdir("./output")
		data_file = open("./output/qr_data.ini", "a+")
		# 定位到文件首位
		data_file.seek(0,0)
		first_line = data_file.readline()
		# 如果文首没有匹配到section自动添加进去
		if not re.search(match_section, first_line):
			data_file.seek(0,0)
			data_file.write(str(self.section)+"\n")
		data_file.close()

if __name__ == '__main__':
	#从命令行接收文件路径
	file_name = sys.argv[1]
	start = time.time()
	q = Scaner(file_name)
	q.createIni()
	q.qrScan()
	spend = time.time() - start
	print u"总耗时：" + str(spend) + u"秒"
	os.system("pause")
	
	
	
	