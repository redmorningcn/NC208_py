
import configparser
import os

class ReadConfig:
    """定义一个读取配置文件的类"""

    def __init__(self, filepath=None):
        if filepath:
            configpath = filepath
        else:
            #root_dir = os.path.dirname(os.path.abspath('.'))
            root_dir = os.getcwd()
            configpath = os.path.join(root_dir, "config.ini")
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath)

    def File(self, param):
        root_dir = os.getcwd()
        value = self.cf.get("File", param)
        value = os.path.join(root_dir, value)
        return value
    def PcSer(self, param):
        value = self.cf.get("PC-COM", param)
        return value
    def SwSer(self, param):
        value = self.cf.get("SW-COM", param)
        return value
    def Debug(self, param):
        value = self.cf.get("Debug", param)
        return value

'''
if __name__ == '__main__':
    test = ReadConfig()
    t = test.File("path")
    print(t)
    t = test.PcSer("port")
    print(t)
    t = test.PcSer("baud")
    print(t)

    t = test.SwSer("port")
    print(t)
    t = test.SwSer("baud")
    print(t)
'''
