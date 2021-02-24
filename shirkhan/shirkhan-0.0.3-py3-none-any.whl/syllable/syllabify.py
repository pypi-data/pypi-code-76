from shirkhan.syllable.sword import SWord
from shirkhan import decode


def do_group(retoken: str):
    """
    把类似 001010010 的 token 转换成
    :param retoken:
    :return:
    """
    group = []
    tmp = []
    for index in range(len(retoken)):
        item = retoken[index]
        tmp.append(item)

        if item == '1':
            group.append(tmp)
            tmp = []
        elif index == len(retoken) - 1:
            group.append(tmp)
    return group


def embed_delimiter(retoken, delimiter="x"):
    """
    按照维吾尔语分音节通用规则分析每一个组合并分音节点插入给的字符并返回
    :param retoken:
    :return:
    """
    # group
    group = do_group(retoken)
    # print("group", group)
    position = ""
    for index in range(len(group)):
        item = group[index]
        if len(item) == 0:
            continue
        if index == 0 or item[-1] != '1':  # 第一和最后一项
            position = position + ''.join(item)
            continue
        c_count = len(item) - 1
        if c_count == 1:
            position = position + item[0] + delimiter + ''.join(item[1:])

        elif c_count == 2:
            position = position + item[0] + delimiter + ''.join(item[1:])
        elif c_count == 3:
            position = position + ''.join(item[:2]) + delimiter + ''.join(item[2:])
        else:
            pass
            # print("不知道", c_count, item)
    return position


def position_transform(original_word, positional_word, delimiter="x"):
    """
    按照反转分析并嵌入分割的字符在原词上还原分割点
    [因为之前反转过，现在简单的吧内容整体转换时不行的，坐标需要反转回去]
    :param original_word:
    :param positional_word:
    :return:
    """
    word_list = list(original_word)
    for i in range(len(positional_word)):
        item = positional_word[i]
        if item == delimiter:
            word_list.insert(len(word_list) - i, delimiter)
    return ''.join(word_list)


def syllabify(word):
    """
    思路：
    1. 把单词向量化，按照元音，辅音 的0，1 值生成token 0100100
    2. 从后往前分析 所以需要反转 retoken 0010010
    3. 把retoken 以元音为分界分组 001 001 0
    4. 按照分音节通用算法进行给retoken 植入分隔符
        - 两个元音之间有1个辅音它属于前面的音节
        - 两个元音之间有2个辅音它一个属于前面的，一个属于后面的
        - 两个元音之间有3个辅音 前两个属于前面的，最后一个属于后面的
    5. 把嵌入分割符的retoken分割点坐标映射到原始内容上 i -> len(word)-i
    6. 按照分割符切割

    :param word:
    :return:
    """
    # 用0100101 标识元音辅音
    token = SWord(word).tokenize()

    # 反转从末尾往前分析
    retoken = token[::-1]

    # 给retoken 植入分割符
    delimiter = "x"
    positional = embed_delimiter(retoken, delimiter)

    # 按照植入分隔符的字符还原原词
    final_posotional = position_transform(word, positional, delimiter)

    # 分割
    return final_posotional.split(delimiter)


if __name__ == '__main__':
    pass
    word = "شىرخان"
    syllabify(word)
