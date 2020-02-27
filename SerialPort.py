'''
包：SerialPort
包初始化：port,buand  端口，和波特率
方法：port_open
方法：port_close
方法：

'''
import serial
import time
import threading
from ctypes import *   #C语言

#加载同目录下的dll
Crc = CDLL(".\\CrcCheck.dll")       


class SerialPort:
    message=''
    def __init__(self,port,buand):
        super(SerialPort, self).__init__()
        try:
            self.ser=serial.Serial(port,buand)         #配置串口
            self.ser.close()                           #串口关闭
            if not self.ser.isOpen():
                self.ser.open()            
        except Exception as e:
            print("---串口打开异常---：", e)
        
  
    def port_open(self):                            #方法，打开串口
        if not self.ser.isOpen():
            self.ser.open()
                
    def port_close(self):                           #方法，关闭串口
        self.ser.close()
            
    def send_data(self,data):                       #方法，发送数据
        #data = input("请输入要发送的数据（非中文）并同时接收数据: ")
        #n=self.port.write((data).encode())
        n=self.ser.write((data))
        return n


    def read_data(self):                            #方法，接收数据
            
        lst_num = 0                                 #前次接收到的数据长度
        self.recv_buf       = []                    #接收数据缓存区
        self.recv_len       = 0                     #接收数据长度
            
        while True:
            if self.ser.in_waiting:                 #有数据
                if((self.ser.in_waiting > lst_num)):
                    lst_num = self.ser.in_waiting    #两次后，接收不增，才确认接收完成
                    time.sleep(0.005)              #停5ms
                    print("已接收：%d,%d",lst_num,self.ser.in_waiting,self.ser.in_waiting > lst_num)
                else:
                    print("接收完成",lst_num,self.ser.in_waiting)
                    lst_num = 0                             #准备下次接收
                    self.recv_len       = self.ser.in_waiting    #数据长度
                    self.recv_buf       = self.ser.read(self.ser.in_waiting ) #数据读取 


serialPort  = "COM8"      #串口
baudRate    = 9600           #波特率

if __name__=='__main__':
    mSerial=SerialPort(serialPort,baudRate)
    mSerial.port_open()
    t1=threading.Thread(target=mSerial.read_data)

    t1.start()
    while True:
        time.sleep(1)
        if(mSerial.recv_len):
            print(mSerial.recv_buf)
            print(Crc.GetCheckSum(mSerial.recv_buf,mSerial.recv_len-1))
            mSerial.recv_len = 0
        
        #mSerial.send_data()
