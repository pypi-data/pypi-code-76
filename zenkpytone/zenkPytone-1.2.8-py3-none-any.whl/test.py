import kintone
from pprint import pprint

kintone = kintone.Kintone(authText='WkVOS1N5czpEM1ZLZTVWd2E4', domain='zenk', app=1677)

where = '工番 = "20XR260"'
order = 'order by 工番 desc'
records = kintone.selectRec(182549)
pprint(records)