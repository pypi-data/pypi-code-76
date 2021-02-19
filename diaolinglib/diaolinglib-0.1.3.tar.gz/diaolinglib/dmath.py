# 按比分配 a份数 b份数 总数量
def than(a, b, s):
    oneone = s / (a + b) * a
    twotwo = s / (a + b) * b
    return "第一个数:{},第二个数:{}".format(oneone, twotwo)


# 圆环 内半径 外半径 面积或周长
def ring(r, R, SC):
    if SC == "C":
        return "周长是：{}".format(2 * 3.14 * r + 2 * 3.14 * R)
    elif SC == "S":
        return "面积是：{}".format(3.14 * (R ** 2 - r ** 2))
    else:
        return "请检查参数！"


# 圆中方 半径 判断
def ci_sq(r, judge):
    if judge == "方形部分":
        return "方形部分的面积：{}".format(2 * r ** 2)
    elif judge == "圆形部分":
        return "圆形部分的面积：{}".format(3.14 * r ** 2)
    elif judge == "中间部分":
        return "中间部分的面积：{}".format(1.14 * r ** 2)
    else:
        return "请检查参数！"


# 方中圆 半径 判断
def sq_ci(r, judge):
    if judge == "方形部分":
        return "方形部分的面积：{}".format(4 * r ** 2)
    elif judge == "圆形部分":
        return "圆形部分的面积：{}".format(3.14 * r ** 2)
    elif judge == "中间部分":
        return "中间部分的面积：{}".format(0.86 * r ** 2)
    else:
        return "请检查参数"


# 方中圆中方，圆中方中园规律：最外面的图形的面积是最里面的2倍

# 扇形面积 半径 圆心角 周长或面积
def sector(r, Center_angle, SC):
    if SC == "S":
        return "面积是{}".format(3.14 * r ** 2 * Center_angle / 360)
    elif SC == "C":
        return "周长是{}".format((2 * 3.14 * r * Center_angle / 360) + (2 * r))
    else:
        return "请检查参数"