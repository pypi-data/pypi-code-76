from shirkhan.syllable.alphabet import Alphabet


class SWord:
    pass

    def __init__(self, word: str):
        self.word = word

    # 吧非母语部分清理掉
    # todo

    def tokenize(self):
        """
        吧word 标识成 00100 这种形式，其中的1和0取决于它在 alphabet [2]中的标识
        :return:
        """
        tokens = []
        for alpha in self.word:
            info = Alphabet.alpha_info(alpha)
            if info is None:
                continue
            tokens.append(str(info[2]))

        return "".join(tokens)

    @staticmethod
    def syllable_count(token: str):
        """
        按照给定的 类似 "00100" 的结果来推算音节总数
        :param token: str 用 tokenize 得出来的结果
        :return:
        """
        return len(token.split("1")) - 1

    def splitter(self):
        split_positions = []
        token = self.tokenize()
        syllable_count = self.syllable_count(token)

        # 只有一个音节
        if syllable_count == 1:
            split_positions = [len(self.word) - 1]
            return split_positions

        # 多个音节
        # split = token.split('1')  # [0,1,0,1]
        # split.reverse()  # [1,0,1,0]
        # for si in range(1, syllable_count + 1):
        #     if len(split[si]) == 1:  # 第一个音节边界
        #         split_positions.append(len(token) - len("1".join(split[:si])) - 1)
        #
        # syllables=[]
        # for pos in sorted(split_positions):
        #     syllables.append(self.word.)

        return
