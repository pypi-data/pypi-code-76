# -*-coding: <Utf-8> -*-
""" Comments for all the librairy """

import requests
import re
import time
import asyncio
from pint import UnitRegistry

timeout = 2.5
ureg = UnitRegistry()
MotorSpreader = 2
MotorCrab = 1
MotorChassis = 3
MotorDirectionBackward = 1
MotorDirectionForward = 2


class Crane:
    

    def get_motor_info_from_number(self, sNr):
        """ 
        It takes the crane as input and returns the  number of the motor with its IP address.
        :param : see def start (sNr, turn) parameters
            
        """
        
        if not isinstance(sNr, int):
            raise TypeError(" The value of n must be an integer but got " +str(sNr))
    
        if MotorSpreader == sNr:
            return (self.ip_slave, 1)
        elif MotorCrab == sNr:
            return (self.ip_slave, 2)
        elif MotorChassis == sNr:
            return (self.ip_master, 1)
        raise RuntimeError("Invalid motor number, must be MotorSpreader, MotorCrab or MotorChassis, got "+str(sNr))

    def start (self, sNr, turn):
        """ 
        :param sNr: This is the first of the arguments. It indicates the engine number that we would like to start. It takes the values ​​1 2 3 which indicates motors 1 2 and 3 respectively
        :param turn: It indicates the direction in which we would like to run the engine. 1 for moving forward and -1 for moving backward.


        """
        if turn not in [MotorDirectionForward, MotorDirectionBackward]:
            raise RuntimeError("Invalid parameter, turn must be either MotorDirectionForward or MotorDirectionBackward. Got " +str(turn))			
    
        ip, numMotor = self.get_motor_info_from_number(sNr)
        r = requests.get("http://"+ip+"/startM?sNr="+str(numMotor)+"&turn="+str(turn),timeout=timeout)
        
        if r.status_code !=200:
            raise RuntimeError("Unable to control the motor, "+str(r.status_code))

        if r.text != "ok":
            raise RuntimeError("Able to controle the motor but got not OK answer: "+r.text)
        return r.text
        
    def stop(self, sNr):
        """
        :param sNr: This is the first of the arguments. It indicates the engine number that we would like to start. It takes the values ​​1 2 3 which indicates motors 1 2 and 3 respectively

        """
        global timeout
        ip, numMotor = self.get_motor_info_from_number(sNr)
        r = requests.get("http://"+ip+"/stopM?sNr="+str(numMotor),timeout=timeout)
        if r.status_code !=200:
            raise RuntimeError("Unable to control the motor, "+str(r.status_code))

        if r.text != "ok":
            raise RuntimeError("Able to controle the motor but got not OK answer: "+r.text)
        return r.text
        
        
    def step (self, sNr, turn):
        """ 
        :param sNr: This is the first of the arguments. It indicates the engine number that we would like to start. It takes the values ​​1 2 3 which indicates motors 1 2 and 3 respectively
        :param turn: It indicates the direction in which we would like to run the engine. 1 for moving forward and -1 for moving backward.

        Example:
        step(MotorSpreader, MotorDirectionBackward)  turns the spreader backwards
        """
        return (self.start(sNr, turn), self.stop(sNr))
  
            
    def start_for(self, t, sNr, turn ):
        
        """:param t : This is the time during which we decide to run a motor. The syntax is t * ureg.second
        It is noted that we can also write t * ureg.millisecond in case we decide to run the engine for t millisecond.
        :param sNr : See the start function
        :param turn :See the start function
     
        example
        start_for(5000*ureg.nanosecond,MotorChassis,MotorDirectionForward)
        Here we decide to rotate the Chassis forward for 5000 nanosecond
        """
        if sNr not in [MotorChassis, MotorSpreader, MotorCrab]:
            raise RuntimeError("Invalid parameter, sNr must be either MotorChassis or MotorSpreader or MotorCrab . Got " +str(sNr))
    
        if t < 0:
            raise ValueError("t must be greater than 0 but got "+str(t))
   
        init_time = time.time()*ureg.second
        print("start")
        while time.time()*ureg.second - init_time < t:
            self.start(sNr, turn)
        self.stop(sNr)
        print("stop")

        

    def _get_battery(self):
        """
        This function returns the battery state : the state of the master's battery as well as that of the slave
        """
    
        global timeout

        r1=requests.get("http://"+self.ip_master+"/getBat?n=1", timeout=timeout)
        r2=requests.get("http://"+self.ip_slave+"/getBat?n=2", timeout=timeout)

        if r1.status_code != 200: 
            raise RuntimeError("Please check if the r1 battery is correctly powered")
    
        if r2.status_code != 200: 
            raise RuntimeError("Please check if the r2 battery is correctly powered")
    
        return (int(r1.text), int(r2.text))

    battery = property(_get_battery)

    def change_speed(self, sNr, diff):
        """
        This function allows us to modify the engine speed while varying its cyclic ratio. 
        :param sNr:  see def start (sNr, turn) parameters
        :param diff: This parameter is used to vary the speed of the motor. Il s'agit d'un entier.
        It should be noted that the maximum speed that the motor can reach is 100 and the motor speed cannot drop below 30
        Example:
		change_speed( MotorSpreader, -60 ) : allows to decrease the motorspeed 3 by 60
        """
        global timeout 
    
        if not isinstance (diff, int):
            raise TypeError()
        
        ip, numMotor = self.get_motor_info_from_number(sNr)
        r = requests.get("http://"+ip+"/changePWMTV?sNr="+str(numMotor)+"&diff="+str(diff), timeout=timeout)
    
        if r.status_code != 200: 
            raise RuntimeError("Unable to change the speed of the motor,"+str(r.status_code))
    
        result = re.search("neuer Speed=\s+(\d+)", r.text)
        num = int(result.groups()[0])
        return num

    def get_speed(self , sNr):
        """ Returns the current speed for a motor """ 
        
        return self.change_speed(sNr, 0)
        
    def set_speed(self , sNr, speed):
        
        """ set the speed for a motor """    	
        current = self.change_speed(sNr, 0) 
        diff = speed - current 
        return self.change_speed(sNr, diff)

    def init (self, ip):
        """ 
        The purpose of this function is to initialize the IP address of the master and once the IP address of the master is
        initialized to obtain that of the slave thanks to the getOtherEsp function   
        """
        global ip_master, ip_slave
        self.ip_master = ip
        self.ip_slave = self.get_other_esp(ip) 

    def get_other_esp(self, ip):
        """
        This function has the role of launching a request to obtain the IP address of the slave
        """
        global timeout
        r = requests.get("http://" + ip + "/getOtherEsp", timeout = timeout)
        if r.status_code != 200:
            raise RuntimeError ("I failed to get the IP address of the slave. Check if the latter is correctly supplied then try again")
        return r.text
        



        

if __name__ == "__main__":
    
  
    ip_1 = "172.17.217.217"
    ip_2 = "172.17.217.217"
   
    crane_1 = Crane()
    crane_2 = Crane()
    
    crane_1.init(ip_1)
    crane_2.init(ip_2)

    print(crane_1.battery)
    print(crane_1.change_speed(MotorCrab, 40))

    print(crane_2.change_speed(MotorSpreader,20))
    print(crane_2.battery)
    crane_2.step(MotorChassis ,MotorDirectionBackward)
    crane_1.step(MotorCrab, MotorDirectionBackward)
    print (crane_1.get_speed(MotorCrab))
    crane_2.start_for(1*ureg.second,MotorSpreader,MotorDirectionBackward)

