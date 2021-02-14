import numpy as np
#----------------------------------------------------------------------------------------#

class UnreachablePositionError(Exception):
    def __init__(self, message="Unreachable position error."):
        self.message = message
        super().__init__(self.message)


class Part(object):
    def __init__(self, axis, value):
        self.__axis = axis
        self.__value = value

    def SetValue(self, value):
        if self.__axis in ['RX', 'RY', 'RZ']: self.__value = value

    def GetValue(self):
        return self.__value

    def GetAxis(self):
        return self.__axis

    def GetMatrix(self):
        if self.__axis == 'RX':
            matrix = np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, np.cos(self.__value), -np.sin(self.__value), 0.0],
                [0.0, np.sin(self.__value), np.cos(self.__value), 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ])

        if self.__axis == 'RY':
            matrix = np.array([
                [np.cos(self.__value), 0.0, np.sin(self.__value), 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [-np.sin(self.__value), 0.0, np.cos(self.__value), 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ])

        if self.__axis == 'RZ':
            matrix = np.array([
                [np.cos(self.__value), -np.sin(self.__value), 0.0, 0.0],
                [np.sin(self.__value), np.cos(self.__value), 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ])

        if self.__axis == 'TX':
            matrix = np.array([
                [1.0, 0.0, 0.0, self.__value],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ])

        if self.__axis == 'TY':
            matrix = np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, self.__value],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ])

        if self.__axis == 'TZ':
            matrix = np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, self.__value],
                [0.0, 0.0, 0.0, 1.0]
            ])
        return matrix


class ForwardKinematics(object):
    def __init__(self):
        self.__record = list()
        self.__endEffector = list()
        self.__parts = list()
        self.__plotTrigger = True
        self.__shadow = list()

    def SetDefaultParameters(self, xmlfile):
        from xml.dom import minidom
        jointAngles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        try: robot = minidom.parse(xmlfile)
        except: raise RuntimeError("\nFile not found or does not exist! Make sure file is in the same folder as .py script!")
        self.__robotName = robot.getElementsByTagName('robot')[0].attributes['name'].value
        nodeTypes = robot.getElementsByTagName('type')
        nodeValues = robot.getElementsByTagName('value')
        angleCounter = 0
        for i in range(len(nodeTypes)):
            if nodeValues[i].attributes['value'].value == '0.0':
                self.__parts.append(Part(nodeTypes[i].attributes['type'].value, jointAngles[angleCounter]))
                angleCounter += 1
            else: self.__parts.append(Part(nodeTypes[i].attributes['type'].value, float(nodeValues[i].attributes['value'].value)))
        self.Calculate()
        self.__shadow = np.array(self.__record.copy())
        self.__record.clear()

    def GetValues(self):
        return [part.GetValue() for part in self.__parts if part.GetAxis() in ['RX', 'RY', 'RZ']]

    def UpdateParameters(self, angles):
        valueIndex = 0
        for partIndex in range(len(self.__parts)):
            if self.__parts[partIndex].GetAxis() in ['RX', 'RY', 'RZ']:
                self.__parts[partIndex].SetValue(angles[valueIndex])
                valueIndex += 1
            if valueIndex == len(angles): break

    def Calculate(self, recording=True):
        transformedMatrix = np.identity(4)
        for part in self.__parts:
            transformedMatrix = np.dot(transformedMatrix, part.GetMatrix())
            if recording: self.__record.append((transformedMatrix[0][3], transformedMatrix[1][3], transformedMatrix[2][3]))
        x = transformedMatrix[0][3]
        y = transformedMatrix[1][3]
        z = transformedMatrix[2][3]
        ro = np.arctan2(transformedMatrix[2][1], transformedMatrix[2][2])
        omega = np.arctan2(-transformedMatrix[2][0], np.sqrt(transformedMatrix[2][1]**2 + transformedMatrix[2][2]**2))
        tau = np.arctan2(transformedMatrix[1][0], transformedMatrix[0][0])
        self.__endEffector = [x, y, z, ro, omega, tau]
        return [x, y, z, ro, omega, tau]

    def Plot(self, geometry=None, isolatedPoints=None, threePoints=None):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        if self.__plotTrigger:
            plt.style.use(['dark_background'])
            plt.rcParams['grid.color'] = '#555555'
            plt.rcParams['toolbar'] = 'None'
            fig = plt.figure(figsize=(10, 10))
            fig.patch.set_facecolor('#282C34')
            try: fig.canvas.manager.window.move(200,200)
            except: pass
            fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
            fig.canvas.set_window_title(self.__robotName)
            ax = fig.add_subplot(111, projection='3d', proj_type='ortho')
            ax.set_facecolor('#282C34')
            ax.set_xlim3d(-200, 200); ax.set_ylim3d(-200, 200); ax.set_zlim3d(0, 400)
            ax.set_xlabel('X-AXIS'); ax.set_ylabel('Y-AXIS'); ax.set_zlabel('Z-AXIS')
            ax.w_xaxis.set_pane_color(tuple([0.2 for _ in range(4)]))
            ax.w_yaxis.set_pane_color(tuple([0.2 for _ in range(4)]))
            ax.w_zaxis.set_pane_color(tuple([0.2 for _ in range(4)]))
            self.__plotTrigger = False

        xplot, yplot, zplot = [0], [0], [0]
        coordinates = self.__endEffector.copy()
        if not len(self.__record): return
        for point in self.__record: xplot.append(point[0]); yplot.append(point[1]); zplot.append(point[2])
        ax.scatter(xplot, yplot, zplot, c='orange', s=25, depthshade=False)
        ax.plot(xplot, yplot, zplot, c='orange', linewidth=2)
        ax.scatter(coordinates[0], coordinates[1], coordinates[2], c='red', s=25, depthshade=False)
        ax.text(coordinates[0], coordinates[1], coordinates[2], c='white', s="[{0}, {1}, {2}]".format(int(coordinates[0]), int(coordinates[1]), int(coordinates[2])), fontsize=12)

        # DEFAULT POSE
        ax.scatter(*self.__shadow.T, c='#AAAAAA', s=15, depthshade=False)
        ax.plot(*self.__shadow.T, c='#AAAAAA')

        if np.asarray(isolatedPoints).any():
            for point in isolatedPoints: ax.scatter(*point, c='gold')
        if np.asarray(geometry).any(): ax.plot(geometry[0], geometry[1], geometry[2], c='gold', linewidth=4)
        if np.asarray(threePoints).any():
            from .Mathematics import CircleCenter3D
            circleCenter = CircleCenter3D(threePoints[0], threePoints[1], threePoints[2])[0]
            ax.scatter(*threePoints[0], c='green')
            ax.scatter(*threePoints[1], c='green')
            ax.scatter(*threePoints[2], c='green')
            ax.scatter(*circleCenter, c='gold')
        plt.show()


class InverseKinematics(object):
    def __init__(self, forwardKinematics, initialPosition=0.001):
        self.__forwardKinematics = forwardKinematics
        self.__diff = np.radians(1)
        self.__angles = [initialPosition for _ in range(6)]

    def __NormalizeShift(self, shift):
        return np.deg2rad(round(-np.fmod(shift, 180.0)))

    def __CreateShiftedMatrix(self, forwardKinematics, diff):
        shiftedMatrix = list()
        inputMatrix = np.array([forwardKinematics.GetValues() for _ in range(6)]) + np.diag([diff for _ in range(6)], 0)
        for i in range(6):
            forwardKinematics.UpdateParameters(inputMatrix[i])
            shiftedMatrix.append(forwardKinematics.Calculate())
        return shiftedMatrix

    def Calculate(self, desiredPosition, iterations=60):
        for iteration in range(iterations):
            diversion = self.__angles.copy()
            self.__forwardKinematics.UpdateParameters(self.__angles)
            currentPosition = self.__forwardKinematics.Calculate()
            self.__forwardKinematics.UpdateParameters(self.__angles)
            shifedPosition = self.__CreateShiftedMatrix(self.__forwardKinematics, self.__diff)
            firstMatrix = np.array([currentPosition for _ in range(6)]).T
            secondMatrix = np.array(shifedPosition).T
            jacobianMatrix = firstMatrix - secondMatrix
            inverseJacobian = np.linalg.inv(jacobianMatrix)
            shiftMatrix = np.dot(inverseJacobian, np.subtract(desiredPosition, currentPosition))
            for i in range(6):
                self.__angles[i] += self.__NormalizeShift(shiftMatrix[i])
                while self.__angles[i] >  np.pi/2: self.__angles[i] -= np.pi
                while self.__angles[i] < -np.pi/2: self.__angles[i] += np.pi
            if diversion == self.__angles: return self.__angles
            if iteration > (iterations - 10):
                if np.linalg.norm(np.subtract(currentPosition[:3], desiredPosition[:3])) > 5.0 and iteration == (iterations-1):
                    raise UnreachablePositionError("The given coordinates leads to an unreachable position !\n")
        return self.__angles
