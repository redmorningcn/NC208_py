#控制电机运行
#
#包：Motor(参数：port,baund)
#
#方法：setSpeed(self,node,speed)，设置指定编号的速度。

from MdMaster import *  

E2000_START_NODE		= 64
E2000_MAX_NUM			= 8
		
ADDR_START_SOUREC		= 0x0200		# 地址：启动指令来源 	 	*/
ADDR_X_FRQ_SOUREC		= 0x0203		# 地址：X频率来源    		*/
ADDR_FRQ_TARGET			= 0x010D		# 地址：目标频率（转速） 	*/	
ADDR_TURN_CHOOSE		= 0x0102		# 地址：正转锁定			*/	
ADDR_MOTOR_CTRL			= 0x2000		# 地址：电机启动、停止转动 */
ADDR_MOTOR_WISE			= 0x2000		# 地址：电机方向			*/
		
CODE_START_CLOCKWISE	        = 0x0001		# 指令：启动正转			*/
CODE_START_UNCLOCKWISE	        = 0x0002		# 指令：启动反转			*/  
		
CODE_START_CLOCKWISE	        = 0x0001		# 指令：启动正转			*/
CODE_START_UNCLOCKWISE	        = 0x0002		# 指令：启动反转			*/  
CODE_X_MODBUS			= 0x000A		# 指令：主频来源modbus		*/
CODE_START_MODBUS_PANEL         = 0x0004		# 指令：启动指令来源面板+modbus */
CODE_TURN_CLOCKWISE		= 0x0000		# 指令：正向锁定			*/
CODE_TURN_UNCLOCKWISE	        = 0x0001		# 指令：反向锁定  			*/
CODE_MOTOR_STOP			= 0x0003		# 指令：减速停机			*/
CODE_MOTOR_STOP_FREE	        = 0x0004		# 指令：自由停机			*/		


def setSpeed(master,node,speed):
    if speed == 0:
        master.RegWr(node,ADDR_MOTOR_CTRL,CODE_MOTOR_STOP)                  #电机停止
    else:
        master.RegWr(node,ADDR_X_FRQ_SOUREC,CODE_X_MODBUS)               #设置主频
        master.RegWr(node,ADDR_START_SOUREC,CODE_START_MODBUS_PANEL)     #设置启动来源
        master.RegWr(node,ADDR_FRQ_TARGET,speed)                         #设置速度
        master.RegWr(node,ADDR_MOTOR_CTRL,CODE_START_CLOCKWISE)          #正转 
        '''
        master.RegsWr(node,ADDR_X_FRQ_SOUREC,[CODE_X_MODBUS])               #设置主频
        master.RegsWr(node,ADDR_START_SOUREC,[CODE_START_MODBUS_PANEL])     #设置启动来源
        master.RegsWr(node,ADDR_FRQ_TARGET,[speed])                         #设置速度
        master.RegsWr(node,ADDR_MOTOR_CTRL,[CODE_START_CLOCKWISE])          #正转 
        '''
'''

import  time

class Motor:
    def __init__(self,master):                                           #初始化电机的控制串口
        #self.motor = MdMaster(port,baund)
        self.motor = master
    def setSpeed(self,node,speed):
        if speed == 0:
            self.motor.RegWr(node,ADDR_MOTOR_CTRL,CODE_MOTOR_STOP)                  #电机停止
        else:
            self.motor.RegsWr(node,ADDR_X_FRQ_SOUREC,[CODE_X_MODBUS])               #设置主频
            self.motor.RegsWr(node,ADDR_START_SOUREC,[CODE_START_MODBUS_PANEL])     #设置启动来源
            self.motor.RegsWr(node,ADDR_FRQ_TARGET,[speed])                         #设置速度
            self.motor.RegsWr(node,ADDR_MOTOR_CTRL,[CODE_START_CLOCKWISE])          #正转


'''
'''
serialPort  = "COM10"                                   #串口
baudRate    =  9600
node = 1
addr = 0
motor = MdMaster(serialPort,baudRate)
#m =  Motor(motormaster)
#m2 =m
#m2 =  Motor(serialPort,baudRate)

setSpeed(motor,node,100)

'''

