'''
和主机进行通讯

'''
import  time
import  threading
from    ctypes      import  *
from    SerialPort  import  *


#加载同目录下的dll
Crc = CDLL(".\\CrcCheck.dll")               #进行CRC校验

send_buf    = (c_byte * 5)(0x55,0xDD,0xFF,0x01,0xCE )       #应答数据

class PcComInfo(Structure):
	_fields_ = [
	                 ('motor',c_uint8),
	                 ('sensor',c_uint8),
                         ('rotate',c_uint16)
                   ]

class  PcComm:
    def __init__(self,port,baund = 9600):
        self.rcflg = 0                                          #接收成功标识
        self.rcbuf = PcComInfo(0,0,0)                                #接收数据

        self.ser = SerialPort(port,baund)                       #初始化串口
        self.ser.open()                                         #打开串口
        pcThread = threading.Thread(target = self.ser.recv)     #创建多线程，启动接收任务
        pcThread.start()

    def recvThread(self):
        while True:
            time.sleep(0.2)                                     #循环周期
            
            if( self.ser.recv_len ):                            #数据接收成功
                
                Crc.GetCheckSum.restype   = c_uint8             #GetCheckSum 返回值类型 
                crc = Crc.GetCheckSum(self.ser.recv_buf, self.ser.recv_len-1) #计算校验和

                #print(self.ser.recv_buf)
                #print(crc,self.ser.recv_buf[self.ser.recv_len-1])
                if(crc == self.ser.recv_buf[self.ser.recv_len-1]):   #校验正确
                    self.ser.send(send_buf)                     #发送应答，标识接收正常
                    #self.rcbuf = self.ser.recv_buf[2:self.ser.recv_len-1]
                    self.rcbuf.motor    = self.ser.recv_buf[2]
                    self.rcbuf.sensor   = self.ser.recv_buf[3]
                    #print(self.ser.recv_buf[4],self.ser.recv_buf[4]<<8,self.ser.recv_buf[5])
                    
                    self.rcbuf.rotate   = (int(self.ser.recv_buf[4]) + int(self.ser.recv_buf[5]<<8))
                    #print("struct:",self.rcbuf.motor,self.rcbuf.sensor,self.rcbuf.rotate)
                    #print(self.rcbuf)

                    self.rcflg = 1                              #置接收成功标识

                self.ser.recv_len = 0                           #清除进入循环条件
                    

'''            
Port  =     "COM8"                                              #串口
Rate  =     9600                                                #波特率

pc = PcComm(Port,Rate)
pcinfo = PcComInfo()
t1 = threading.Thread(target = pc.recvThread)
t1.start()
while True:
    if pc.rcflg == 1:
        pc.rcflg = 0
        pcinfo = pc.rcbuf
        print("motor:",pcinfo.motor,pcinfo.sensor,pcinfo.rotate)
'''   
