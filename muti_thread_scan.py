#coding=utf-8
import zbar
from PIL import Image
import sys
import threading
import time
import os
import re

reload(sys)
#设置系统默认编码方式，避免中文乱码
sys.setdefaultencoding('utf-8')
#创建MyThread线程类
class MyThread(threading.Thread):
	def __init__(self, func, args):
		threading.Thread.__init__(self)
		self.func = func
		self.args = args
	#改写run方法
	def run(self):
		#apply用于间接的调用func函数
		apply(self.func, self.args)
#二维码扫描类
def qrScan(folder):
	#计算图片数量的全局变量
	global total
	global is_qr
	#创建zbar扫描器
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')
	#遍历folder路径下的所有内容，walk返回3个值（路径，路径下的文件夹，路径下的文件）
	for root,dir,files in os.walk(folder):
		#遍历该文件夹下的所有文件
		for file in files:
			#挨个打开二维码图片
			img = Image.open(root+"/"+file).convert('L')
			w, h = img.size
			zimg = zbar.Image(w, h, 'Y800', img.tobytes())
			#开始扫描图片
			scanner.scan(zimg)
			#创建互斥锁
			lock = threading.Lock()
			#获取锁
			lock.acquire()
			try:
				total += 1
			finally:
				#释放锁
				lock.release()
			for s in zimg:
				# 如果是二维码，打印二维码的相关数据
				if s.data:
					#获取锁
					lock.acquire()
					is_qr += 1
					data_file = open("./output/qr_data.ini", "a")
					data_file.write( str(file) + "=" + s.data.decode('utf-8').encode('gbk') + "\n")
					print str(file)+":"+s.data.decode('utf-8').encode('gbk')+"\n"
					data_file.close()
					#释放锁
					lock.release()
				# 如果不是二维码，这里给出提示
				else:
					#获取锁
					lock.acquire()
					error_info = open("./output/error_info.txt", "a")
					error_info.write("ERROR : "+str(file)+" is not QRcode!\n")
					error_info.close()
					print  "ERROR : "+str(file)+" is not QRcode!\n"
					#释放锁
					lock.release()

def createIni(section = "[Qrdata]"):
	#创建ini数据库
	#判断ini文件是否有section
	match_section = re.compile(section)
	#判断是否存在output文件夹，若不存在则创建
	if not os.path.exists("output"):
		os.mkdir("output")
	data_file = open("./output/qr_data.ini", "a+")
	#定位到文件首位
	data_file.seek(0,0)
	first_line = data_file.read()
	#如果文首没有匹配到section自动添加进去
	if not re.search(match_section, first_line):
		data_file.seek(0,0)
		data_file.write(str(section)+"\n")
	data_file.close()
					
#创建多线程方法
def createMutiThread(img_folder):
	#定义线程总数
	thread_num = range(len(img_folder))
	#创建线程列表
	threads = []
	#创建多线程
	for f in img_folder:
		t = MyThread(qrScan,(f,))
		threads.append(t)
	#运行线程
	for i in thread_num:
		threads[i].start()
	#阻塞进程直到线程执行完毕
	for i in thread_num:
		threads[i].join()
					
if __name__ == '__main__':
	#创建输出目录
	createIni()
	#记录图片总数
	total = 0
	is_qr = 0
	#创建二维码图片路径列表
	img_folder = []
	for i in sys.argv[1:]:
		img_folder.append(i)

	if not img_folder:
		print "ERROR:please input file path!"
	
	#记录扫描开始时间
	start = time.time()
	
	#创建多线程进行扫描
	createMutiThread(img_folder)

	spend = time.time() - start
	print "总耗时：" + str(spend) + "秒"
	print "共扫描" + str(total) + "张图片"
	print "其中有效的二维码图片有" + str(is_qr) + "张"
		