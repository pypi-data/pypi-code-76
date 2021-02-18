# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deeqnlpy',
 'deeqnlpy.lib.baikal',
 'deeqnlpy.lib.baikal.language',
 'deeqnlpy.lib.google.api']

package_data = \
{'': ['*']}

install_requires = \
['grpcio==1.35.0', 'protobuf==3.14.0']

setup_kwargs = {
    'name': 'deeqnlpy',
    'version': '0.9.2',
    'description': 'The deeq nlp python client library',
    'long_description': '# What is this?\n\n`deeqnlpy` is the python 3 library for deeq NLP.\n\nDeeq(pronounce as deeque) NLP is a Korean NLP,\nwhich provides tokenizing, POS tagging for Korean.\n\n## How to install\n\n```shell\npip3 install deeqnlpy\n```\n\n## How to get deeq NLP\n- Click [this form](https://docs.google.com/forms/d/e/1FAIpQLSfSJQCMwm0pS1nJiirwUNjfj-7jT-T_CLUfgMc-vTpRbHZZnw/viewform)\n- Fill it.\n- Get emailed download link, a license file.\n- Or use docker image.\n```shell\ndocker pull baikalai/deeq-nlp:v1.4.2\n```\n- Caution: You should use deeq NLP v1.4.2 or later.\n\n## How to use\n\n```python\nfrom deeqnlpy import Tagger\n\nmy_tagger = Tagger(\'localhost\') # If you have your own local deeq NLP. \n# or\ntagger = Tagger() # With smaller public cloud instance, it may be slow.\n\n# print results. \nres = tagger.tags(["안녕하세요.", "반가워요!"])\n\n# get protobuf message.\nres.msg()\n\n# get json object\njo = res.as_json()\nprint(jo)\n\n# get tuple of pos tagging.\nres.pos()\n\n# another methods\nres.morphs()\nres.nouns()\nres.verbs()\n\n# custom dictionary\ncust_dic = tagger.custom_dict("my")\ncust_dic.copy_np_set({\'내고유명사\', \'우리집고유명사\'})\ncust_dic.copy_cp_set({\'코로나19\'})\ncust_dic.copy_cp_set({\'코로나^백신\', \'"독감^백신\'})\ncust_dic.update()\n\ntagger.set_domain(\'my\')\ntagger.pos(\'코로나19는 언제 끝날까요?\')\n```\n',
    'author': 'Gihyun YUN',
    'author_email': 'gih2yun@baikal.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://baikal.ai/app2/#/morpheme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
