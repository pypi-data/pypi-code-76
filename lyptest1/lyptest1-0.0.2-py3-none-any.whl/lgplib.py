import base64
import os
class lgplib():
    def Base_64(self,PATH,IMGNAME):
        file_path = os.path.join(PATH,IMGNAME) #获取base_dir+'/image'文件夹内的文件
        f=open(file_path,'rb') #二进制方式打开图文件
        lsReadImage_f=base64.b64encode(f.read())#读取文件内容，转换为base64编码
        f.close()#关闭文件
        return "0.0.5"+str(lsReadImage_f)