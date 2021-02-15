## todo: unarchive


# from utils_ak.interactive_imports import *
# from qset_feature_store import *
#
#
# class BasicStreamingDatasetManager:
#     def __init__(self, datasets_dic):
#         self.datasets_dic = {}
#         for k, v in datasets_dic.items():
#             df = qdm.get_dataset(v)
#             self.datasets_dic[k] = df
#
#         self.datasets_dic = {k: self.crop(v) for k, v in self.datasets_dic.items()}
#
#     def crop(self, dataset):
#         raise NotImplemented()
#
#     def get_dataset(self, featureset, params=None, **kwargs):
#         return self.datasets_dic[featureset['name']].copy()
#
#     def add(self, key, obj):
#         if isinstance(obj, dict):
#             new_df = pd.DataFrame(obj['values'], index=obj['index'], columns=obj['columns'])
#         elif isinstance(obj, pd.DataFrame):
#             new_df = obj
#         else:
#             raise Exception('Unknown row object type')
#
#         self.datasets_dic[key] = pd.concat([self.datasets_dic[key], new_df])  #todo: optimize, do not copy
#         self.datasets_dic[key] = self.crop(self.datasets_dic[key])
#
#
# class FixedLengthStreamingDatasetManager(BasicStreamingDatasetManager):
#     def __init__(self, datasets_dic, length):
#         self.length = length
#         super().__init__(datasets_dic)
#
#     def crop(self, dataset):
#         return dataset.iloc[-self.length:]
#
#
# class FixedPeriodStreamingDatasetManager(BasicStreamingDatasetManager):
#     def __init__(self, datasets_dic, period):
#         self.period = cast_timedelta(period) # inclusive!
#         super().__init__(datasets_dic)
#
#     def crop(self, dataset):
#         last_index = dataset.index[-1]
#         return dataset.loc[cast_datetime(last_index) - self.period:]
#
#
# class StreamingDatasetManager:
#     def __init__(self, featureset, session_gap=2):
#         self.featureset = featureset
#         self.session_gap = session_gap
#
#         config = cast_featureset_model(featureset).get_inherited_config()
#
#         datasets_dic = {k: v for k, v in config.get('params', {}).items() if isinstance(v, ObjectId) and cast_featureset_model(v).is_dataset()}
#
#         self.sdm = FixedPeriodStreamingDatasetManager(datasets_dic=datasets_dic,
#                                                       period=timedelta(seconds=config['materialization']['lookback_seconds']))
#
#         self.wm = BasicWindowManager(lambda key: ProcessingSessionWindow(gap=self.session_gap))
#
#         # todo: hardcode (local_file hook)
#         self.dataset_manager = DatasetManager({'local_file': self.sdm})
#
#     def process(self):
#         values = self.wm.close_if_possible()  # {ts: {dataset_name: dataset_value}}
#         if not values:
#             return
#
#         values = sum([v for v in values.values()], [])  # flatten
#         df = pd.DataFrame(values)  # ts, dataset, row
#         df = df.sort_values(by='ts')
#
#         for ts, grp_ts in df.groupby('ts'):
#             # add values for each dataset
#             for dataset, grp_dataset in grp_ts.groupby('dataset'):
#                 new_df = pd.DataFrame(grp_dataset['row'].values.tolist())
#                 new_df.index = [cast_datetime(ts)] * len(new_df)
#                 new_df.index.name = 'startRange'
#                 self.sdm.add(dataset, new_df)
#
#             print(self.dataset_manager.get_dataset(self.featureset))
#
#     def add(self, ts, value):
#         self.wm.add(key=ts, value=value)
#
#
# def test1():
#     from qset_feature_store import QsetRepositoryClient
#     cli = QsetRepositoryClient('akadaner')
#     sqdm = FixedPeriodStreamingDatasetManager({'timebars': cli.get_latest(user='akadaner', name='timebars')}, timedelta(minutes=1))
#     print(sqdm.datasets_dic)
#
#
# if __name__ == '__main__':
#     from qset_feature_store import QsetRepositoryClient
#     cli = QsetRepositoryClient('akadaner')
#     featureset = cli.get_latest(user='akadaner', name='feature_set1')
#     sqdm = StreamingDatasetManager(featureset, session_gap=2)
#
#     sqdm.add(cast_ts(datetime.datetime.now()), {'ts': str(datetime.datetime.now()), 'dataset': 'timebars', 'row': {'ticker': 'XTZ-USDT', 'pHigh': random.uniform(2.2, 2.4), 'pLow': random.uniform(2.0, 2.2)}})
#     time.sleep(3)
#     sqdm.add(cast_ts(datetime.datetime.now()), {'ts': str(datetime.datetime.now()), 'dataset': 'timebars', 'row': {'ticker': 'XTZ-USDT', 'pHigh': random.uniform(2.2, 2.4), 'pLow': random.uniform(2.0, 2.2)}})
#     sqdm.process()