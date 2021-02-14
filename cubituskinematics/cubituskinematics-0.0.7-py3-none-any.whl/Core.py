from .Kinematics import ForwardKinematics, InverseKinematics, UnreachablePositionError
from .Mathematics import CircleCenter3D, GramSchmidt, GenerateCircle3D
from platform import system
from serial import Serial
from time import sleep
import numpy as np
from . import Bezier
import os
#----------------------------------------------------------------------------------------#
clear = lambda: os.system('cls') if system() == "Windows" else lambda: os.system('clear')
#----------------------------------------------------------------------------------------#

class Core(object):
    """
    'Core' module is used as interface between user and robotic arm.
    -> SetEndEffector()\t\tfunction to set end effector angles, default angles are [0°, 0°, 0°]
    -> SetGripper()\t\tfunction to set gripper to hold or release its grip
    -> LoadXML()\t\tfunction to set custom .xml file into the system
    -> Perform*Shape*()\tset of functions that perform specified geometric shape declared by the name of the function
    -> PerformEquationCurve()\tfunction that performs specified mathematic function described with formulas/equations (one for each axis)
    NOTE: Robotic arm performs movement ONLY when it's possible (so both XML parameters of the arm and specified end effector position are valid)
    """
    def __init__(self, endEffector=[0.0, 0.0, 0.0]):
        self.__endEffector = endEffector
        self.__gripper = 0.0
        self.__xmlName = f"{os.path.dirname(os.path.abspath(__file__))}/cubitus.xml"
        self.__toPlotPositions = list()
        self.__toSendPositions = list()

    def __SendMetadata(self, sampling, repetition=1):
        armController = Serial(port="/dev/serial0", baudrate=250_000)
        toSend = f"{sampling};{repetition};\n"
        armController.write(toSend.encode('utf-8'))
        armController.readline().decode('ascii')
        armController.close()

    def __SendData(self, angles, angleType, sampling):
        armController = Serial(port="/dev/serial0", baudrate=250_000)
        toSend = ""
        for a in range(sampling):
            if angleType == "radians": toSend = f"".join([f"{int(np.degrees(angle))};" for angle in angles[a]]) + '\n'
            if angleType == "degrees": toSend = f"".join([f"{int(angle)};" for angle in angles[a]]) + '\n'
            armController.write(toSend.encode('utf-8'))
            armController.readline().decode('ascii')
        armController.close()

    def __PlotData(self, alpha, beta, gamma, delta, epsilon, phi, inv=False, geometry=None, isolatedPoints=None, threePoints=None):
        fk = ForwardKinematics()
        fk.SetDefaultParameters(self.__xmlName)
        fk.UpdateParameters([alpha, beta, gamma, delta, epsilon, phi])
        fkResult = fk.Calculate()
        fk.Plot(geometry=geometry, isolatedPoints=isolatedPoints, threePoints=threePoints)
        if inv:
            ik = InverseKinematics(fk)
            ikResult = ik.Calculate(fkResult)
            return ikResult

    def FoldArm(self):
        self.__toPlotPositions.append([0.0, np.radians(-90.0), np.radians(90.0), 0.0, 0.0, 0.0])
        self.__toSendPositions.append([0.0, np.radians(90.0), np.radians(-90.0), 0.0, 0.0, 0.0, self.__gripper])
        if system() == "Windows":
            for position in self.__toPlotPositions: self.__PlotData(*position, inv=False)
        if system() == "Linux":
            self.__SendMetadata(1, 1)
            sleep(0.05)
            self.__SendData([self.__toSendPositions[0]], angleType="radians", sampling=1)
            sleep(2)
        self.__toPlotPositions.clear()
        self.__toSendPositions.clear()

    def SetEndEffector(self, unit, rho, omega, tau):
        if unit == "degrees": self.__endEffector = [np.radians(angle) for angle in [rho, omega, tau]]
        elif unit == "radians": self.__endEffector = [rho, omega, tau]
        else: raise ValueError("The unit should be either degrees or radians!")

    def SetGripper(self, grabbed):
        self.__gripper = 0.0 if grabbed else -35.0

    def LoadXML(self, fileName, name):
        self.__xmlName = f"{os.path.dirname(os.path.abspath(fileName))}/{name}.xml"

    def PerformPoint(self, point):
        if not isinstance(point, list): raise TypeError("Point must be declared as a list!")
        fk = ForwardKinematics()
        fk.SetDefaultParameters(self.__xmlName)
        ik = InverseKinematics(fk)

        result = ik.Calculate([*point, *self.__endEffector])
        self.__toPlotPositions.append(result.copy())
        self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])

        if system() == "Windows":
            for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, isolatedPoints=[point])
        if system() == "Linux":
            self.__SendMetadata(1, 1)
            sleep(0.05)
            self.__SendData([self.__toSendPositions[0]], angleType="radians", sampling=1)
            sleep(2)

        self.__toPlotPositions.clear()
        self.__toSendPositions.clear()

    def PerformLine(self, pointA, pointB, sampling=50, repeat=1):
        if sampling not in range(10, 101): raise ValueError("Incorrect sampling! Number must be in range <10; 100>.")
        if not isinstance(pointA, list) or not isinstance(pointB, list): raise TypeError("Each point must be declared as a list!")
        
        fk = ForwardKinematics()
        fk.SetDefaultParameters(self.__xmlName)
        ik = InverseKinematics(fk)
        pointsRange = np.linspace(0, 1, 100)
        kinematicsRange = np.linspace(0, 1, sampling)

        A = np.array(pointA)
        B = np.array(pointB)
        vect = B - A
        points = [[], [], []]
        for p in pointsRange:
            points[0].append(A[0] + p*vect[0])
            points[1].append(A[1] + p*vect[1])
            points[2].append(A[2] + p*vect[2])

        for t in kinematicsRange:
            result = ik.Calculate([A[0] + (t)*vect[0], A[1] + (t)*vect[1], A[2] + (t)*vect[2], self.__endEffector[0], self.__endEffector[1], np.arctan2(A[1], A[0])])
            self.__toPlotPositions.append(result.copy())
            self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])
        if system() == "Windows":
            for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, geometry=points)
        if system() == "Linux":
            self.__SendMetadata(sampling, repeat)
            sleep(0.05)
            self.__SendData(self.__toSendPositions, angleType="radians", sampling=sampling)
            sleep(0.75)
        self.__toPlotPositions.clear()
        self.__toSendPositions.clear()

    def PerformCircle(self, pointA, pointB, pointC, sampling=50, repeat=1):
        if sampling not in range(10, 101): raise ValueError("Incorrect sampling! Number must be in range <10; 100>.")
        if not isinstance(pointA, list) or not isinstance(pointB, list) or not isinstance(pointC, list): raise TypeError("Each point must be declared as a list!")
        fk = ForwardKinematics()
        fk.SetDefaultParameters(self.__xmlName)
        ik = InverseKinematics(fk)

        A = np.array(pointA)
        B = np.array(pointB)
        C = np.array(pointC)
        threePoints = np.array([A, B, C])
        try:
            center, points = GenerateCircle3D(A, B, C)
            for t in range(0, 100, 100//sampling):
                if not (t % (100//sampling)):
                    result = ik.Calculate([points[0][t], points[1][t], points[2][t], self.__endEffector[0], self.__endEffector[1], np.arctan2(center[1], center[0])])
                    self.__toPlotPositions.append(result.copy())
                    self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])
            if system() == "Windows":
                for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, geometry=points, threePoints=threePoints)
            if system() == "Linux":
                self.__SendMetadata(sampling, repeat)
                sleep(0.05)
                self.__SendData(self.__toSendPositions, angleType="radians", sampling=sampling)
        except UnboundLocalError: print("Given points are invalid to calculate a circle !")
        self.__toPlotPositions.clear()
        self.__toSendPositions.clear()

    def PerformParabola(self, quadratic, height, vertex, sampling=50, repeat=1):
        if sampling not in range(10, 101): raise ValueError("Incorrect sampling! Number must be in range <10; 100>.")
        fk = ForwardKinematics()
        fk.SetDefaultParameters(self.__xmlName)
        ik = InverseKinematics(fk)
        A = quadratic; sampl = height; center = np.array(vertex)
        leftBorder, rightBorder = int(center[0]-sampl), int(center[0]+sampl)
        points = [[], [], []]
        for p in range(leftBorder, rightBorder+1):
            points[0].append(p)
            points[1].append(0.0)
            points[2].append(A * ((p-center[0])**2) + center[1])

        for t in np.linspace(leftBorder, rightBorder, sampling):
            result = ik.Calculate([t, 0.0, A*((t-center[0])**2)+center[1], *self.__endEffector])
            self.__toPlotPositions.append(result.copy())
            self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])
        if system() == "Windows":
            for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, geometry=points)
        if system() == "Linux":
            self.__SendMetadata(sampling, repeat)
            sleep(0.05)
            self.__SendData(self.__toSendPositions, angleType="radians", sampling=sampling)
        self.__toPlotPositions.clear()
        self.__toSendPositions.clear()

    def PerformBezier(self, pointA, pointB, pointC, sampling=50, repeat=1):
        if not isinstance(pointA, list) or not isinstance(pointB, list) or not isinstance(pointC, list): raise TypeError("Each point must be declared as a list!")
        fk = ForwardKinematics()
        fk.SetDefaultParameters(self.__xmlName)
        ik = InverseKinematics(fk)
        pointsRange = np.linspace(0, 1, 100)
        kinematicsRange = np.linspace(0, 1, sampling)
        A = np.array(pointA)
        B = np.array(pointB)
        C = np.array(pointC)
        bezierCurve = Bezier.Curve(np.array([A, B, C]).T, degree=2)
        points = [[], [], []]
        for p in pointsRange:
            points[0].append(bezierCurve.Evaluate(p).flatten()[0])
            points[1].append(bezierCurve.Evaluate(p).flatten()[1])
            points[2].append(bezierCurve.Evaluate(p).flatten()[2])

        for t in kinematicsRange:
            result = ik.Calculate([*bezierCurve.Evaluate(t).flatten(), *self.__endEffector])
            self.__toPlotPositions.append(result.copy())
            self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])
        if system() == "Windows":
            for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, geometry=points)
        if system() == "Linux":
            self.__SendMetadata(sampling, repeat)
            sleep(0.05)
            self.__SendData(self.__toSendPositions, angleType="radians", sampling=sampling)
        self.__toPlotPositions.clear()
        self.__toSendPositions.clear()

    def PerformEquationCurve(self, Xequation, Yequation, Zequation, sampling=50, repeat=1):
        if sampling not in range(10, 101): raise ValueError("Incorrect sampling! Number must be in range <10; 100>.")
        from numpy import sin, cos, tan, pi, log
        fk = ForwardKinematics()
        fk.SetDefaultParameters(self.__xmlName)
        ik = InverseKinematics(fk)

        pointsRange = np.linspace(0, 1, 100)
        kinematicsRange =  np.linspace(0, 1, sampling)

        for equation in [Xequation, Yequation, Zequation]:
            if 't' not in equation: raise ValueError("There must be parameter 't' in each equation!")

        while(True):
            try:
                points = [[], [], []]
                for t in pointsRange:
                    points[0].append(eval(Xequation))
                    points[1].append(eval(Yequation))
                    points[2].append(eval(Zequation))

                for t in kinematicsRange:
                    result = ik.Calculate([eval(Xequation), eval(Yequation), eval(Zequation), *self.__endEffector])
                    self.__toPlotPositions.append(result.copy())
                    self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])
                if system() == "Windows":
                    for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, geometry=points)
                if system() == "Linux":
                    self.__SendMetadata(sampling, repeat)
                    sleep(0.05)
                    self.__SendData(self.__toSendPositions, angleType="radians", sampling=sampling)
                self.__toPlotPositions.clear()
                self.__toSendPositions.clear()
                return

            except UnreachablePositionError: raise UnreachablePositionError("The given coordinates leads to an unreachable position!\n")

            except: raise RuntimeError("Oops! Something went wrong!\n")

#----------------------------------------------------------------------------------------#

    def PerformUIGeometricShape(self, shape, sampling, repeat):
        if sampling not in range(10, 101): raise ValueError("Incorrect sampling! Number must be in range <10; 100>.")
        fk = ForwardKinematics()
        fk.SetDefaultParameters(self.__xmlName)
        ik = InverseKinematics(fk)

        pointsRange = np.linspace(0, 1, 100)
        kinematicsRange = np.linspace(0, 1, sampling)

        if shape == "point":
            print("\nCUBITUS MODE: ~point~")
            print("You can try these examples: \
                \nPoint:\t150 0 200 \
                \n----------- \
                \nPoint:\t180 0 230 \
                \n-----------")
            self.__pointCloud = list()
            while True:
                userInput = input("Enter point in space (to stop appending points enter 'X' or 'x'): ")
                if userInput in ['X', 'x']: break
                try:
                    P = np.array(userInput.split(' '), dtype=np.float)
                    if P.size == 3: self.__pointCloud.append(P)
                    else: print("The number of coordinates should be 3.")
                except: print("Invalid input! Try again...")

            for point in self.__pointCloud:
                result = ik.Calculate([*point, *self.__endEffector])
                self.__toPlotPositions.append(result.copy())
                self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])
            if system() == "Windows":
                for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, isolatedPoints=self.__pointCloud)
            if system() == "Linux":
                for _ in range(repeat*len(self.__pointCloud)):
                    for i in range(len(self.__pointCloud)):
                        self.__SendMetadata(1, 1)
                        sleep(0.05)
                        self.__SendData([self.__toSendPositions[i]], angleType="radians", sampling=1)
                        sleep(2)
            self.__toPlotPositions.clear()
            self.__toSendPositions.clear()
            return

        elif shape == "line":
            print("\nCUBITUS MODE: ~line~")
            print("You can try this example:\nFirst point:\t200 0 130\nSecond point:\t210 0 245 \
                \n-----------")
            A = np.array(input("Enter first point in space: ").split(' '), dtype=np.float)
            B = np.array(input("Enter second point in space: ").split(' '), dtype=np.float)
            vect = B - A

            points = [[], [], []]
            for p in pointsRange:
                points[0].append(A[0] + p*vect[0])
                points[1].append(A[1] + p*vect[1])
                points[2].append(A[2] + p*vect[2])

            for t in kinematicsRange:
                result = ik.Calculate([A[0] + (t)*vect[0], A[1] + (t)*vect[1], A[2] + (t)*vect[2], self.__endEffector[0], self.__endEffector[1], np.arctan2(A[1], A[0])])
                self.__toPlotPositions.append(result.copy())
                self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])
            if system() == "Windows":
                for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, geometry=points)
            if system() == "Linux":
                self.__SendMetadata(sampling, repeat)
                sleep(0.05)
                self.__SendData(self.__toSendPositions, angleType="radians", sampling=sampling)
                sleep(0.75)
            self.__toPlotPositions.clear()
            self.__toSendPositions.clear()
            return

        elif shape == "circle":
            print("\nCUBITUS MODE: ~circle~")
            print("You can try these examples: \
                \nFirst point:\t150 0 200\nSecond point:\t185 -80 190\nThird point:\t210 30 150 \
                \n----------- \
                \nFirst point:\t40 -200 180\nSecond point:\t25 -190 180\nThird point:\t20 -180 180 \
                \n-----------")
            A = np.array(input("Enter first point in space: ").split(' '), dtype=np.float)
            B = np.array(input("Enter second point in space: ").split(' '), dtype=np.float)
            C = np.array(input("Enter third point in space: ").split(' '), dtype=np.float)
            threePoints = np.array([A, B, C])
            try:
                center, points = GenerateCircle3D(A, B, C)
                for t in range(0, 100, 100//sampling):
                    if not (t % (100//sampling)):
                        result = ik.Calculate([points[0][t], points[1][t], points[2][t], self.__endEffector[0], self.__endEffector[1], np.arctan2(center[1], center[0])])
                        self.__toPlotPositions.append(result.copy())
                        self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])
                if system() == "Windows":
                    for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, geometry=points, threePoints=threePoints)
                if system() == "Linux":
                    self.__SendMetadata(sampling, repeat)
                    sleep(0.05)
                    self.__SendData(self.__toSendPositions, angleType="radians", sampling=sampling)
            except UnboundLocalError: print("Given points are invalid to calculate a circle !")
            self.__toPlotPositions.clear()
            self.__toSendPositions.clear()
            return

        elif shape == "parabola":
            print("\nCUBITUS MODE: ~parabola~")
            print("You can try this example: \
                \nParabolic width:\t0.03\nWidth sampling:\t30\nVertex coordinates:\t217 200 \
                \n-----------")
            A = float(input("Enter coeficient of parabolic width <0.01; 0.1>: "))
            sampl = int(input("Enter width sampling (optimal is e.g. 100): "))
            center = np.array(input("Enter vertex coordinates (two values - [X, Z]): ").split(' '), dtype=np.float)
            leftBorder, rightBorder = int(center[0]-sampl), int(center[0]+sampl)

            points = [[], [], []]
            for p in range(leftBorder, rightBorder+1):
                points[0].append(p)
                points[1].append(0.0)
                points[2].append(A * ((p-center[0])**2) + center[1])

            for t in np.linspace(leftBorder, rightBorder, sampling):
                result = ik.Calculate([t, 0.0, A*((t-center[0])**2)+center[1], *self.__endEffector])
                self.__toPlotPositions.append(result.copy())
                self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])
            if system() == "Windows":
                for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, geometry=points)
            if system() == "Linux":
                self.__SendMetadata(sampling, repeat)
                sleep(0.05)
                self.__SendData(self.__toSendPositions, angleType="radians", sampling=sampling)
            self.__toPlotPositions.clear()
            self.__toSendPositions.clear()
            return

        elif shape == "bezier":
            print("\nCUBITUS MODE: ~bezier~")
            print("You can try these examples: \
                \nFirst point:\t150 -50 240\nSecond point:\t200 -20 40\nThird point:\t230 40 190 \
                \n----------- \
                \nFirst point:\t230 0 140\nSecond point:\t280 20 280\nThird point:\t240 50 150 \
                \n-----------")
            A = np.array(input("Enter first point in space: ").split(' '), dtype=np.float)
            B = np.array(input("Enter second point in space: ").split(' '), dtype=np.float)
            C = np.array(input("Enter third point in space: ").split(' '), dtype=np.float)
            bezierCurve = Bezier.Curve(np.array([A, B, C]).T, degree=2)

            points = [[], [], []]
            for p in pointsRange:
                points[0].append(bezierCurve.Evaluate(p).flatten()[0])
                points[1].append(bezierCurve.Evaluate(p).flatten()[1])
                points[2].append(bezierCurve.Evaluate(p).flatten()[2])

            for t in kinematicsRange:
                result = ik.Calculate([*bezierCurve.Evaluate(t).flatten(), *self.__endEffector])
                self.__toPlotPositions.append(result.copy())
                self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])
            if system() == "Windows":
                for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, geometry=points)
            if system() == "Linux":
                self.__SendMetadata(sampling, repeat)
                sleep(0.05)
                self.__SendData(self.__toSendPositions, angleType="radians", sampling=sampling)
            self.__toPlotPositions.clear()
            self.__toSendPositions.clear()
            return

        else: raise RuntimeError("Unknown 'shape' parameter!")

    def PerformUIEquationCurve(self, sampling, repeat):
        from numpy import sin, cos, tan, pi, log
        fk = ForwardKinematics()
        fk.SetDefaultParameters(self.__xmlName)
        ik = InverseKinematics(fk)

        pointsRange = np.linspace(0, 1, 100)
        kinematicsRange =  np.linspace(0, 1, sampling)

        while(True):
            try:
                print("\nCUBITUS MODE: ~equation~")
                Xequation = input("X axis custom equation (use 't' as parameter): ")
                Yequation = input("Y axis custom equation (use 't' as parameter): ")
                Zequation = input("Z axis custom equation (use 't' as parameter): ")

                points = [[], [], []]
                for t in pointsRange:
                    points[0].append(eval(Xequation))
                    points[1].append(eval(Yequation))
                    points[2].append(eval(Zequation))

                for t in kinematicsRange:
                    result = ik.Calculate([eval(Xequation), eval(Yequation), eval(Zequation), *self.__endEffector])
                    self.__toPlotPositions.append(result.copy())
                    self.__toSendPositions.append([-result[0], -result[1], -result[2], result[3], result[4], result[5], self.__gripper])
                if system() == "Windows":
                    for position in self.__toPlotPositions: self.__PlotData(*position, inv=False, geometry=points)
                if system() == "Linux":
                    self.__SendMetadata(sampling, repeat)
                    sleep(0.05)
                    self.__SendData(self.__toSendPositions, angleType="radians", sampling=sampling)
                self.__toPlotPositions.clear()
                self.__toSendPositions.clear()
                return

            except UnreachablePositionError:
                print("The given coordinates leads to an unreachable position!\n")
                if input("Do you want to try again? (Y/N): ") not in ['Y', 'y']: return
                clear()

            except:
                print("Your custom equation(s) was written incorrectly!\n")
                if input("Do you want to try again? (Y/N): ") not in ['Y', 'y']: return
                clear()
