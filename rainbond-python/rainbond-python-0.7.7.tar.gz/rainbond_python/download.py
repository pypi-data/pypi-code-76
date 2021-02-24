import os
from .tools import handle_abnormal
from flask import Response, send_from_directory, make_response


def download_file(file_path: str, file_name: str):
    if not os.path.exists(os.path.join(file_path, file_name)):
        handle_abnormal(
            message='文件(普通下载)路径不存在',
            status=400,
            other={'file_path': file_path, 'file_name': file_name}
        )
    response = make_response(send_from_directory(
        file_path,  # 本地目录的path
        file_name,  # 文件名(带扩展名)
        as_attachment=True
    ))
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(
        file_name.encode().decode('latin-1'))
    return response


def download_flow(file_path: str, file_name: str):
    complete_path = os.path.join(file_path, file_name)
    if not os.path.exists(complete_path):
        handle_abnormal(
            message='文件(流传输)路径不存在',
            status=400,
            other={'complete_path': complete_path}
        )

    def send_file():
        # 流式读取文件
        with open(complete_path, 'rb') as target_file:
            while 1:
                data = target_file.read(20 * 1024 * 1024)   # 每次读取20M
                if not data:
                    break
                yield data
    # 浏览器不识别的也会自动下载
    response = Response(send_file(), content_type='application/octet-stream')
    # 确保中文格式不乱码
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(
        file_name.encode().decode('latin-1'))
    return response
