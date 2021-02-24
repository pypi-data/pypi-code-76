# coding: utf-8
import os
import sys
import xx_tool

print('hdt test')
xx_tool.foo()

def create_file(file_path, msg, headline = None):
    if os.path.exists(file_path):
        os.remove(file_path)
    f = open(file_path,"a")
    if headline:
        f.write(headline)
    f.writelines(msg)
    f.close


def inject_work_git_hooks(path,content_sh,content_py=''):
    git_path = os.path.join(path,'.git/hooks')
    if not os.path.exists(git_path):
        os.makedirs(git_path)
    pre_path = os.path.join(git_path,'pre-commit')
    pre_py_path = os.path.join(git_path,'pre_commit.py')
    # 获取 pre_py_path 的绝对路径
    pre_py_abs_path = os.path.abspath(pre_py_path)
    print('pre_py_path:' + pre_py_abs_path)
    str_head_line = 'prepypath='+pre_py_abs_path+'\n'
    create_file(pre_path,content_sh,headline=str_head_line)
    # 让其变为可执行文件
    cmd = "chmod +x " + pre_path
    os.system(cmd)
    create_file(pre_py_path,content_py)

def main():
    print('def main')
    msg = "test"
    # if len(sys.argv) > 1:
    #     msg = sys.argv[1]
    # if len(sys.argv) > 2:
    #     path = sys.argv[2]

    # with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inj/HOOK_PRE_COMMIT'), 'r', encoding='utf-8') as content_sh:
    #     #读取 SH 脚本内容
    #     with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inj/PY_PRE_COMMIT'), 'r', encoding='utf-8') as content_py:
    #         inject_work_git_hooks(path,content_sh = content_sh,content_py = content_py)

    #create_file('./hdt.txt',msg)
    xx_tool.foo()

def foo():
    xx_tool.foo()

if __name__ =='__main__':
    main()
    