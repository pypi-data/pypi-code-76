import sys

import ybc_player
from ybc_commons import httpclient
from ybc_commons.ArgumentChecker import Argument
from ybc_commons.ArgumentChecker import Checker
from ybc_commons.oss import path
from ybc_commons.util.predicates import (non_blank, is_in_range, is_empty,
                                         is_valid_filename, is_image_file)

if sys.platform == 'skulpt':
    try:
        import ybc_lib_skulpt_box as lib_box
        import ybc_lib_skulpt_camera as lib_camera
    except ImportError:
        lib_box = None
else:
    raise NotImplementedError

__BOT_URL = 'bot'
_FACE_COMPARE_URL = 'face-compare'
_FOOD_RECOG_URL = 'food-recognize'
_DEFAULT_TOP_NUM = 1
_MAX_FACE_DETECT_NUM = 30
_FACE_DETECT_URL = 'face-detect'
_PHOTO_NOT_FOUND = 400001
_MIN_FACE_DETECT_NUM = 1
_SPEAKER = 1
_SPEED = 1
_AHT = 0
_VOLUME = 100
_FORMAT = 2
_SPEAKER_DICT = {
    (1): 'xiaogang',
    (2): 'xiaoyun',
    (3): 'xiaobei',
    (4): 'sicheng',
    (5): 'ruoxi',
    (6): 'sijing',
    (7): 'xiaomei'
}
_SPEED_DICT = {(1): -200, (0.5): -250, (1.5): 250, (2): 500}
_EXT_DICT = {(2): 'WAV', (1): 'PCM', (3): 'MP3'}
_SAMPLE_RATE = 1
_TEXT_TO_VOICE_URL_PATH = 'text2voice'


def camera(filename: str = ''):
    """
    调用计算机摄像头进行拍照

    :param filename: 照片要保存的名字(文本类型,非必填) 例子:“1.jpg”
    :return: 返回所拍摄照片的名字(字符串类型)
    """
    Checker.check_arguments([
        Argument('ybc', 'camera', 'filename', filename, str,
                 is_empty | is_valid_filename & is_image_file)
    ])

    return lib_camera.camera(filename)


def enterbox(msg='', image: (str, list, tuple) = None, default=''):
    """
    展示一个输入弹框

    :param msg: 要展示的信息(文本类型,非必填) 例子:'请输入内容'
    :param image: 要展示的图片名(图片类型,非必填) 例子:'1.jpg'
    :param default: 输入框预留文字(文本类型,非必填) 例子:'请输入内容'
    :return: 返回在弹框中输入的文本(字符串类型)
    """
    return lib_box.enterbox(msg, image, default)


def fileopenbox(msg=''):
    """
    展示一个可以选择文件的弹框

    :param msg: 要展示的信息(文本类型,非必填) 例子:'我的文件'
    :return: 返回用户所选择文件的路径(字符串类型)
    """
    return lib_box.fileopenbox(msg)


def msgbox(msg='', image: (str, list, tuple) = None, audio: str = ''):
    """
    展示一个消息弹框

    :param msg: 要展示的信息(文本类型,非必填) 例子:'我想展示的信息'
    :param image: 要展示的图片的文件名(文本类型或列表,非必填) 例子:'1.jpg'
    :param audio: 要播放的音频文件的名字(音频类型,非必填) 例子:'1.mp3'
    :return: 点击弹框的'确认'按钮返回字符串'ok'，点击关闭按钮返回 None
    """
    return lib_box.msgbox(msg, image, audio)


def chat(text: str):
    """
    与智能机器人对话

    :param text: 你想说的话(文本类型,必填) 例子:"你好"
    :return: 返回智能机器人的回答(字符串类型)
    """
    Checker.check_arguments(
        [Argument('ybc', 'chat', 'text', text, str, non_blank)])
    data = {'perception': {'inputText': {'text': text}}}
    result = httpclient.post(__BOT_URL, data)
    if result['code'] == 0:
        return result['text']
    return result['msg']


def contrast(image_a: str, image_b: str):
    """
    对比人脸相似度

    :param image_a: 待对比图片名(图片类型,必填) 例子:’1.jpg’
    :param image_b: 待对比图片名(图片类型,必填) 例子:’2.jpg’
    :return: 成功: 相似度打分 失败: 提示错误信息(int类型)
    """
    Checker.check_arguments([
        Argument('ybc', 'contrast', 'image_a', image_a, str, non_blank),
        Argument('ybc', 'contrast', 'image_b', image_b, str, non_blank)
    ])
    image_a_url = path.url_of(image_a)
    image_b_url = path.url_of(image_b)
    data = {'imageAUrl': image_a_url, 'imageBUrl': image_b_url}
    res = httpclient.post(_FACE_COMPARE_URL, data)
    if res['code'] == _PHOTO_NOT_FOUND:
        raise Exception(res['msg'])
    elif res['code'] != 0:
        return res['msg']
    else:
        return '两张图片中人物的相似度为' + str(res['score']) + '%'


def food(image: str):
    """
    美食识别

    :param image: 当前目录下期望被识别的图片名字(图片类型,必填) 例如:'1.jpg'
    :return: 图片的美食信息(字典类型)
    """
    Checker.check_arguments([
        Argument('ybc', 'food', 'image', image, str, non_blank)
    ])
    res = _recog_food(image, _DEFAULT_TOP_NUM)
    if res['code'] == _PHOTO_NOT_FOUND:
        raise Exception('文件' + image + '不存在')
    elif res['code'] != 0:
        return res['msg']
    name = res['foodsInfo'][0]['name']
    calorie = str(res['foodsInfo'][0]['calorie'])
    return '图片中的食物是' + name + '，每100克含热量' + calorie + '卡路里'


def face(filename: str):
    """
    识别图片中图中的人脸信息

    :param filename: 待识别的人脸图片(图片类型,必填) 例子:’1.jpg’
    :return: 识别出的人脸信息(string类型)
    """
    Checker.check_arguments(
        [Argument('ybc', 'face', 'filename', filename, str, non_blank)])

    def _info_faces(data):
        if isinstance(data, str):
            return data
        if len(data) > 5:
            return '该照片中人脸数目超过5个啦！识别不出来啦！'
        messages = [
            '第{}个人脸信息：{}'.format(i, _compose_message(d)) for i, d in enumerate(data[:5], start=1)
        ]
        return '图片中总共发现{}张人脸：\n{}'.format(len(data), '\n'.join(messages))

    return _info_faces(_detect_face(filename, _MAX_FACE_DETECT_NUM))


def speak(text: str, model_type: int = 1):
    """
    让计算机朗读一段文字

    :param text: 要朗读的文字内容(文本类型,必填) 例子:‘欢迎来到猿编程！’
    :param model_type: 发音类型，1 代表小刚（男声），2 代表小云（女声），3 代表小北（萝莉女声），4 代表思诚（标准男生），5 代表若兮（温柔女声），6 代表思婧（严厉女声），7 代表小美（甜美女声）(int类型,非必填) 例子:1
    :return: 无
    """
    Checker.check_arguments([
        Argument('ybc', 'speak', 'text', text, str, non_blank),
        Argument('ybc', 'speak', 'model_type', model_type, int,
                 is_in_range(1, 8))
    ])
    if len(text) > 256:
        raise Exception('speak功能括号里的文本参数不符合要求哦！看看是不是字数太多，超过了限制的范围？调整一下字数吧～')

    voice_file = _text2voice4speak(text, model_type)
    ybc_player.play(voice_file)


def _text2voice4speak(text: str,
                      speaker: int = _SPEAKER,
                      speed: (int, float) = _SPEED,
                      aht: int = _AHT,
                      volume: int = _VOLUME,
                      _format: int = _FORMAT):
    """
    将文字转换为音频

    :param text: 要转换成音频的文字内容(文本类型,必填) 例子:‘欢迎来到猿编程！’
    :param speaker: 声音的类型，默认1(int类型,非必填) 例子:1
    :param speed: 语速，默认为1(int类型,非必填) 例子:1
    :param aht: 音高，默认为0(int类型,非必填) 例子:0
    :param volume: 音量，默认为100(int类型,非必填) 例子:100
    :param _format: 音频格式，1为PCM，2为WAV，3为MP3，默认为2(int类型,非必填) 例子:1
    :return: 音频文件的名字(字符串类型)
    """
    speaker = _SPEAKER_DICT[speaker]
    _speed = _SPEED_DICT.get(speed, 0)
    ext = _EXT_DICT.get(_format, 'WAV')
    data = {
        'text': text,
        'voice': speaker,
        'format': ext,
        'sampleRate': _SAMPLE_RATE,
        'volume': volume,
        'speechRate': _speed,
        'pitchRate': aht
    }
    voice = httpclient.post(_TEXT_TO_VOICE_URL_PATH, data)
    if voice['code'] == 0:
        # ybc_player.play 支持播放 url，故无需再下载文件到本地
        # 同时避免 IDE 互动题中使用到暂不支持的 urlretrive 方法
        return voice['fileUrl']
    raise Exception(voice['msg'])


def _detect_face(filename: str = '', max_face_num: int = _MIN_FACE_DETECT_NUM):
    """
    识别图片中一张人脸信息

    :param filename: 待识别的图片名(图片类型,必填) 例子:’1.jpg’
    :param max_face_num: 检测人脸数量，范围 1 ~ 5，默认为1(int类型,非必填) 例子:1
    :return:
        success: 返回包含人脸信息的字典
        failed: 提示错误信息
    """
    file_url = path.url_of(filename)
    data = {'imageUrl': file_url, 'maxFaceNum': max_face_num}
    res = httpclient.post(_FACE_DETECT_URL, data)
    if res['code'] == _PHOTO_NOT_FOUND:
        raise Exception('文件' + filename + '不存在')
    elif res['code'] != 0:
        return res['msg']
    else:
        return res['faceAttrs']


def _compose_message(data):
    _glass = '' if data['glass'] else '不'
    return '{}，{}岁左右，{}戴眼镜，颜值打分：{}分'.format(data['gender'], data['age'],
                                            _glass, data['beauty'])


def _recog_food(filename, top_num):
    """
    调用食物图片接口，并返回识别结果
    """
    file_url = path.url_of(filename)
    data = {'imageUrl': file_url, 'topNum': top_num}
    return httpclient.post(_FOOD_RECOG_URL, data)