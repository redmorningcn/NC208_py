#作者：redmorningcn  20.03.02
#打开配置文件，将配置信息读入到列表
#
#包：SwitchTable
#包初始化：配置文件路径，例如：r"F:\cvi\app\NC208\NC208measureconfig.csv"
#方法：getConfig(self,num)，根据传感器编号num，获取配置信息列表。

import fileinput


#配置文件路径
path = r"NC208measureconfig.csv"

conf_list= []
#读取配置信息
def readConfigInfoFromFile(path):
    linenum = 0
    for line in fileinput.input(path):
        linenum += 1
        if linenum == 1:                    #第1行不处理
            continue
        else:
            #print("line is:",line)
            str = line.split(',')           #分割line
            #print(str)
            dict = {}
            dict['sensor']  = int(str[0])   #传感器编号
            dict['motor']   = int(str[1])   #电机编号
            dict['enble']   = int(str[2])   #启用标识，1，启用；0，禁用
            dict['tmp']     = int(str[3])   #备  用
            dict['node1']   = int(str[4])   #编号1
            dict['value1']  = int(str[5])   #值1
            dict['node2']   = int(str[6])   #编号2
            dict['value2']  = int(str[7])   #值2       
            #print(dict)
            conf_list.append(dict)

class SwitchTable(object):
    def __init__(self,path = r"NC208measureconfig.csv"):
        try:
            readConfigInfoFromFile(path)
        except Exception as e:
            print("---配置文件打开异常---:",e)

    def getConfig(self,num):                 #传感器编号
        for conf in conf_list:
            #print(conf)
            if conf.get('sensor') == num:
                return conf
    
        print("未找到对应的配置",num)
        return {}

'''
sonsor = SwitchTable(path)    
a = sonsor.getConfig(1)
print(a)
print("sensor = ",a['sensor'])
#readConfigInfoFromFile(path)
    
#print(conf_list)

'''
