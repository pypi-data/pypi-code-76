# coding:utf-8
# author caturbhuja
# date   2020/11/4 3:49 下午 
# wechat chending2012 


class KafkaMixin:
    """
    此类中均为伪方法，仅仅为了提供IDE的提示功能
    """
    # ---------------------------- common ---------------------------------
    # common 更多方法，请看
    #
    # --------------------------------------------------------------------
    def close(self):
        """"""

    # ---------------------------- consumer ---------------------------------
    # consumer 更多方法，请看 KafkaConsumer
    # from kafka import KafkaConsumer
    # --------------------------------------------------------------------
    def assign(self, partition):
        """设置consumer的partition"""

    def get_position(self, partition):
        """获取该 partition 的位置"""

    def get_partitions(self, topic=None):
        """获取该topic的partition，如果初始化参数包含topic，则可以不用传入"""

    def get_messages(self, timeout_ms=5000, max_records=1000, value_type='tuple', decode=False):
        """拉取kafka消息"""

    def commit(self, offsets=None):
        """提交 offsets"""

    # ---------------------------- producer ---------------------------------
    # producer 更多方法，请看 KafkaProducer
    # from kafka import KafkaProducer
    # --------------------------------------------------------------------
    def flush(self, timeout=None):
        """推动所有数据"""

    def send(self, value: (bytes, str, dict, list, tuple), key=None, partition=None, topic=None, auto_flush=True):
        """往kafka发送数据"""

    def send_many(self, data: iter, partition=None, topic=None, auto_flush=True):
        """往kafka 一次性发送很多数据"""






