import struct,math,time,datetime,threading,os
from concurrent.futures import as_completed, ProcessPoolExecutor
import pandas as pd
from wtafinance.tools.data_visualization import *
# 格式符        C语言类型	        Python类型	        Standard size
# x             pad byte(填充字节)	no value
# c	            char	            string of length 1	1
# b	            signed              char integer	    1
# B	            unsigned            char integer	    1
# ?	            _Bool	            bool	            1
# h	            short	            integer	            2
# H	            unsigned            short integer	    2
# i	            int	                integer	            4
# I(大写的i)	unsigned            int	integer	        4
# l(小写的L)	long	            integer	            4
# L	            unsigned long	    long	            4
# q	            long long	        long	            8
# Q	            unsigned long long	long	            8
# f	            float	            float	            4
# d	            double	            float	            8
# s	            char[]	            string
# p	            char[]	            string
# P	            void *	            long
class BaseFunc(object):
    def hex_to_int(self,h):
        i = int(h, 16)
        return i
    def int_to_hex(self,i):
        h = hex(i)
        return h

    def sum_str(self,data):
        s = ""
        for i in data:
            s += i
        return s

    def reverse_list(self,data):
        data.reverse()
        return data

    def timeatamp_to_format(self, timeStamp):
        # timearray = time.localtime(timeStamp)
        # res = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
        res = datetime.datetime.fromtimestamp(timeStamp)
        # if "00:00:00" in res:
        #     res = self.timeatamp_to_format(timeStamp+(3600*2))
        if res.hour==0:
            res = datetime.datetime.fromtimestamp(timeStamp+(3600*2))
        return res


    def timestr_to_timeatamp(self, timestr):
        if " " in timestr:
            data_sj = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")  # 定义格式
        else:
            data_sj = time.strptime(timestr, "%Y-%m-%d")  # 定义格式
        timeatamp = int(time.mktime(data_sj))
        return timeatamp


    def get_unicode_str(self,bytes):
        '''
        :param bytes: 字节列表
        :return:
        '''
        unicode_str_list = ['\\u'+self.sum_str(self.reverse_list(bytes[i:i+2])) for i in range(0,len(bytes),2)]
        return self.sum_str(unicode_str_list).encode('utf-8').decode("unicode_escape")

    def get_ascii_str(self,bytes):
        '''
        获取Ascii码对应字符串
        :param bytes:
        :return:
        '''
        return self.sum_str([chr(self.hex_to_int(i)) for i in bytes])



class ClassCodeConfig():
    config = [
        {
            "ClassCode": "1003",
            "ClassName": "非金融资产负债表",
            "TargetUnitCode": {'1003001': '证券简称', '1003002': '证券代码', '1003003': '机构名称', '1003004': '公告日期', '1003005': '截止日期',
                 '1003006': '报告年度', '1003007': '合并类型编码', '1003008': '合并类型', '1003009': '报表来源编码', '1003010': '报表来源',
                 '1003011': '货币资金', '1003012': '结算备付金', '1003013': '拆出资金',
                 '1003014': '以公允价值计量且其变动计入当期损益的金融资产(20190322弃用)',
                 '1003015': '衍生金融资产', '1003016': '应收票据', '1003017': '应收账款', '1003018': '预付款项', '1003019': '应收保费',
                 '1003020': '应收分保账款', '1003021': '应收分保合同准备金', '1003022': '其中：应收利息', '1003023': '其中：应收股利',
                 '1003024': '其他应收款', '1003025': '应收关联公司款', '1003026': '买入返售金融资产', '1003027': '存货',
                 '1003028': '其中：消耗性生物资产',
                 '1003029': '划分为持有待售的资产', '1003030': '发放贷款及垫款-流动资产', '1003031': '一年内到期的非流动资产', '1003032': '交易性金融资产',
                 '1003033': '应收票据及应收账款', '1003034': '合同资产', '1003035': '其他流动资产', '1003036': '流动资产合计',
                 '1003037': '发放贷款及垫款-非流动资产', '1003038': '可供出售金融资产', '1003039': '持有至到期投资', '1003040': '长期应收款',
                 '1003041': '长期股权投资', '1003042': '投资性房地产', '1003043': '固定资产', '1003044': '在建工程', '1003045': '工程物资',
                 '1003046': '固定资产清理', '1003047': '生产性生物资产', '1003048': '油气资产', '1003049': '无形资产', '1003050': '开发支出',
                 '1003051': '商誉', '1003052': '长期待摊费用', '1003053': '递延所得税资产', '1003054': '债权投资', '1003055': '其他债权投资',
                 '1003056': '其他权益工具投资', '1003057': '其他非流动金融资产', '1003058': '其他非流动资产', '1003059': '非流动资产合计',
                 '1003060': '资产总计', '1003061': '短期借款', '1003062': '向中央银行借款', '1003063': '吸收存款及同业存放', '1003064': '拆入资金',
                 '1003065': '以公允价值计量且其变动计入当期损益的金融负债（20190322弃用）', '1003066': '衍生金融负债', '1003067': '应付票据',
                 '1003068': '应付账款',
                 '1003069': '预收款项', '1003070': '卖出回购金融资产款', '1003071': '应付手续费及佣金', '1003072': '应付职工薪酬',
                 '1003073': '应交税费',
                 '1003074': '其中：应付利息', '1003075': '其中：应付股利', '1003076': '其他应付款', '1003077': '应付关联公司款',
                 '1003078': '应付分保账款',
                 '1003079': '保险合同准备金', '1003080': '代理买卖证券款', '1003081': '代理承销证券款', '1003082': '划分为持有待售的负债',
                 '1003083': '一年内到期的非流动负债', '1003084': '预计负债-流动负债', '1003085': '递延收益-流动负债', '1003086': '交易性金融负债',
                 '1003087': '应付票据及应付账款', '1003088': '合同负债', '1003089': '其他流动负债', '1003090': '流动负债合计', '1003091': '长期借款',
                 '1003092': '应付债券', '1003093': '其中：优先股-非流动负债', '1003094': '永续债-非流动负债', '1003095': '长期应付款',
                 '1003096': '长期应付职工薪酬', '1003097': '专项应付款', '1003098': '预计负债', '1003099': '递延收益-非流动负债',
                 '1003100': '递延所得税负债', '1003101': '其他非流动负债', '1003102': '非流动负债合计', '1003103': '负债合计',
                 '1003104': '实收资本（或股本）', '1003105': '其他权益工具', '1003106': '其中：优先股-所有者权益', '1003107': '永续债-所有者权益',
                 '1003108': '资本公积', '1003109': '减：库存股', '1003110': '其他综合收益', '1003111': '专项储备', '1003112': '盈余公积',
                 '1003113': '一般风险准备', '1003114': '未分配利润', '1003115': '外币报表折算价差', '1003116': '归属于母公司所有者权益',
                 '1003117': '少数股东权益', '1003118': '非正常经营项目收益调整', '1003119': '所有者权益（或股东权益）合计',
                 '1003120': '负债和所有者（或股东权益）合计',
                 '1003121': '备注', '1003122': '应收款项融资', '1003123': '使用权资产', '1003124': '租赁负债'}
        },
        {
            "ClassCode": "1002",
            "ClassName": "非金融现金表",
            "TargetUnitCode":{'1002001': '证券简称', '1002002': '证券代码', '1002003': '机构名称', '1002004': '公告日期', '1002005': '开始日期',
                 '1002006': '截止日期', '1002007': '报告年度', '1002008': '合并类型编码', '1002009': '合并类型', '1002010': '报表来源编码',
                 '1002011': '报表来源', '1002012': '销售商品、提供劳务收到的现金', '1002013': '客户存款和同业存放款项净增加额', '1002014': '向中央银行借款净增加额',
                 '1002015': '向其他金融机构拆入资金净增加额', '1002016': '收到原保险合同保费取得的现金', '1002017': '收到再保险业务现金净额',
                 '1002018': '保户储金及投资款净增加额', '1002019': '处置以公允价值计量且其变动计入当期损益的金融资产净增加额', '1002020': '收取利息、手续费及佣金的现金',
                 '1002021': '拆入资金净增加额', '1002022': '回购业务资金净增加额', '1002023': '收到的税费返还', '1002024': '收到其他与经营活动有关的现金',
                 '1002025': '经营活动现金流入小计', '1002026': '购买商品、接受劳务支付的现金', '1002027': '客户贷款及垫款净增加额',
                 '1002028': '存放中央银行和同业款项净增加额', '1002029': '支付原保险合同赔付款项的现金', '1002030': '支付利息、手续费及佣金的现金',
                 '1002031': '支付保单红利的现金', '1002032': '支付给职工以及为职工支付的现金', '1002033': '支付的各项税费',
                 '1002034': '支付其他与经营活动有关的现金', '1002035': '经营活动现金流出小计', '1002036': '经营活动产生的现金流量净额',
                 '1002037': '收回投资收到的现金', '1002038': '取得投资收益收到的现金', '1002039': '处置固定资产、无形资产和其他长期资产收回的现金净额',
                 '1002040': '处置子公司及其他营业单位收到的现金净额', '1002041': '收到其他与投资活动有关的现金', '1002042': '投资活动现金流入小计',
                 '1002043': '购建固定资产、无形资产和其他长期资产支付的现金', '1002044': '投资支付的现金', '1002045': '质押贷款净增加额',
                 '1002046': '取得子公司及其他营业单位支付的现金净额', '1002047': '支付其他与投资活动有关的现金', '1002048': '投资活动现金流出小计',
                 '1002049': '投资活动产生的现金流量净额', '1002050': '吸收投资收到的现金', '1002051': '其中：子公司吸收少数股东投资收到的现金',
                 '1002052': '取得借款收到的现金', '1002053': '发行债券收到的现金', '1002054': '收到其他与筹资活动有关的现金', '1002055': '筹资活动现金流入小计',
                 '1002056': '偿还债务支付的现金', '1002057': '分配股利、利润或偿付利息支付的现金', '1002058': '其中：子公司支付给少数股东的股利、利润',
                 '1002059': '支付其他与筹资活动有关的现金', '1002060': '筹资活动现金流出小计', '1002061': '筹资活动产生的现金流量净额',
                 '1002062': '四、汇率变动对现金的影响', '1002063': '四(2)、其他原因对现金的影响', '1002064': '五、现金及现金等价物净增加额',
                 '1002065': '期初现金及现金等价物余额', '1002066': '期末现金及现金等价物余额', '1002067': '净利润', '1002068': '加：资产减值准备',
                 '1002069': '固定资产折旧、油气资产折耗、生产性生物资产折旧', '1002070': '投资性房地产的折旧及摊销', '1002071': '无形资产摊销',
                 '1002072': '长期待摊费用摊销', '1002073': '处置固定资产、无形资产和其他长期资产的损失', '1002074': '固定资产报废损失',
                 '1002075': '公允价值变动损失', '1002076': '财务费用', '1002077': '投资损失', '1002078': '递延所得税资产减少',
                 '1002079': '递延所得税负债增加', '1002080': '存货的减少', '1002081': '经营性应收项目的减少', '1002082': '经营性应付项目的增加',
                 '1002083': '其他', '1002084': '经营活动产生的现金流量净额2', '1002085': '债务转为资本', '1002086': '一年内到期的可转换公司债券',
                 '1002087': '融资租入固定资产', '1002088': '现金的期末余额', '1002089': '减：现金的期初余额', '1002090': '加：现金等价物的期末余额',
                 '1002091': '减：现金等价物的期初余额', '1002092': '加：其他原因对现金的影响2', '1002093': '现金及现金等价物净增加额2'}
        },
        {
            "ClassCode": "1001",
            "ClassName": "非金融利润表",
            "TargetUnitCode":{'1001001': '证券代码', '1001002': '证券简称', '1001003': '机构名称', '1001004': '公告日期', '1001005': '开始日期',
                 '1001006': '截止日期', '1001007': '报告年度', '1001008': '合并类型编码', '1001009': '合并类型', '1001010': '报表来源编码',
                 '1001011': '报表来源', '1001012': '一、营业总收入', '1001013': '其中：营业收入', '1001014': '利息收入', '1001015': '已赚保费',
                 '1001016': '手续费及佣金收入', '1001017': '二、营业总成本', '1001018': '其中：营业成本', '1001019': '利息支出',
                 '1001020': '手续费及佣金支出', '1001021': '退保金', '1001022': '赔付支出净额', '1001023': '提取保险合同准备金净额',
                 '1001024': '保单红利支出', '1001025': '分保费用', '1001026': '营业税金及附加', '1001027': '销售费用', '1001028': '管理费用',
                 '1001029': '勘探费用', '1001030': '财务费用', '1001031': '研发费用', '1001032': '资产减值损失', '1001033': '加：公允价值变动净收益',
                 '1001034': '投资收益', '1001035': '其中：对联营企业和合营企业的投资收益', '1001036': '汇兑收益', '1001037': '其它收入',
                 '1001038': '信用减值损失', '1001039': '净敞口套期收益', '1001040': '资产处置收益', '1001041': '影响营业利润的其他科目',
                 '1001042': '三、营业利润', '1001043': '加：补贴收入', '1001044': '营业外收入', '1001045': '其中：非流动资产处置利得',
                 '1001046': '减：营业外支出', '1001047': '其中：非流动资产处置损失', '1001048': '加：影响利润总额的其他科目', '1001049': '四、利润总额',
                 '1001050': '减：所得税', '1001051': '加：影响净利润的其他科目', '1001052': '五、净利润', '1001053': '持续经营净利润',
                 '1001054': '终止经营净利润', '1001055': '归属于母公司所有者的净利润', '1001056': '少数股东损益', '1001057': '（一）基本每股收益',
                 '1001058': '（二）稀释每股收益', '1001059': '七、其他综合收益', '1001060': '八、综合收益总额', '1001061': '其中：归属于母公司',
                 '1001062': '其中：归属于少数股东', '1001063': '备注', '1001064': '其中：利息费用', '1001065': '其中：利息收入',
                 '1001066': '信用减值损失（2019格式）', '1001067': '资产减值损失（2019格式）'}
        },
        {
            "ClassCode": "1007",
            "ClassName": "历史行情",
            "TargetUnitCode": {'1007001': 'data', '1007002': 'high', '1007003': 'vol2', '1007004': 'open', '1007005': 'low',
                 '1007006': 'turnover', '1007007': 'Amplitude', '1007008': 'p_change', '1007009': 'close', '1007010': 'date',
                 '1007011': 'volume', '1007012': 'name', '1007013': 'code', '1007014': 'fqt', '1007015': 'type',
                 '1007016': 'is_dapan'}
        }
        ,
        {
            "ClassCode": "1008",
            "ClassName": "五分钟数据",
            "TargetUnitCode": {'1008004': 'high', '1008007': 'vol2', '1008002': 'open', '1008005': 'low', '1008008': 'turnover'
                , '1008009': 'Amplitude', '1008010': 'p_change', '1008003': 'close', '1008001': 'date', '1008006': 'volume'}
        }
    ]


class TargetUnit(object):
    def __init__(self, code, unit, digit, storage_type,base_class_code):
        '''
        指标实例化
        :param code: 指标代码
        :param unit: 货币单位
        :param digit: 数值位数
        '''
        self.code = str(code)
        self.base_class_code = base_class_code
        self.name = [i["TargetUnitCode"][self.code] for i in ClassCodeConfig.config if i["ClassCode"] == self.base_class_code][0]
        self.unit = unit
        self.digit = digit
        self.storage_type = storage_type
        # print("指标代码：",self.code)
        # print("指标单位：",self.unit)
        # print("指标位数：",self.digit)


class FileHead(object):
    '''
    文件头
    '''
    def __init__(self,sec_code,sec_name,market,flag,class_count,class_subset):
        '''
        初始化文件头部参数
        :param sec_code: 股票代码
        :param sec_name: 股票简称
        :param market: 市场
        :param flag: 股票自定义标识
        :param class_count: 大类个数
        :param class_subset: 大类子集
        '''
        self.sec_code = sec_code
        self.sec_name = sec_name
        self.market = market
        self.flag = flag
        self.class_count = class_count
        self.class_subset:list = class_subset


class ClassHead(BaseFunc):
    '''
    大类头部
    '''
    def __init__(self,class_head_hexs):
        self.code, = struct.unpack("I", bytes.fromhex(self.sum_str(class_head_hexs[:4]))) # 大类代码
        self.code = str(self.code)
        self.name = [i for i in ClassCodeConfig.config if i["ClassCode"] == self.code][0]["ClassName"]
        self.target_count, = struct.unpack("I", bytes.fromhex(self.sum_str(class_head_hexs[4:8])))   # 指标个数
        self.DataLen, = struct.unpack("H", bytes.fromhex(self.sum_str(class_head_hexs[8:10]))) # 数据长度
        self.latest_time, = struct.unpack("I", bytes.fromhex(self.sum_str(class_head_hexs[10:14])))   # 指标最新时间
        self.latest_time = self.timeatamp_to_format(self.latest_time)
        self.target_subset = []
        # print("大类：",self.code)
        for i in range(self.target_count):
            limit = i*21
            target_code, = struct.unpack("q", bytes.fromhex(self.sum_str(class_head_hexs[14+limit:22+limit])))
            target_unit = self.get_unicode_str(class_head_hexs[22+limit:26+limit])
            target_digit, = struct.unpack("q", bytes.fromhex(self.sum_str(class_head_hexs[26+limit:34+limit])))
            target_storage_type = self.get_ascii_str(class_head_hexs[34+limit:35+limit])
            self.target_subset.append(TargetUnit(target_code, target_unit, target_digit, target_storage_type,self.code))


class ClassUnit(BaseFunc):
    def __init__(self,class_code,class_start_address,class_head_hexs=None,class_body_hexs=None):
        '''
        初始化大类
        :param class_code: 大类编码
        :param class_start_address: 大类起始地址
        :param class_head_hexs: 大类头部内容
        :param class_body_hexs: 大类数据内容
        '''
        self.class_code = str(class_code)
        self.class_target_code_conf = [i for i in ClassCodeConfig.config if i["ClassCode"] == self.class_code][0]["TargetUnitCode"]
        self.class_name = [i for i in ClassCodeConfig.config if i["ClassCode"] == self.class_code][0]["ClassName"]
        self.class_start_address = class_start_address
        self.class_head_hexs = class_head_hexs
        self.class_body_hexs = class_body_hexs
        self.class_head: ClassHead = None  # 大类头部内容
        self.class_body: pd.DataFrame = None  # 大类数据内容

    def init_class_data(self,limit):
        columns = [self.class_target_code_conf[str(target.code)] for target in self.class_head.target_subset]
        columns.insert(0, "time")
        # data = [self.class_body_hexs[i:i+limit] for i in range(0, len(self.class_body_hexs), limit) if self.class_body_hexs[i:i+limit][:8]]
        data = []
        # 循环每一行
        for i in range(0, len(self.class_body_hexs), limit):
            # 判断是否为最后一条数据
            if struct.unpack('q', bytes.fromhex(self.sum_str(self.class_body_hexs[i:i + limit][:8])))[0] == 0:
                break
            # 把每一行的数据加入到一个列表
            data.append(self.class_body_hexs[i:i+limit])

        for data_index in range(len(data)):
            #  解析字段数据
            # data[data_index] = [struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][i:i+8])))[0]
            #                     if i == 0
            #                     else
            #                     struct.unpack(self.class_head.target_subset[int(i/8)-1].storage_type, bytes.fromhex(self.sum_str(data[data_index][i:i+8])))[0]
            #                     for i in range(0, len(data[data_index]), 8)
            #                     if int(i / 8) - 1 < self.class_head.target_count]
            l = [struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][0:8])))[0]]
            for i in range(0,self.class_head.target_count):
                item = self.class_head.target_subset[i]
                if item.storage_type == "q":
                    l.append(struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][i*8+8:i*8 + 16])))[0])
                elif item.storage_type == "T":
                    l.append(self.timeatamp_to_format(struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][i * 8+8:i * 8 + 16])))[0]))
                else:
                    l.append(struct.unpack("d",bytes.fromhex(self.sum_str(data[data_index][i*8+8:i*8 + 16])))[0])
            # for i in range(0, len(data[data_index]), 8):
            #     if int(i / 8)-1 == self.class_head.target_count:
            #         break
            #     elif i==0:
            #         l.append(struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][i:i + 8])))[0])
            #     elif self.class_head.target_subset[int(i / 8)].storage_type=="T":
            #         l.append(struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][i:i + 8])))[0])
            #     elif self.class_head.target_subset[int(i / 8)].storage_type=="d":
            #         l.append(struct.unpack(self.class_head.target_subset[int(i / 8)].storage_type,
            #                                bytes.fromhex(self.sum_str(data[data_index][i:i + 8])))[0])
            data[data_index] = l
        self.class_body = pd.DataFrame(data, columns=columns)


class DataSource(BaseFunc):
    def __init__(self):
        self.file_head:FileHead = None
        self.file_body = dict()

    # 初始化头部
    def init_head(self, head_data):
        '''
        初始化文件头部
        :param data:
        :return:
        '''
        sec_code = str(struct.unpack("q", bytes.fromhex(self.sum_str(head_data[:8])))[0]).zfill(6)
        sec_name = self.get_unicode_str(head_data[8:24])
        market = self.get_ascii_str(head_data[24:26])
        flag = bool(struct.unpack("h", bytes.fromhex(self.sum_str(head_data[26:28])))[0])
        class_count, = struct.unpack("I", bytes.fromhex(self.sum_str(head_data[28:32])))
        class_subset = []
        for i in range(class_count):
            limit = i*12
            class_code, = struct.unpack("I", bytes.fromhex(self.sum_str(head_data[32+limit:36+limit])))
            class_start_address, = struct.unpack("q", bytes.fromhex(self.sum_str(head_data[36+limit:44+limit])))
            class_subset.append(ClassUnit(class_code,class_start_address))
        # market, flag, class_count, class_subset
        # 实例化头部类
        self.file_head = FileHead(sec_code=sec_code, sec_name=sec_name, market=market, flag=flag,
                                  class_count=class_count, class_subset=class_subset)

    #初始化内容
    def init_body(self, body_data):
        i = 0
        for classUnit in self.file_head.class_subset:
            limit = (8*200*4*50+6400)*i
            body_len = 8*200*4*50
            if self.file_head.class_count==1:
                body_len = len(body_data)
            classUnit.class_head_hexs = body_data[0+limit:6400+limit]
            classUnit.class_body_hexs = body_data[6400+limit:body_len+limit]
            classUnit.class_head = ClassHead(classUnit.class_head_hexs)
            classUnit.init_class_data(classUnit.class_head.DataLen)
            self.file_body[str(classUnit.class_head.code)] = classUnit.class_body
            i += 1

    def search_data(self, start,end,class_code):
        res_data = pd.DataFrame()
        if len(self.file_body.keys()) == 0:
            return res_data

        if class_code is None:
            for key in self.file_body.keys():
                res_data = self.file_body[key]
        else:
            res_data = self.file_body[class_code]
        start_time=start
        end_time=end
        if start_time is not None:
            start_time = self.timestr_to_timeatamp(start_time)
            res_data = res_data.loc[res_data["time"]>=start_time]
        if end_time is not None and end_time!='':
            end_time = self.timestr_to_timeatamp(end_time)
            res_data = res_data.loc[res_data["time"] <= end_time]
        res_data.drop(['time'],axis=1,inplace=True)
        return res_data.reset_index(drop=True)

    # def search_data(self, param):
    #     res_data = {}
    #     date_time = param["date_time"]
    #     class_list = param["param_data"]["classList"]
    #     class_list = [{"code": str(class_.class_code), "field": "*"} for class_ in self.file_head.class_subset] if class_list == "*" else class_list
    #     for class_ in class_list:
    #         field_code_conf = [i for i in ClassCodeConfig.config if i["ClassCode"] == class_["code"]][0]["TargetUnitCode"]
    #         if class_["code"] in self.file_body.keys():
    #             res_data[class_["code"]] = self.file_body[class_["code"]]
    #         else:
    #             res_data[class_["code"]] = []
    #             continue
    #         if date_time is not None:
    #             start_time = date_time["startTime"] if "startTime" in date_time.keys() else None
    #             end_time = date_time["endTime"] if "endTime" in date_time.keys() else None
    #             if start_time is not None:
    #                 start_time = self.timestr_to_timeatamp(start_time)
    #                 res_data[class_["code"]] = res_data[class_["code"]].loc[res_data[class_["code"]]["time"]>=start_time]
    #             if end_time is not None:
    #                 end_time = self.timestr_to_timeatamp(end_time)
    #                 res_data[class_["code"]] = res_data[class_["code"]].loc[res_data[class_["code"]]["time"] <= end_time]
    #         if class_["field"] != "*":
    #             field_list = [field_code_conf[str(i)] for i in class_["field"]]
    #             if "time" not in field_list:
    #                 field_list.insert(0,"time")
    #             res_data[class_["code"]] = res_data[class_["code"]][field_list]
    #         if "time" in res_data[class_["code"]].columns.values.tolist():
    #             res_data[class_["code"]]["time"]=res_data[class_["code"]]["time"].apply(self.timeatamp_to_format)
    #
    #     return res_data

    def read_file(self, path):
        '''
        文件读取
        :param path: 路径
        :return:
        '''
        try:
            total_list = []
            with open(path,'rb') as f:
                s = f.read(1024)
                while s:
                    # byte = ord(s)
                    # total_list.append('%02x' % (byte))
                    total_list += ['%02x' % (i) for i in s]
                    s = f.read(1024)

            self.init_head(total_list[:1024])
            self.init_body(total_list[1024:])
        except IOError as e:
            raise Exception("目标文件夹没有该文件,可能是参数传递错误,路径为："+path)

class MainClass():
    def __init__(self, RootPath,PoolSize = 3):
        self.PoolSize = PoolSize
        self.RootPath = os.path.join(RootPath,"System")
        self.day_fqt= {  # 日数据
                "0": "dat",
                "1": "ldat",
                "2": "rdat",
            }
        self.fzline_fqt={
                "0": "fat",
                "1": "lfat",
                "2": "rfat",
            }
        self.finance_fqt={
                "0":"fin"
            }

    def _do_something_data(self,file_path,start,end,class_code=None):
        data_source = DataSource()
        data_source.read_file(file_path)
        return data_source.search_data(start,end,class_code)

    def _get_market(self,code):
        return "SH" if code[0] == "6" else "SZ"

    def _get_data_path(self,data_type,ktype,fqt,code):
        '''
        获取资源路径
        :param data_type: [INDEX,SH,SZ]
        :param ktype: [day,5,finance]
        :param fqt:
        :return:
        '''
        day_path ={
            "path":"day",
            "suffix":self.day_fqt
        }
        fzline_path = {
            "path": "fzline", # 五分钟
            "suffix": self.fzline_fqt
        }
        finance_path={
            "path": "finance",  # 三大财报
            "suffix":self.finance_fqt
        }
        data_path_dict = {
            "INDEX":{
                "path":"INDEX",
                "D":day_path,
                "5":fzline_path
            },
            "SH":{
                "path": "SH",
                "D":day_path,
                "5":fzline_path,
                "finance":finance_path
            },
            "SZ":{
                "path": "SZ",
                "D":day_path,
                "5":fzline_path,
                "finance":finance_path
            }
        }
        path_1 = data_path_dict[data_type]
        path_2 = path_1[ktype]
        path_3 = path_2["suffix"]
        return os.path.join(self.RootPath,path_1["path"],path_2["path"],code+'.'+path_3[fqt])

    def get_hist_data(self,code,start,end='',fqt="0",ktype='D'):
        '''行情数据'''
        data_type = self._get_market(code)
        file_path = self._get_data_path(data_type,ktype,fqt,code)
        return self._do_something_data(file_path,start,end)

    def income(self, code, start, end=''):
        '''
        非金融利润表数据
        :param code:
        :param start:
        :param end:
        :return:
        '''
        data_type = self._get_market(code)
        file_path = self._get_data_path(data_type, "finance", "0", code)
        return self._do_something_data(file_path, start, end,"1001")

    def cashflow(self, code, start, end=''):
        '''
        非金融现金表数据
        :param code:
        :param start:
        :param end:
        :return:
        '''
        data_type = self._get_market(code)
        file_path = self._get_data_path(data_type, "finance", "0", code)
        return self._do_something_data(file_path, start, end, "1002")

    def balancesheet(self, code, start, end=''):
        '''
        非金融资产负债表数据
        :param code:
        :param start:
        :param end:
        :return:
        '''
        data_type = self._get_market(code)
        file_path = self._get_data_path(data_type, "finance", "0", code)
        return self._do_something_data(file_path, start, end, "1003")

    def get_index(self, code,start,end='',fqt="0",ktype='D'):
        '''
        指数数据
        :param code:
        :param start:
        :param end:
        :return:
        '''
        file_path = self._get_data_path("INDEX", ktype, fqt, code)
        return self._do_something_data(file_path, start, end)

    def get_stockIndex_data(self,code,base_code,start,end='',fqt="0",ktype='D',bFillNA=False):
        k_data = self.get_hist_data(code,start,end,fqt,ktype)
        index_data = self.get_index(base_code,start,end,fqt,ktype)
        base_stock_data = index_data.loc[:, ['date', 'close']]
        base_stock_data.rename(columns={'close': 'base_close'}, inplace=True)

        result = pd.concat([k_data.set_index('date'), base_stock_data.set_index('date')], axis=1).reset_index()

        if (bFillNA):
            result = result.fillna(axis=0, method='ffill')

        result = result.dropna(axis=0, how='any')
        result.reset_index(drop=True, inplace=True)
        result.rename(columns={'index': 'date'}, inplace=True)
        if (len(result) <= 0):
            return pd.DataFrame()
        return result

if __name__ == '__main__':
    # code_list = ["000001.sz","000002.sz","000004.sz","000005.sz","000006.sz","000007.sz","000008.sz","000009.sz",
    #              "000010.sz","000011.sz","000012.sz","000014.sz","000016.sz","000017.sz","000018.sz","000019.sz",
    #              "000020.sz","000021.sz","000023.sz","000024.sz","000025.sz","000026.sz","000027.sz","000028.sz"]
    code_list = ["000001"]
    mainclass= MainClass(r"D:\tby_svn\wta_finance\trunk\2 项目实施阶段\2.4 系统开发\2.4.1 系统实现\WtaFinancePlatform\WtaFinancePlatform_WPF\bin\x86\Debug\Data")
    System = {
        "classList":"*"
        #     [
        #     {
        #         "code": "1007",  # 大类编码
        #         "field": ["1007002","1007003","1007004"] #"*"  # "*"表示所有
        #     }
        # ]
    }
    date_time={
        "startTime": "2015-01-01 00:00:00",
        "endTime": "2021-01-01 00:00:00"
    }
    s = time.time()
    res_data = mainclass.get_data(code_list, fqt='2',date_time=None,system=None,custom=System)
    e = time.time()
    print(res_data)
    print(e-s)


