import __init__

Samples = []
#__init__.recordAsyn("test.wav",dur=10,TH=0.01,Samples=Samples)
#__init__.play_wav("test.wav")
endPoints = []
__init__.recordAsynSerialAndPlot(dur=10,label='test',TH=0.02,endPoints=endPoints)
#__init__.Record('test.wav')
