'''
函数：dec2bin16list(dec),将10进制数，转化为16位二进制list  
'''
def dec2bin16list(dec):
    vlist = []
    if 0 <= dec < 65536:             #数据在0
        for c in '{:016b}'.format(dec):
            vlist.append(int(c))

    return vlist

def dec2bin8list(dec):
    vlist = []
    if 0 <= dec < 256:             #数据在0
        for c in '{:08b}'.format(dec):
            vlist.append(int(c))

    return vlist


'''
while True:
    val = input("10进制转2进制列表：输入转换值：")
    print(val,int(val))
    print(dec2bin16_list(int(val)))
'''
