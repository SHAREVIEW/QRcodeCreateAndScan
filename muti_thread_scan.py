#coding=utf-8
import zbar
from PIL import Image
import sys
import threading
import time
import os
import re

reload(sys)
#����ϵͳĬ�ϱ��뷽ʽ��������������
sys.setdefaultencoding('utf-8')
#����MyThread�߳���
class MyThread(threading.Thread):
	def __init__(self, func, args):
		threading.Thread.__init__(self)
		self.func = func
		self.args = args
	#��дrun����
	def run(self):
		#apply���ڼ�ӵĵ���func����
		apply(self.func, self.args)
#��ά��ɨ����
def qrScan(folder):
	#����ͼƬ������ȫ�ֱ���
	global total
	global is_qr
	#����zbarɨ����
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')
	#����folder·���µ��������ݣ�walk����3��ֵ��·����·���µ��ļ��У�·���µ��ļ���
	for root,dir,files in os.walk(folder):
		#�������ļ����µ������ļ�
		for file in files:
			#�����򿪶�ά��ͼƬ
			img = Image.open(root+"/"+file).convert('L')
			w, h = img.size
			zimg = zbar.Image(w, h, 'Y800', img.tobytes())
			#��ʼɨ��ͼƬ
			scanner.scan(zimg)
			#����������
			lock = threading.Lock()
			#��ȡ��
			lock.acquire()
			try:
				total += 1
			finally:
				#�ͷ���
				lock.release()
			for s in zimg:
				# ����Ƕ�ά�룬��ӡ��ά����������
				if s.data:
					#��ȡ��
					lock.acquire()
					is_qr += 1
					data_file = open("./output/qr_data.ini", "a")
					data_file.write( str(file) + "=" + s.data.decode('utf-8').encode('gbk') + "\n")
					print str(file)+":"+s.data.decode('utf-8').encode('gbk')+"\n"
					data_file.close()
					#�ͷ���
					lock.release()
				# ������Ƕ�ά�룬���������ʾ
				else:
					#��ȡ��
					lock.acquire()
					error_info = open("./output/error_info.txt", "a")
					error_info.write("ERROR : "+str(file)+" is not QRcode!\n")
					error_info.close()
					print  "ERROR : "+str(file)+" is not QRcode!\n"
					#�ͷ���
					lock.release()

def createIni(section = "[Qrdata]"):
	#����ini���ݿ�
	#�ж�ini�ļ��Ƿ���section
	match_section = re.compile(section)
	#�ж��Ƿ����output�ļ��У����������򴴽�
	if not os.path.exists("output"):
		os.mkdir("output")
	data_file = open("./output/qr_data.ini", "a+")
	#��λ���ļ���λ
	data_file.seek(0,0)
	first_line = data_file.read()
	#�������û��ƥ�䵽section�Զ���ӽ�ȥ
	if not re.search(match_section, first_line):
		data_file.seek(0,0)
		data_file.write(str(section)+"\n")
	data_file.close()
					
#�������̷߳���
def createMutiThread(img_folder):
	#�����߳�����
	thread_num = range(len(img_folder))
	#�����߳��б�
	threads = []
	#�������߳�
	for f in img_folder:
		t = MyThread(qrScan,(f,))
		threads.append(t)
	#�����߳�
	for i in thread_num:
		threads[i].start()
	#��������ֱ���߳�ִ�����
	for i in thread_num:
		threads[i].join()
					
if __name__ == '__main__':
	#�������Ŀ¼
	createIni()
	#��¼ͼƬ����
	total = 0
	is_qr = 0
	#������ά��ͼƬ·���б�
	img_folder = []
	for i in sys.argv[1:]:
		img_folder.append(i)

	if not img_folder:
		print "ERROR:please input file path!"
	
	#��¼ɨ�迪ʼʱ��
	start = time.time()
	
	#�������߳̽���ɨ��
	createMutiThread(img_folder)

	spend = time.time() - start
	print "�ܺ�ʱ��" + str(spend) + "��"
	print "��ɨ��" + str(total) + "��ͼƬ"
	print "������Ч�Ķ�ά��ͼƬ��" + str(is_qr) + "��"
		