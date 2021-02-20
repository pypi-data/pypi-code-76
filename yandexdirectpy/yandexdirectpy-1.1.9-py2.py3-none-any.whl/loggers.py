# import errno
# import logging
# import os
#
#
# def mkdir_p(path):
#     try:
#         os.makedirs(path, exist_ok=True)  # Python>3.2
#     except TypeError:
#         try:
#             os.makedirs(path)
#         except OSError as exc:  # Python >2.5
#             if exc.errno == errno.EEXIST and os.path.isdir(path):
#                 pass
#             else:
#                 raise
#
#
# class MakeFileHandler(logging.FileHandler):
#     def __init__(self, filename, mode='a', encoding=None, delay=0):
#         mkdir_p(os.path.dirname(filename))
#         logging.FileHandler.__init__(self, filename, mode, encoding, delay)
#
#
# FORMAT = '[%(asctime)s] %(levelname)s %(filename)s [%(funcName)s] %(message)s'
# formatter = logging.Formatter(FORMAT)
#
# # default logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
#
#
# file_handler = MakeFileHandler(filename='LOG/LOG.log')
# file_handler.setFormatter(formatter)
#
# logger.addHandler(file_handler)
#
# # error logger
# error_logger = logging.getLogger('Error Logger')
# error_logger.setLevel(logging.ERROR)
#
#
# error_file_handler = MakeFileHandler(filename='LOG/ERROR.log')
# error_file_handler.setFormatter(formatter)
#
# error_logger.addHandler(error_file_handler)