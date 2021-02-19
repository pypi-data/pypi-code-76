# 按比分配 a份数 b份数 总数量
def than(a, b, s):
    oneone = s / (a + b) * a
    twotwo = s / (a + b) * b
    return oneone, twotwo


# 圆环 内半径 外半径 面积或周长
def ring(r, R, SC):
    if SC == "C":
        return 2 * 3.14 * r + 2 * 3.14 * R
    elif SC == "S":
        return 3.14 * (R ** 2 - r ** 2)
    else:
        return "请检查参数！"


# 圆中方 半径 判断
def ci_sq(r, judge):
    if judge == 1:
        return 2 * r ** 2
    elif judge == 2:
        return 3.14 * r ** 2
    elif judge == 3:
        return 1.14 * r ** 2
    else:
        return "请检查参数！"


# 方中圆 半径 判断
def sq_ci(r, judge):
    if judge == 1:
        return 4 * r ** 2
    elif judge == 2:
        return 3.14 * r ** 2
    elif judge == 3:
        return 0.86 * r ** 2
    else:
        return "请检查参数"


# 方中圆中方，圆中方中园规律：最外面的图形的面积是最里面的2倍

# 扇形面积 半径 圆心角 周长或面积
def sector(r, Center_angle, SC):
    if SC == "S":
        return 3.14 * r ** 2 * Center_angle / 360
    elif SC == "C":
        return (2 * 3.14 * r * Center_angle / 360) + (2 * r)
    else:
        return "请检查参数"


#计算BMI 身高 体重
def BMI(h,w):
    return w*10000/h**2


#勾股定理求边 直角边1 直角边2 斜边
def thag(ras1,ras2,hyp):
    if ras1 == "x" and ras2 != "x" and hyp !="x":
        return (hyp**2-ras2**2)**0.5
    elif ras2 == "x" and ras1 != "x" and hyp !="x":
        return (hyp**2-ras1**2)**0.5
    elif hyp == "x" and ras1!= "x" and ras2 !="x":
        return (ras1**2+ras2**2)**0.5
    else:
        return "请检查参数"