
from setuptools import setup
# 公開用パッケージの作成 [ezpip]
import ezpip

# 公開用パッケージの作成 [ezpip]
with ezpip.packager(develop_dir = "./_develop_ezRL/") as p:
	# パッケージ化
	setup(
		name = "ezRL",
		version = "1.1.7",
		description = "easy Reinforcement Learning tool for python",
		author = "ezRL_team",
		author_email = "ezrl.adm@gmail.com",
		url = "https://github.co.jp/",
		packages = p.packages,
		install_requires = ["relpath"],
		long_description = p.long_description,
		long_description_content_type = "text/markdown",
		license = "CC0 v1.0",
		classifiers = [
			"Programming Language :: Python :: 3",
			"Topic :: Software Development :: Libraries",
			"License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
		],
		# entry_points = """
		#     [console_scripts]
		#     hoge = hoge:hoge
		# """
	)
