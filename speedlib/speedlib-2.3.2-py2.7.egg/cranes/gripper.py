from pint import UnitRegistry

def gripper( n=0 ):
    """  It is a function to control the gripper
        : param : x is the parameter which allows to activate or not the magnet. 
         This sensor has as output d which is the distance which separates it from an obstacle (I take here the ceiling of the container)
        :param d :  it gives a certain value that we can read
        
        :n  this is the number of the crane
    """

    global timeout
    
    d = sensor (n) * ureg.meter
    x = False # initial state value (convention)
    if d > 0.002 *ureg.meter : #for exemple
        x = False # The magnet is disabled
    if d < 0.002 * ureg.meter : # for exemple
        x = True # The magnet is disabled
    
    
    r = requests.get("http://"+"172.17.217.60"+"/gripper?sNr="+str(2)+"&x="+str(x),timeout=timeout)
    


def sensor(n = 0):
    """
We can imagine a function which takes as input the number of the crane and therefore the sensor which will be placed on the drue and which will return
a certain distance d that we will recover in the seize function
"""
    return d
