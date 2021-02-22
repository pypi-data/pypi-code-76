# coding:utf-8
# author caturbhuja
# date   2020/11/4 3:49 下午 
# wechat chending2012 


class MysqlMixin:
    """
    此类中均为伪方法，仅仅为了提供IDE的提示功能
    """
    # ---------------------------- Mysql ---------------------------------
    # Mysql 更多方法，请看
    #
    # --------------------------------------------------------------------
    def cursor(self):
        """获取游标"""

    def query(self, query, *parameters, **kwparameters) -> (dict, list):
        """执行语句，获取结果
        Returns a row list for the given query and parameters.
        """

    def execute(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""

    def iter(self, query, *parameters, **kwparameters) -> iter:
        """Returns an iterator for the given query and parameters."""

    def close(self):
        """关闭连接"""
