import sys
import time
from fastutil.tool import gpu_util, loguru_util, logging_util, message_util, git_util, task_plan
from fastutil.model import model_util
from loguru import logger
from fastutil.data import cleaner
import argparse
from multiprocessing import Pool


def test_util():
    message_util.send_email('测试日志', '收到了吗', '464840061@qq.com')
    logging_util.set_rotating_logger(__name__, 'log/test.log')
    loguru_util.add_path('log/test1.log')
    loguru_util.add_email('错误日志', '464840061@qq.com')
    logger.info(gpu_util.check_gpu(100))
    logger.error('这里发生错误了')
    task_plan.start_plan()


def test_clean():
    doc1 = '<div><p><b>This is a 1 link:打飞机昂克赛拉打飞机▇</b> <a href="http://www.example.com">example</a></p></div>'
    doc2 = '<div><p><b>This is a 2 link:</b> <a href="http://www.example.com">example</a></p></div>'
    docs = [doc1, doc2]
    html_cleaner = cleaner.HtmlCleaner()
    print(list(html_cleaner.clean_sentences(docs)))

    unexpected_char_cleaner = cleaner.UnexpectedCharCleaner()
    print(unexpected_char_cleaner.clean('fsdfkj 打飞机昂克赛拉打飞机▇'))

    _cleaner = cleaner.GeneralCleaner()
    print(list(_cleaner.clean_sentences(docs)))


@logger.catch()
# @model_util.log_record(config_module=logging_util, save_dir='log/' + git_util.get_ver_id(), check_commit=False)
def test_task():
    parser = argparse.ArgumentParser(description='使用示例：taskkill train.py')
    parser.add_argument('name', nargs='*', help='进程grep标记')
    args = parser.parse_args('a b  c'.split())
    # time.sleep(1000)
    print(args.name)
    raise Exception('gg')


def log(v):
    with logger.contextualize(ID=v):
        time.sleep(0.3)
        logger.info(v)


if __name__ == '__main__':
    loguru_util.add_path('log/nohup.log', trace_id='ID')
    with Pool(3) as pool:
        pool.map(log, range(100))
