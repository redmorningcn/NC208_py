'''
作者：redmorningcn  20.03.01

函数：SetRelays(master,node,bin16list)，master：MbMaser对象，通过串口设置继电器组，val
函数：ClearAllRelays(master)，clear 所有寄存器组

'''

from    MdMaster import *  
from    dec2bin16 import * 

#将指定节点值的寄存器清零
def SetRelays(master,node,val):
    addr = 0
    if node:                                #值大于零
        #高字节和低字节互换
        tmp = val % 65536
        lo  = tmp % 256
        lolist = dec2bin8list(lo)[::-1]
        
        hi  = int(tmp / 256)
        hilist = dec2bin8list(hi)[::-1]
        val = lo * 256 + hi

        bin16list = hilist + lolist 
        
        #bin16list = dec2bin16list(val)
        #print(bin16list)
        master.CoilsWr(node,addr,bin16list)         #设置继电器组值，打开指定通道

#清除所有寄存器值
def ClearAllRelays(master):
    addr = 0
    val  = 0
    for i in range(18):
        try:
            bin16list = dec2bin16list(val)              #置所有值为0
            node = i + 1
            print("node%d清零"%node)
            master.CoilsWr(node,addr,bin16list)         #设置继电器组值，打开指定通道
        except Exception as e:
            print("序号：",i,e)
            
 

'''
import  time
from    ctypes import *

serialPort  = "COM10"                       #串口
baudRate    =  9600  
master = MdMaster(serialPort,baudRate)

node = 1
val = 0
while True:
    #time.sleep(5)
    node = int(input("input node:"))
    val  = int(input("input val:"))
    vlist = dec2bin16list(val)
    print(vlist)
    #vlist = [1,0,1,0]
    SetRelays(master,node,vlist)
'''
