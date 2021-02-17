import pandas as pd

def convertJavaSignalToPython(signalJava):
    '''
    Method converts a Java signal object (with getTime(), getValue() methods) into a pandas Series
    :param signalJava: Java signal object
    :return: pandas Series
    '''
    timeJava = signalJava.getTime()
    timePython = []
    for t in range(len(timeJava)):
        timePython.append(timeJava[t])

    valueJava = signalJava.getValue()
    valuePython = []
    for t in range(len(valueJava)):
        valuePython.append(valueJava[t])

    return pd.Series(valuePython, timePython)


def concatenate(signalFirst, signalSecond):
    '''
    Method concatenates two series by adding last time and value of the first signal to each time and value of the
    second signal.
    :param signalFirst: first signal
    :param signalSecond: second signal
    :return: concatenated signal
    '''
    index = [x + signalFirst.index[-1] for x in signalSecond.index]
    values = [x + signalFirst.values[-1] for x in signalSecond.values]

    return signalFirst.append(pd.Series(values, index))