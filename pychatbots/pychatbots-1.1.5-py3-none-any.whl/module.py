"""pychatbot.module是小懒猫推出的对话训练平台"""
import re, math 
from collections import Counter 
from difflib import SequenceMatcher

WORD = re.compile(r"([\u4e00-\u9fa5])")

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)


def higher(str1,str2):
     return SequenceMatcher(None,str1,str2).quick_ratio()

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])
     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)
     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

#计算余弦相似度
def compare(str1,str2):
    for i in '!,.?。！？':
         str1 = str1.replace(i,'')
         str2 = str2.replace(i,'')
    str1 = str(str1)
    str2 = str(str2)
    a = text_to_vector(str1)
    b = text_to_vector(str2)
    cosine = get_cosine(a,b)
    high = higher(str1,str2)/100
    q = cosine + high
    return q

class module():
    def train(self,g,filename,modulename,encoding):
        #导入库
        import pickle
        try:
            f = open(filename + str('.txt'),encoding=encoding)
        except:
            return 'error:文件不存在'
        try:
            w = f.readlines()
        except:
             return 'error:编码错误'
        f.close()
        i = 0
        q = 0
        dic = {}
        while True:
            try:
                #处理数据集
                s = w[i].split(g,2)
                s[2] = s[2].replace('\n','')
                s[2] = float(s[2])
                s[1] = s[1].split('#')
                #写入字典
                dic[int(q)] = s
                print(str(i+1) +'次'+ '/##########/100%')
                i = i+1
                q = i
            except:
                break
        #创建pkl文件
        with open(str(modulename)+ '.h6', 'wb') as fq:
            #存入pkl文件
            pickle.dump(dic, fq)
        #关闭文件
        fq.close()
        return 1
    def chat(self,qs,modulename):
        #导入库
        import pickle
        import random
        try:
            f = open(str(modulename) + '.h6','rb')
        except:
            return 'error:文件不存在'
        try:
            date = pickle.load(f)
        except:
             return 'error:文件为空'
        #关闭文件
        f.close()
        i = 0
        while True:
            if date.get(i)==None:
                return None
            if float(compare(date.get(i)[0],qs))>=float(date.get(i)[2]):
                #相似度比较
                return random.choice(date.get(i)[1])
            else:
                i = i+1
    def Best_train(self,g,filename,modulename,encoding):
        import pickle
        try:
             f = open(filename + str('.txt'),encoding=encoding)
        except:
            return 'error:文件不存在'
        try:
           w = f.readlines()
        except:
             return 'error:编码错误'
        f.close()
        i = 0
        q = 0
        dic = {}
        while True:
            try:
                #处理数据集
                s = w[i].split(g,1)
                s[1] = s[1].replace('\n','')
                s[1] = s[1].split('#')
                #写入字典
                dic[int(q)] = s
                print(str(i+1) +'次'+ '/##########/100%')
                i = i+1
                q = i
            except:
                break
        #创建pkl文件
        with open(str(modulename)+ '.h6', 'wb') as fq:
            #存入pkl文件
            pickle.dump(dic, fq)
        #关闭文件
        fq.close()
        return 1
    def Best_chat(self,qs,modulename):
        #导入库
        import pickle
        import random
        try:
            f = open(str(modulename) + '.h6','rb')
        except:
            return 'error:文件不存在'
        try:
            date = pickle.load(f)
        except:
             return 'error:文件为空'
        #关闭文件
        f.close()
        i = 0
        pare =[]
        qs = qs.replace(' ','')
        while True:
             if date.get(i)==None:
                s = max(pare)
                good = pare.index(s)
                if s<0.25:
                     return None
                if date.get(good)==None:
                     return None
                else:
                    return random.choice(date.get(good)[1])
             else:
                  a = date.get(i)[0]
                  aa = compare(qs,a)
                  pare.append(aa)
                  i = i+1
class bot():
     def __init__(self,botname):
          self.botname = botname
     def bot(self,qs,chu,Nonesay,modulename,again,tihuan):
          import pickle
          import time
          import random
          try:
               f = open(str(self.botname)+'.bot','rb')
               if isinstance(chu,str):
                    qs = qs.replace(chu,'')
               if isinstance(chu,list):
                    for i in chu:
                         qs = qs.replace(i,'')
               if not chu:
                    pass
               if not isinstance(chu,str) and not isinstance(chu,list):
                    return 'error:chu参数只支持列表(list)和字符串(str)'
               modules = module()
               adf = modules.Best_chat(qs,modulename)
               list1 = pickle.load(f)
               f.close()
               if adf==None:
                    if not Nonesay:
                         pass
                    else:
                         if isinstance(Nonesay,str):
                             f = open(str(self.botname)+'.bot','wb')
                             list1.append(qs)
                             list1.append(Nonesay)
                             list1.append(time.time())
                             pickle.dump(list1,f)
                             return Nonesay
                         if isinstance(Nonesay,list):
                             f = open(str(self.botname)+'.bot','wb')
                             d = random.choice(Nonesay)
                             list1.append(qs)
                             list1.append(d)
                             list1.append(time.time())
                             pickle.dump(list1,f)
                             return d
                         
                         else:
                              return 'error:Nonesay参数只支持列表(list)和字符串(str)'
               time1 = list1[2::3]
               q1 = list1[::3]
               a1 = list1[1::3]
               i = 0
               l = []
               while True:
                    try:
                        s = compare(qs,q1[i])
                        l.append(s)
                        i = i+1
                    except IndexError:
                         break
               k = max(l)
               ak = l.index(k)
               f = open(str(self.botname)+'.bot','wb')
               if k>0.8:
                    import time
                    times = time.localtime(time1[ak])[3]
                    import time
                    nowtime = time.localtime()[3]
                    h = nowtime - times
                    if h>=1:
                         list1.append(qs)
                         list1.append(adf)
                         list1.append(time.time())
                         pickle.dump(list1,f)
                         return adf
                    if h==0:
                         if tihuan==False or tihuan==None:
                             if again==None or again==False:
                                  pickle.dump(list1,f)
                                  return 'error:again与tihuan两项必须选一个'
                             else:
                                  for i in '.!。？！?':
                                       adf = adf.replace(i,'')
                                  if isinstance(again,list):
                                       adf = str(adf)  + str(random.choice(again))
                                       list1.append(qs)
                                       list1.append(adf)
                                       list1.append(time.time())
                                       pickle.dump(list1,f)
                                       return adf
                                  if isinstance(again,str):
                                       adf = str(adf)  + str(again)
                                       list1.append(qs)
                                       list1.append(adf)
                                       list1.append(time.time())
                                       pickle.dump(list1,f)
                                       return adf
                                  else:
                                        pickle.dump(list1,f)
                                        return 'error:again参数只支持列表(list)和字符串(str)'
                         else:
                              if isinstance(tihuan,str):
                                  adf = tihuan
                                  list1.append(qs)
                                  list1.append(adf)
                                  list1.append(time.time())
                                  pickle.dump(list1,f)
                                  return adf
                              if isinstance(tihuan,list):
                                  aq = random.choice(tihuan)
                                  list1.append(qs)
                                  list1.append(aq)
                                  list1.append(time.time())
                                  pickle.dump(list1,f)
                                  return aq
                              else:
                                   pickle.dump(list1,f)
                                   return 'error:tihuan参数只支持列表(list)和字符串(str)'
                    else:
                         list1.append(qs)
                         list1.append(adf)
                         list1.append(time.time())
                         pickle.dump(list1,f)
                         return adf
               else:
                    list1.append(qs)
                    list1.append(adf)
                    list1.append(time.time())
                    pickle.dump(list1,f)
                    return adf
          except (FileNotFoundError,EOFError):
               fs = open(str(self.botname)+'.bot','wb')
               modules = module()
               list1 = []
               a = modules.Best_chat(qs,modulename)
               if a==None:
                    if not Nonesay:
                         pass
                    else:
                         if isinstance(Nonesay,str):
                             list1.append(qs)
                             list1.append(Nonesay)
                             list1.append(time.time())
                             pickle.dump(list1,fs)
                             return Nonesay
                         if isinstance(Nonesay,list):
                             d = random.choice(Nonesay)
                             list1.append(qs)
                             list1.append(d)
                             list1.append(time.time())
                             pickle.dump(list1,fs)
                             return d
                         
                         else:
                              return 'error:Nonesay参数只支持列表(list)和字符串(str)'
               else:          
                    list1.append(qs)
                    list1.append(a)
                    list1.append(time.time())
                    pickle.dump(list1,fs)
                    return a
     def reset(self):
          f = open(str(self.botname) + '.bot','wb')
          return 'bot was reseted'
if __name__=="__main__":
  module = module()
