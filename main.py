from    SwitchTable import  *      #切换配置表
from    PcComm      import  *      #和测试台电脑通讯
from    Relays      import  *      #继电器组切换，通道选择
from    E2001       import  *      #速度切换
import  time
from    SysConfig   import  *      #配置文件
import  sys
import  os
from time import strftime, localtime

version = "V1.2"
#配置文件路径
path    = r"F:\cvi\app\NC208\NC208measureconfig.csv"
#测试台串口
pcPort  = "COM8"
pcBaud = 9600
#切换装置串口
swPort  = "COM10"
swBaud = 9600
debug  = 0

class Logger(object):
    def __init__(self, filename="log.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
 
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()    

    def flush(self):
        pass

#初始化函数
def getConfig():
    global  path
    global  pcPort
    global  pcBaud
    global  swPort
    global  swBaud
    global  debug

    
    conf = ReadConfig()
    path = conf.File("path")
    print("配 置 信 息 ： ")
    print("传感器配置表：",path)
    
    pcPort = conf.PcSer("port")
    pcBaud = int(conf.PcSer("baud"))
    print("测试台串口  ： %s，波特率： %d bps；"%(pcPort,pcBaud))
    
    swPort = conf.SwSer("port")
    swBaud = int(conf.SwSer("baud"))
    print("切换装置串口： %s，波特率： %d bps；"%(swPort,swBaud))
    
    print('\r\n-------------------------------------------')
    debug = int(conf.Debug("debug"))
    print("模 式 选 项 ：\r\n<0>：通道切换  (运行模式)；\r\n<1>：传感器控制(调试模式)；\r\n<2>：速度控制  (调试模式)；")
    print("\r\n--选用 <%d> 模式--"%debug)
    time.sleep( 0.5 )

    print('\r\n--------------------------------------------')


#程序入库，主函数    
def main():
    log = strftime("%Y_%m_%d %H_%M_%S", localtime())
    log = "log/"+log + ".log"
    sys.stdout = Logger(log)                                           #加入日志

    print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    print('\r\n--------------------------------------------')
    print("名称：通道切换程序；\r\n作者：redmorningcn；\r\n版本：%s；"%version,)
    print("创建时间：2020/03/15；")
    print('\r\n--------------------------------------------')
    #sys.stdout = origin
    #f.close()
    try:
        getConfig()                                                 #取配置信息
    
        #print(pcPort,pcBaud)
        confTable   =  SwitchTable(path)                            #切换表
        config      =  {}                                           #配置字典

        pcInfo      =  PcComInfo()                                  #测试台信息结构体
        pcSer       =  PcComm(pcPort,pcBaud)                        #测试台串口对象
        t1          =  threading.Thread(target = pcSer.recvThread)  #创建多线程，运行串口接收任务
        t1.start()

        SwSer       =  MdMaster(swPort,swBaud)                      #创建切换装置对象

        ClearAllRelays(SwSer)                                       #开机清所有寄存器20
        
        lstnode1    = 1
        lstnode2    = 1
        pcSer.rcflg = 0
        
        
        print("\r\n-----------------开始运行<%d>----------------"%debug)
        while True:
            #print(".")
            time.sleep( 0.5 )

            #接收到信息测试台信息
            if  (pcSer.rcflg == 1) or (debug > 0):  #接收到信息(debug,调试模式)

                #取测试台通讯内容            
                pcInfo = pcSer.rcbuf        #取接收的信息
                if debug:
                    print("传感器序号:%d,电机转速:%d"%(pcInfo.sensor,pcInfo.rotate))
                pcSer.rcflg = 0             #结束标识清零
                
                if pcInfo.sensor < 255:
                    pcInfo.sensor += 1      #跳过序号0，所有序号加1             
                

                #调试模式
                if  debug == 1:             #传感器调试
                    try:
                        pcInfo.sensor = int(input("输入传感器编号："))
                        pcInfo.rotate = 0
                    except:
                        print("***输入信息有错")
                if  debug == 2:             #转速控制调试
                    pcInfo.sensor   = 1
                    try:
                        config['motor'] = int(input("输入电机编号："))
                        pcInfo.rotate   = int(input("输入转速："))
                    except:
                        print("***输入信息有错")
                    

                #根据配置表，切换通道
                if pcInfo.sensor == 255:
                    try:
                        ClearAllRelays(SwSer)   #清零所有寄存器
                    except Exception as e:
                        print("***配置寄存器清除异常---",e)
                else:
                    #根据传感器编号，读配置表信息
                    config = confTable.getConfig(pcInfo.sensor)
                    if debug:
                        print(config,len(config))
                
                    if len(config):  #配置表有效
                        #清前一次标识
                        SetRelays(SwSer,lstnode1,0)
                        SetRelays(SwSer,lstnode2,0)
                        print("\r\n---(%d)清除传感器上次配置完成---"%pcInfo.sensor)
                        
                        SetRelays(SwSer,config['node1'],config['value1'])
                        SetRelays(SwSer,config['node2'],config['value2'])

                        lstnode1 = config['node1']
                        lstnode2 = config['node2']
                        print("\r\n--------(%d)传感器切换完成--------"%pcInfo.sensor)
                        #根据配置表，设置电机
                        speed = int((pcInfo.rotate * 5) / 3 )       #速度换算
                        setSpeed(SwSer,config['motor'],speed % 3500)
                        print("\r\n----------电机设置完成------------")

                        print(strftime("%Y-%m-%d %H:%M:%S", localtime()))

                
    except Exception as e:
        print("***软件配置异常---",e)
        input("***按回车键继续----")

if __name__ == '__main__':
    main()



