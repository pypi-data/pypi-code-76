import ybc_commons.environment as _env

__version__ = '1.1.0a2'
_scene = _env.get_scene()

if _scene == _env.Scene.ZEUS_CODING:
    from ybc.ybc_zeus_coding_impl import (
        msgbox,
        enterbox,
        fileopenbox,
        chat,
        contrast,
        food,
        face,
        speak,
        camera,
    )

    __all__ = [
        'msgbox', 'enterbox', 'fileopenbox',
        'chat', 'contrast', 'food',
        'face', 'speak', 'camera',
    ]

else:
    from ybc.ybc_impl import (
        msgbox,
        enterbox,
        fileopenbox,
        chat,
        contrast,
        food,
        face,
        speak,
        camera,
    )
    from ybc.ybc_impl import (
        card,
        share,
    )
    from ybc_calculate import check
    from ybc_exception import exception_handler
    from ybc_face import (
        magic,
        age,
        beauty,
        compare,
        gender,
        gender1,
        glass,
        glass1,
        info,
        info_all,
        mofa,
    )
    from ybc_qrcode import (
        make,
        makeqr,
    )
    from ybc_speech import (
        record,
        text2voice,
        voice2text,
    )
    from ybc_todo import (
        todo,
        draw,
        openweb,
    )
    from ybc_tuya import (
        xzpq,
        jiqimao,
        rainbow,
        flower,
        stamen,
        petal,
        stem,
        rgb
    )
    from ybc_tuya import rainbow1
    from ybc_tuya import rainbow2
    from ybc_tuya import rainbow3
    from ybc_tuya import rainbow4
    from ybc_tuya import rainbow5
    from ybc_tuya import rainbow6
    from ybc_tuya import rainbow7
    from ybc_tuya import rainbow8
    from ybc_txt_search import xh
    from ybc_gesture import gesture
    from ybc_sms import sms
    from ybc_player import play

    g = globals()

    __all__ = [
        'check',
        'face', 'magic', 'age', 'beauty', 'compare', 'gender', 'gender1', 'glass',
        'glass1', 'info', 'info_all', 'mofa',
        'record', 'speak', 'text2voice', 'voice2text',
        'msgbox', 'enterbox', 'fileopenbox',
        'camera',
        'todo', 'draw', 'openweb',
        'make', 'makeqr',
        'gesture',
        'chat',
        'share', 'card', 'contrast', 'food',
        # ybc_tuya
        'xzpq', 'jiqimao', 'rainbow', 'flower', 'stamen', 'petal', 'stem', 'rgb',
        'rainbow1', 'rainbow2', 'rainbow3', 'rainbow4', 'rainbow5', 'rainbow6', 'rainbow7',
        'rainbow8',
        'xh',
        'sms',
        'play',
    ]

    global_functions = [k for k in __all__ if k and k[0] != '_' and callable(g[k])]

    for fn in global_functions:
        g[fn] = exception_handler(__name__)(g[fn])
