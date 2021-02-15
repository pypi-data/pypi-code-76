# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qset_feature_store',
 'qset_feature_store.archive',
 'qset_feature_store.archive.dataset_manager',
 'qset_feature_store.archive.worker',
 'qset_feature_store.archive.worker.dataset',
 'qset_feature_store.controller',
 'qset_feature_store.featureset_engine',
 'qset_feature_store.featureset_engine.dataset_manager',
 'qset_feature_store.repository']

package_data = \
{'': ['*'],
 'qset_feature_store.featureset_engine': ['dataset_manager/data/local/6026716f1ae81052b43a9818/*',
                                          'dataset_manager/data/local/6026721a87f650a55707dfdb/*',
                                          'dataset_manager/data/local/60267e93e653a081d4e5456e/*',
                                          'dataset_manager/data/local/602a170a9d5e0dd1173f7956/*',
                                          'dataset_manager/data/local/602a17284e0f5bc2e64031d2/*',
                                          'dataset_manager/data/local/602a1749ec11cc0d869773dd/*',
                                          'dataset_manager/data/local/602a18b5d359dc90e893dddf/*',
                                          'dataset_manager/data/local/602a19077cd15c8858ac48dd/*',
                                          'dataset_manager/data/local/602a190c82e20d0e7896a40e/*',
                                          'dataset_manager/data/local/602a1c22827b0e4bd50a0d92/*',
                                          'dataset_manager/data/local/602a1c540626c6fcb56b0f82/*',
                                          'dataset_manager/data/local/602a1c6c53e6aa1620d4fe38/*',
                                          'dataset_manager/data/local/602a1c78c07ce140072ce287/*',
                                          'dataset_manager/data/local/602a1c8de4f2329deae0ab9c/*',
                                          'dataset_manager/data/local/602a1c9ad74fc7857d22b316/*',
                                          'dataset_manager/data/local/602a1cdef42338b9b07816c7/*',
                                          'dataset_manager/data/local/602a1cf2ca38d994f8054fde/*',
                                          'dataset_manager/data/local/602a1d08b73b600289fb0384/*',
                                          'dataset_manager/data/local/602a1d1ee401c348f08eb2c6/*',
                                          'dataset_manager/data/local/602a1d25b63b29352f27bb98/*',
                                          'dataset_manager/data/local/602a1eff8b062bf201d65e9b/*',
                                          'dataset_manager/data/local/602a2fdfff1a6476d0374458/*',
                                          'dataset_manager/data/local/602a2fe6987698907accae8e/*',
                                          'dataset_manager/data/local/binance/6024fd64f2ca39cea598e399/*',
                                          'dataset_manager/data/local/binance/602512fc6b2eb3031fa883b8/*',
                                          'dataset_manager/data/local/binance/6025152e76442bb46c82a129/*',
                                          'dataset_manager/data/local/binance/602524ad96fa8f4c4ea94dbf/*',
                                          'dataset_manager/data/local/binance/602524d1dd67effe309c2a25/*',
                                          'dataset_manager/data/local/binance/602524e36f32a6ab7bfb526d/*',
                                          'dataset_manager/data/local/binance/6025255f76b11d190d87b624/*',
                                          'dataset_manager/data/local/binance/60252577681f7b4e87e72847/*',
                                          'dataset_manager/data/local/binance/60252584db4dad5a6c2cdbb3/*',
                                          'dataset_manager/data/local/binance/6025258b3261851e6fb1f6bb/*',
                                          'dataset_manager/data/local/binance/602525a6b179830bebd173ba/*',
                                          'dataset_manager/data/local/binance/602525ade235cbb1ed304760/*',
                                          'dataset_manager/data/local/binance/60267f50ba8ff2704b3a859a/*',
                                          'dataset_manager/data/local/binance/60267f8f7f46bb76f2133f66/*',
                                          'dataset_manager/data/local/binance/60267fe33a3bbc099730f023/*',
                                          'dataset_manager/data/local/binance/60268009ef38f9d2bdb48c76/*',
                                          'dataset_manager/data/local/binance/6026805c0a38520ab0bd61de/*',
                                          'dataset_manager/data/local/binance/602680e0e88e185a147ce393/*',
                                          'dataset_manager/data/local/binance/602680fd1b846353f619ffca/*',
                                          'dataset_manager/data/local/binance/6026813ccb5670a4bbb50523/*',
                                          'dataset_manager/data/local/binance/602681524ddf3907c5c95877/*',
                                          'dataset_manager/data/local/binance/6026817cfb1aae4e22b7b34b/*',
                                          'dataset_manager/data/local/binance/602681857d8b83e4a26e4af7/*',
                                          'dataset_manager/data/local/default/60267fbaaf52325147eafffa/*']}

install_requires = \
['utils-ak>=0.1.5,<0.2.0']

setup_kwargs = {
    'name': 'test-qset-feature-store',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Arsenii Kadaner',
    'author_email': 'arseniikadaner@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
