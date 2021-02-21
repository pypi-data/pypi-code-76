# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jawiki_cleaner']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jawiki-cleaner = jawiki_cleaner.cli:main']}

setup_kwargs = {
    'name': 'jawiki-cleaner',
    'version': '0.1.5',
    'description': 'Japanese Wikipedia cleaner',
    'long_description': '# Japanese Wikipedia Cleaner\n\n- Split sentences at the proper position taking parentheses into account.\n- Normalize Unicode characters by NFKC.\n- Extract text from wiki links\n- Remove of unnecessary symbols.\n\nApply this tool for a extracted text by WikiExtractor.\n\n```\n$ jawiki-cleaner --input ./wiki.txt --output ./cleaned-wiki.txt\n$ jawiki-cleaner -i ./wiki.txt -o ./cleaned-wiki.txt\n$ jawiki-cleaner -i ./wiki.txt # output path will be `./cleaned-wiki.txt`\n```\n\n\n\n## Example\n\n### Before\n\n```txt:wiki.txt\n<doc id="5" url="?curid=5" title="アンパサンド">\nアンパサンド\n\nアンパサンド (&amp;、英語名：) とは並立助詞「…と…」を意味する記号である。ラテン語の の合字で、Trebuchet MSフォントでは、と表示され "et" の合字であることが容易にわかる。ampersa、すなわち "and per se and"、その意味は"and [the symbol which] by itself [is] and"である。\n歴史.\nその使用は1世紀に遡ることができ、5世紀中葉から現代に至るまでの変遷がわかる。\nZ に続くラテン文字アルファベットの27字目とされた時期もある。\nアンパサンドと同じ役割を果たす文字に「のet」と呼ばれる、数字の「7」に似た記号があった(, U+204A)。この記号は現在もゲール文字で使われている。\n記号名の「アンパサンド」は、ラテン語まじりの英語「&amp; はそれ自身 "and" を表す」(&amp; per se and) のくずれた形である。英語以外の言語での名称は多様である。\n手書き.\n日常的な手書きの場合、欧米でアンパサンドは「ε」に縦線を引く単純化されたものが使われることがある。\nまた同様に、「t」または「+（プラス）」に輪を重ねたような、無声歯茎側面摩擦音を示す発音記号「」のようなものが使われることもある。\nプログラミング言語.\nプログラミング言語では、C など多数の言語で AND 演算子として用いられる。以下は C の例。\nPHPでは、変数宣言記号（$）の直前に記述することで、参照渡しを行うことができる。\nBASIC 系列の言語では文字列の連結演算子として使用される。codice_4 は codice_5 を返す。また、主にマイクロソフト系では整数の十六進表記に codice_6 を用い、codice_7 （十進で15）のように表現する。\nSGML、XML、HTMLでは、アンパサンドを使ってSGML実体を参照する。\n\n</doc>\n```\n\n### Run `jawiki-cleaner -i wiki.txt`\n\n### After\n\n```\nアンパサンド(&、英語名)とは並立助詞「...と...」を意味する記号である。\nラテン語の の合字で、Trebuchet MSフォントでは、と表示され "et" の合字であることが容易にわかる。\nampersa、すなわち "and per se and"、その意味は"and [the symbol which] by itself [is] and"である。\nその使用は1世紀に遡ることができ、5世紀中葉から現代に至るまでの変遷がわかる。\nZ に続くラテン文字アルファベットの27字目とされた時期もある。\nアンパサンドと同じ役割を果たす文字に「のet」と呼ばれる、数字の「7」に似た記号があった(U-204A)。\nこの記号は現在もゲール文字で使われている。\n記号名の「アンパサンド」は、ラテン語まじりの英語「& はそれ自身 "and" を表す」(& per se and)のくずれた形である。\n英語以外の言語での名称は多様である。\n日常的な手書きの場合、欧米でアンパサンドは「ε」に縦線を引く単純化されたものが使われることがある。\nまた同様に、「t」または「-(プラス)」に輪を重ねたような、無声歯茎側面摩擦音を示す発音記号のようなものが使われることもある。\nプログラミング言語では、C など多数の言語で AND 演算子として用いられる。\nPHPでは、変数宣言記号($)の直前に記述することで、参照渡しを行うことができる。\nBASIC 系列の言語では文字列の連結演算子として使用される。\ncodice_4 は codice_5 を返す。\nまた、主にマイクロソフト系では整数の十六進表記に codice_6 を用い、codice_7(十進で15)のように表現する。\nSGML、XML、HTMLでは、アンパサンドを使ってSGML実体を参照する。\n```',
    'author': 'hppRC',
    'author_email': 'hpp.ricecake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hpprc/jawiki-cleaner',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
