#!/usr/bin/env python
# -*-coding:utf-8 -*-


'''
 ~ 接口多参数测试用例生成
   用例包括正常值paris-2组合的用例、异常值用例、不传必选参数用例和不传全部可选参数的用例
   每个用例取值后面会增加一个字符串，表示用例属性：
   1、正常用例，取值是normal
   2、缺少必选参数的异常用例，是missing_required_param
   3、其它异常用例，是abnormal


示例：
    # 一行代表一个参数，一个参数有3个属性。
    # 前两个是列表，最后一个是布尔类型。分别是正常值、异常值和是否必选参数
    params = [
        [[1, 2], [0, 3], False],
        [[-1, -2], [0, -3], True],
        [[-3, 3], [-2, 4], False]
    ]
    for case in InterfaceTestcases(params):
        print(case)

    # 结合pytest
    @pytest.mark.parametrize(['param_1', 'param_2', 'param_3', 'normal_flag'], [
        value_list for value_list in InterfaceTestcases([
            [['1', '10'], ['0', '7'], True],
            [["1", '10', '100'], ['0', '101'], False],
            [[None, '', 2161524184], ['1'], False],
            [[None, '', '1', '11'], [0, 'f2rewrawr'], False]
        ])
    ])
    def test_1(self, param_1, param_2, param_3, normal_flag):
        params = {
            'param_1': param_1,
            'param_2': param_2,
            'param_3': param_3
        }

        # params删除不传入的参数
        params = {k: v for k, v in params.items() if v != 'no_param'}

        if normal_flag == 'normal':
            do_something_normal()
        elif normal_flag == 'abnormal':
            do_something_abnormal()
        else:
            pass

'''


from typing import List
import random

from allpairspy import AllPairs


class InterfaceTestcases(object):
    """接口多参数测试用例生成"""

    def __init__(self, params: List[List]) -> None:
        '''
            @params: params，一行代表一个参数，一个参数有3个属性。
                            前两个是列表，最后一个是布尔类型。分别是正常值、异常值和是否必选参数
        '''
        self.params = params
        self.normal_list = [list(set(row[0])) for row in self.params]
        self.normal_cases = self.createPairs()
        self._cases = self.createAllCases()
        self._count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._count < len(self._cases):
            self._count += 1
            return self._cases[self._count - 1][:]
        else:
            raise StopIteration('已经到达临界')

    def createPairs(self):
        ''' 生成正常测试用例 '''
        if len(self.normal_list) == 0:
            return []
        elif len(self.normal_list) == 1:
            return [[case, 'normal'] for case in self.normal_list[0]]
        return [row + ['normal'] for row in AllPairs(self.normal_list)]

    def getRandomNormalCaseWithoutExcptParam(self, param_id: int) -> List:
        ''' 随机生成不包括异常参数的正常用例
            params: param_id：异常参数序号
            return: 不包括异常参数的随机正常用例
        '''
        case = self.normal_list[:param_id] + self.normal_list[param_id+1:]
        return [random.choice(row) for row in case]

    def createExceptionCases(self) -> List:
        ''' 生成异常测试用例 '''

        cases = []
        for i, exception_row in enumerate(self.params):
            exception_list = exception_row[1]
            for data in exception_list:
                new_case = self.getRandomNormalCaseWithoutExcptParam(i)
                new_case.insert(i, data)
                new_case.append('abnormal')
                cases.append(new_case)
        return cases

    def createNoParamsCases(self) -> List:
        ''' 获取不传参数的用例。
            1、每个必选参数生成一个不带该参数的用例
            2、所有非必选参数，生成一个不带所有非必选参数的用例
        '''

        cases = []
        is_has_option_param = False

        # 可选参数用例，case要深度拷贝，否则后面可能改变normal_cases的值
        optional_param_cace = random.choice(self.normal_cases)[:]

        for i, row in enumerate(self.params):
            if row[-1]:
                # 判断参数是否必选

                # new_case要深度拷贝，否则会改变normal_cases的值
                new_case = random.choice(self.normal_cases)[:]
                new_case[i] = 'no_param'
                new_case[-1] = 'missing_required_param'
                cases.append(new_case)
            else:
                is_has_option_param = True
                optional_param_cace[i] = 'no_param'
        return cases + [optional_param_cace] if is_has_option_param else cases

    def createAllCases(self) -> List:
        except_cases = self.createExceptionCases()
        noparam_cases = self.createNoParamsCases()
        return self.normal_cases + except_cases + noparam_cases


if __name__ == "__main__":
    pass
