from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    requirements_list = [line.strip() for line in fr.readlines()]

setup(
    name='fastutil',
    version='1.0.8',
    description='common python util',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='kylin',
    author_email='464840061@qq.com',
    url='https://github.com/kylinat2688/fastutil',
    python_requires=">=3.4.0",
    install_requires=requirements_list,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "taskplan = fastutil.tool.task_plan:start_plan",
            "taskkill = fastutil.tool.task_util:kill_task",
            "fitlog_init= fastutil.tool.fitlog_util:init_fitlog",
            "fitlog_commit= fastutil.tool.fitlog_util:fitlog_commit",
            "ver_id= fastutil.tool.git_util:ver_id",
            "date_ver_id= fastutil.tool.git_util:date_ver_id"
        ]
    }
)
