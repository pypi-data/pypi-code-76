#! /usr/bin/python
# coding:utf-8

'''
基于pymysql
1 数据库连接
2 数据库运行
2.1 select
2.2 非select
2.2.1 insert
2.2.2 非insert
3 数据库存储过程
4 数据库关闭连接
'''

import pymysql
from 配置 import 数据库配置

class 数据库:
    def __init__(self,配置=数据库配置):
        self.db = pymysql.connect(
            host=配置['地址'],
            user=配置['账号'],
            passwd=配置['密码'],
            db=配置['数据库'],
            port=配置['端口']
        )
        self.cs = self.db.cursor()
        print('数据库已连接:%s' % 配置['地址'])

    def 跑(self,脚本或存储过程名,脚本类型='查询',*存储过程参数):
        '''
        脚本类型
        1 select 需要返回结果
        2 存储过程
        3 其他 insert delete alter 需要commit
        '''
        if '查' in 脚本类型:
            self.cs.execute(脚本或存储过程名)
            self.__result = self.cs.fetchall()
            return self.__result 
        elif '存储过程' in 脚本类型:
            self.cs.callproc(脚本或存储过程名,存储过程参数)
            print('存储过程已跑:%s' % 脚本或存储过程名)
        else:
            self.cs.execute(脚本或存储过程名)
            self.db.commit()
            print('跑了')

    def 插(self,表名,数据,结束后关闭='是'):
        '''数据需要为嵌套可循环类型'''
        _kw  = ['%s' for i in range(len(数据[0]))]
        _sql = "insert into {表} values ({参数})".format(表=表名,参数=','.join(_kw))
        print('构造脚本:%s' % _sql)
        self.cs.executemany(_sql,数据)
        self.db.commit()
        print('已插入:%s' % 表名)
        if 结束后关闭 == '是':
            self.关闭()
        

    def 关闭(self):
        self.cs.close()
        self.db.close()
        print('数据库连接已关闭')

