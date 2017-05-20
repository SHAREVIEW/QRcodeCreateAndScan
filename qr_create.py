#coding=utf-8
import qrcode
import sys
import os
import time

reload(sys)
#设置系统默认编码方式，避免中文乱码
sys.setdefaultencoding('utf-8')
#二维码创建
class QrCreate:
	#参数说明：data为需要转换成二维码的数据，img_name为生成的二维码名称
	def __init__(self, data, name):
		self.data = data
		self.img_name = name
	
	#创建二维码
	def create(self):
		#创建输出文件夹
		if not os.path.exists("output"):
			os.mkdir("output")
		#生成的二维码参数设置
		qr = qrcode.QRCode(
			version = 2,	#表示生成二维码的尺寸大小[1,40]
			error_correction = qrcode.constants.ERROR_CORRECT_L,#制定二维码的容错系统L,M,Q,H
			box_size = 5,	#表示每个格子的像素大小
			border = 1	#表示边框的格子厚度是多少（默认为4）
			)
		qr.add_data(self.data)
		qr.make(fit=True)
		img = qr.make_image()
		img_path = "./output/" + str(self.img_name)
		img.save(img_path)
		
if __name__ == '__main__':
	#从命令行接收二维码数据
	qr = QrCreate(sys.argv[1].decode("gbk").encode("utf-8"), sys.argv[2])
	start = time.time()
	qr.create()
	spend = time.time() - start
	print u"总耗时：" + str(spend) + u"秒"
	print "QRCode created successfully!" 
	os.system("pause")
