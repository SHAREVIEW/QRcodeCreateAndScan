# 使用前，请先部署相应的环境

## 具体情况，请看“setEnvironment.txt”


-------------qr_scan.py-------------

	程序：二维码扫描


	功能：扫描单张二维码

	操作：在命令行输入 “文件名”即可进行扫描
	示例1：python qr_scan.py test.jpg
	示例2：python qr_scan.py ./output/test.jpg
	
	
	说明：1.会在当前目录下创建一个output文件夹

		/output/qr_data.ini为数据库文件，保存扫描结果


-------------qr_create.py-------------

	程序：二维码生成

	功能：生成单张二维码(支持中英文，数字，符号)

	操作：在命令行输入 “字符串” “图片名”即可创建二维码
	示例：python qr_create.py "this is test001" "test.jpg"
	
	说明：1.生成的二维码图片默认放在当前目录下的output文件夹下
	
-------------muti_thread_scan.py-------------

	程序：二维码文件夹扫描


	功能：多线程扫描二维码文件夹

	操作：在命令行输入 “文件夹名” “文件夹名”... 即可进行多线程扫描
	示例1：python muti_thread_scan.py “test_all"
	示例2：python muti_thread_scan.py “test_all" "test_half"
	
	
	说明：1.会在当前目录下创建一个output文件夹

		/output/qr_data.ini为数据库文件，保存扫描结果
		
		/output/error_info.txt为非二维码图片的错误信息
		
		2.当只传入一个文件夹名时，程序进行单线程扫描
	
	
### 补充说明
* 程序运行结束后，不会关闭而是暂停窗口
* 若有需要关闭窗口的，注释掉程序最后一行的os.system("pause")即可


--------------@weekdawn---------------
