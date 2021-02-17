import math
from steam_nb_api.roxie_parser import geometricFunctions


class BlockParameters:
    '''
        Class of block parameters
    '''

    def __init__(self, noBlock, typeBlock, nco, radius, phi, alpha, current, condname, n1, n2, imag, turn):
        self.noBlock = noBlock
        self.typeBlock = typeBlock
        self.nco = nco
        self.radius = radius
        self.phi = phi
        self.alpha = alpha
        self.current = current
        self.condname = condname
        self.n1 = n1
        self.n2 = n2
        self.imag = imag
        self.turn = turn
        self.shift2 = [0.0, 0.0]
        self.roll2 = [0.0, 0.0, 0.0]
        self.xPos = []
        self.yPos = []
        self.xBarePos = []
        self.yBarePos = []
        self.xS = []
        self.yS = []
        self.iS = []

    def toString(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
            self.noBlock, self.typeBlock, self.nco, self.radius, self.phi, self.alpha, self.current, self.condname,
            self.n1, self.n2, self.imag, self.turn, self.shift2, self.roll2)

    def setBlockShift2(self, shift2):
        self.shift2 = shift2

    def setBlockRoll2(self, roll2):
        self.roll2 = roll2

    def setXYPos(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

    def setXYBarePos(self, xBarePos, yBarePos):
        self.xBarePos = xBarePos
        self.yBarePos = yBarePos

    def setXYStrandPosAndCurrent(self, xS, yS, iS):
        self.xS = xS
        self.yS = yS
        self.iS = iS

    def findCondPos_blockCoil(self, conductorSigma, flagBare=False):
        '''
            **Returns conductor positions**

            Function to find conductor corner x-y positions and conductor current if the block has type "block coil"

            :param conductorSigma: ConductorSigma object with the conductor parameters
            :type conductorSigma: ConductorSigma
            :param flagBare: Flag indicating whether the bare or insulated conductor coordinates are required
            :type flagBare: bool

            :return: numpy.ndarray
        '''

        x0 = 0
        y0 = 0
        x0Cond = self.radius / 1000  # in [m]
        y0Cond = self.phi / 1000  # in [m]
        alpha = self.alpha / 180 * math.pi  # in [rad]
        current = self.current
        imag = self.imag
        turn = self.turn / 180 * math.pi  # in [rad]
        condname = self.condname
        nConductors = self.nco
        shift2 = self.shift2
        roll2 = self.roll2

        shiftX = shift2[0] / 1e3  # in [m]
        shiftY = shift2[1] / 1e3  # in [m]
        x0Roll = roll2[0] / 1e3  # in [m]
        y0Roll = roll2[1] / 1e3  # in [m]
        alphaRoll = roll2[2] / 180 * math.pi  # in [rad]

        wBare = conductorSigma.wBare
        hInBare = conductorSigma.hInBare
        hOutBare = conductorSigma.hOutBare
        hBare = (hInBare + hOutBare) / 2
        wInsulNarrow = conductorSigma.wInsulNarrow
        wInsulWide = conductorSigma.wInsulWide

        # Define initial x/y positions
        xTemp = x0Cond
        yTemp = y0Cond
        x = []
        y = []
        I = []
        for c in range(nConductors):

            # Calculate coordinates of four corner of bare (no insulation) conductor
            x1Bare = xTemp + wInsulNarrow
            x2Bare = xTemp + wInsulNarrow
            x3Bare = xTemp + (wBare + wInsulNarrow)
            x4Bare = xTemp + (wBare + wInsulNarrow)

            y1Bare = yTemp + (hInBare + wInsulWide)
            y2Bare = yTemp + wInsulWide
            y3Bare = yTemp + wInsulWide
            y4Bare = yTemp + (hInBare + wInsulWide)

            # Calculate coordinates of four corner of insulated conductor
            x1 = xTemp
            x2 = xTemp
            x3 = xTemp + (wBare + 2 * wInsulNarrow)
            x4 = xTemp + (wBare + 2 * wInsulNarrow)

            y1 = yTemp + (hInBare + 2 * wInsulWide)
            y2 = yTemp
            y3 = yTemp
            y4 = yTemp + (hInBare + 2 * wInsulWide)

            # Update xTemp and yTemp (using insulated conductor positions)
            xTemp = xTemp
            yTemp = yTemp + (hInBare + 2 * wInsulWide)

            # If bare conductor coordinates are needed, recalculate the four corner coordinates
            if flagBare == True:
                x1, x2, x3, x4 = x1Bare, x2Bare, x3Bare, x4Bare
                y1, y2, y3, y4 = y1Bare, y2Bare, y3Bare, y4Bare

            # Assign x- and y-positions of the four corners
            #         x4pos = [x1, x2, x3, x4]
            #         y4pos = [y1, y2, y3, y4]

            # Apply conductor rotation of angle=alpha around origin (x0Cond,y0Cond)
            (x1, y1) = geometricFunctions.rotatePoint((x1, y1), (x0Cond, y0Cond), alpha)
            (x2, y2) = geometricFunctions.rotatePoint((x2, y2), (x0Cond, y0Cond), alpha)
            (x3, y3) = geometricFunctions.rotatePoint((x3, y3), (x0Cond, y0Cond), alpha)
            (x4, y4) = geometricFunctions.rotatePoint((x4, y4), (x0Cond, y0Cond), alpha)

            # Mirror conductor about the X-axis
            if imag == 1:
                y1, y2, y3, y4 = -y1, -y2, -y3, -y4
            elif imag == 0:
                pass
            else:
                raise Exception('Value of variable imag must be either 0 or 1. It is {} instead.'.format(imag))

            # Apply conductor rotation of angle=turn around origin (x0,y0)
            (x1, y1) = geometricFunctions.rotatePoint((x1, y1), (x0, y0), turn)
            (x2, y2) = geometricFunctions.rotatePoint((x2, y2), (x0, y0), turn)
            (x3, y3) = geometricFunctions.rotatePoint((x3, y3), (x0, y0), turn)
            (x4, y4) = geometricFunctions.rotatePoint((x4, y4), (x0, y0), turn)

            # Apply roll2 conterclockwise rotation transformation
            (x1, y1) = geometricFunctions.rotatePoint((x1, y1), (x0Roll, y0Roll), alphaRoll)
            (x2, y2) = geometricFunctions.rotatePoint((x2, y2), (x0Roll, y0Roll), alphaRoll)
            (x3, y3) = geometricFunctions.rotatePoint((x3, y3), (x0Roll, y0Roll), alphaRoll)
            (x4, y4) = geometricFunctions.rotatePoint((x4, y4), (x0Roll, y0Roll), alphaRoll)

            # Apply shift2 cartesian shift transformation
            x1, y1 = x1 + shiftX, y1 + shiftY
            x2, y2 = x2 + shiftX, y2 + shiftY
            x3, y3 = x3 + shiftX, y3 + shiftY
            x4, y4 = x4 + shiftX, y4 + shiftY

            # Assign x- and y-positions of the four edges
            x4pos = [x1, x2, x3, x4]
            y4pos = [y1, y2, y3, y4]

            x.append(x4pos)
            y.append(y4pos)
            I.append(current)

        # Set calculated values as attributes of BlockParameter object
        if flagBare == False:
            self.setXYPos(x, y)
        elif flagBare == True:
            self.setXYBarePos(x, y)

        return x, y, I

    def findCondPos_cosTheta(self, conductorSigma, flagBare: bool =False, verbose: bool = False) -> list:
        '''
            **Returns conductor positions**

            Function to find conductor corner x-y positions and conductor current if the block has type "cos-theta"

            :param conductorSigma: ConductorSigma object with the conductor parameters
            :type conductorSigma: ConductorSigma
            :param flagBare: Flag indicating whether the bare or insulated conductor coordinates are required
            :type flagBare: bool
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: numpy.ndarray
        '''

        x0 = 0
        y0 = 0
        radius = self.radius / 1000  # in [m]
        phi = self.phi / 180 * math.pi  # in [rad]
        alpha = self.alpha / 180 * math.pi  # in [rad]
        current = self.current
        imag = self.imag
        turn = self.turn / 180 * math.pi  # in [rad]
        condname = self.condname
        nConductors = self.nco
        shift2 = self.shift2
        roll2 = self.roll2

        shiftX = shift2[0] / 1e3  # in [m]
        shiftY = shift2[1] / 1e3  # in [m]
        x0Roll = roll2[0] / 1e3  # in [m]
        y0Roll = roll2[1] / 1e3  # in [m]
        alphaRoll = roll2[2] / 180 * math.pi  # in [rad]

        wBare = conductorSigma.wBare
        hInBare = conductorSigma.hInBare
        hOutBare = conductorSigma.hOutBare
        hBare = (hInBare + hOutBare) / 2
        wInsulNarrow = conductorSigma.wInsulNarrow
        wInsulWide = conductorSigma.wInsulWide

        #     print('conductorSigma.name = {}'.format(conductorSigma.name))
        #     print('wBare = {}'.format(wBare))
        #     print('hInBare = {}'.format(hInBare))
        #     print('hOutBare = {}'.format(hOutBare))
        #     print('wInsulNarrow = {}'.format(wInsulNarrow))
        #     print('wInsulWide = {}'.format(wInsulWide))

        # Define the coefficients of the circle on which the x2 points (bottom-left) of each conductor rest
        # R, x0, and y0 coefficients of the circle, as in: (x-x0)**2 + (y-y0)**2 = R**2
        circle = [radius, x0, y0]

        # Define x/y positions, including conductor rotation of angle=alpha around origin (x0Cond,y0Cond)
        alphaTemp = alpha
        phiTemp = phi
        if verbose:
            print('Initial alpha = {} deg'.format(alpha / math.pi * 180))
            print('Initial phi = {} deg'.format(phi / math.pi * 180))
        x = []
        y = []
        I = []
        for c in range(nConductors):
            # Calculate coordinates of four corner of bare (no insulation) conductor
            x1Bare = radius * math.cos(phiTemp) + wInsulNarrow * math.cos(alphaTemp) - (
                        hInBare + wInsulWide) * math.sin(alphaTemp)
            x2Bare = radius * math.cos(phiTemp) + wInsulNarrow * math.cos(alphaTemp) - wInsulWide * math.sin(alphaTemp)
            x3Bare = radius * math.cos(phiTemp) + (wBare + wInsulNarrow) * math.cos(alphaTemp) - wInsulWide * math.sin(
                alphaTemp)
            x4Bare = radius * math.cos(phiTemp) + (wBare + wInsulNarrow) * math.cos(alphaTemp) - (
                        hOutBare + wInsulWide) * math.sin(alphaTemp)

            y1Bare = radius * math.sin(phiTemp) + wInsulNarrow * math.sin(alphaTemp) + (
                        hInBare + wInsulWide) * math.cos(alphaTemp);
            y2Bare = radius * math.sin(phiTemp) + wInsulNarrow * math.sin(alphaTemp) + wInsulWide * math.cos(alphaTemp)
            y3Bare = radius * math.sin(phiTemp) + (wBare + wInsulNarrow) * math.sin(alphaTemp) + wInsulWide * math.cos(
                alphaTemp)
            y4Bare = radius * math.sin(phiTemp) + (wBare + wInsulNarrow) * math.sin(alphaTemp) + (
                        hOutBare + wInsulWide) * math.cos(alphaTemp)

            # Calculate coordinates of four corner of insulated conductor
            x1 = radius * math.cos(phiTemp) - (hInBare + 2 * wInsulWide) * math.sin(alphaTemp)
            x2 = radius * math.cos(phiTemp)
            x3 = radius * math.cos(phiTemp) + (wBare + 2 * wInsulNarrow) * math.cos(alphaTemp)
            x4 = radius * math.cos(phiTemp) - (hOutBare + 2 * wInsulWide) * math.sin(alphaTemp) + (
                        wBare + 2 * wInsulNarrow) * math.cos(alphaTemp)

            y1 = radius * math.sin(phiTemp) + (hInBare + 2 * wInsulWide) * math.cos(alphaTemp);
            y2 = radius * math.sin(phiTemp)
            y3 = radius * math.sin(phiTemp) + (wBare + 2 * wInsulNarrow) * math.sin(alphaTemp)
            y4 = radius * math.sin(phiTemp) + (wBare + 2 * wInsulNarrow) * math.sin(alphaTemp) + (
                        hOutBare + 2 * wInsulWide) * math.cos(alphaTemp)

            # Increase inclination angle by atan( (h2-h1)/w )
            alphaTemp = alphaTemp + math.atan2((hOutBare - hInBare), (wBare + 2 * wInsulNarrow))

            # Find line through points 1 and 4 of the current conductor (top-left and top-right)
            # A, B, and C coefficients of the line, as in: A*x + B*y + C = 0
            line = geometricFunctions.findLineThroughTwoPoints([x1, y1], [x4, y4], verbose=verbose)

            # Find the intersection points between the circle and the line just defined
            xy = geometricFunctions.intersectLineCircle(line, circle, verbose=verbose)

            # Find the one of two intersection points that is closest to the x2 point of the current conductor
            if xy[0] == [None, None] and xy[1] == [None, None]:
                raise ValueError('No intersection points were found! [{},{}] and [{},{}].'.format(x1, y1, x2, y2))
            elif xy[0] == [None, None] and xy[1] != [None, None]:
                next_x2, next_y2 = xy[0][0], xy[0][1]
                if verbose:
                    print('One intersection point was found and selected: [{},{}].'.format(next_x2, next_y2))
            else:
                dist1 = math.sqrt((x2 - xy[0][0]) ** 2 + (y2 - xy[0][1]) ** 2)
                dist2 = math.sqrt((x2 - xy[1][0]) ** 2 + (y2 - xy[1][1]) ** 2)
                if dist1 <= dist2:
                    next_x2, next_y2 = xy[0][0], xy[0][1]
                else:
                    next_x2, next_y2 = xy[1][0], xy[1][1]
                if verbose:
                    print(
                        'Two intersection points were found: [{},{}] and [{},{}].'.format(xy[0][0], xy[0][1], xy[1][0],
                                                                                          xy[1][1]))
                    print('The closest point was selected: [{},{}].'.format(next_x2, next_y2))

            # Find new phi angle, defined as the angle between the X-axis and the line joining [next_x2,next_y2] and [x0,y0]
            phiTemp = math.atan2(next_y2 - y0, next_x2 - x0)
            if verbose:
                print('phiTemp = {} rad'.format(phiTemp))
                print('phiTemp = {} deg'.format(phiTemp / math.pi * 180))

            # If bare conductor coordinates are needed, recalculate the four corner coordinates
            if flagBare == True:
                x1, x2, x3, x4 = x1Bare, x2Bare, x3Bare, x4Bare
                y1, y2, y3, y4 = y1Bare, y2Bare, y3Bare, y4Bare

            # Assign x- and y-positions of the four corners
            #         x4pos = [x1, x2, x3, x4]
            #         y4pos = [y1, y2, y3, y4]

            # Mirror conductor about the X-axis
            if imag == 1:
                y1, y2, y3, y4 = -y1, -y2, -y3, -y4
            elif imag == 0:
                pass
            else:
                raise Exception('Value of variable imag must be either 0 or 1. It is {} instead.'.format(imag))

            # Apply conductor rotation of angle=turn around origin (x0,y0)
            (x1, y1) = geometricFunctions.rotatePoint((x1, y1), (x0, y0), turn)
            (x2, y2) = geometricFunctions.rotatePoint((x2, y2), (x0, y0), turn)
            (x3, y3) = geometricFunctions.rotatePoint((x3, y3), (x0, y0), turn)
            (x4, y4) = geometricFunctions.rotatePoint((x4, y4), (x0, y0), turn)

            # Apply roll2 conterclockwise rotation transformation
            (x1, y1) = geometricFunctions.rotatePoint((x1, y1), (x0Roll, y0Roll), alphaRoll)
            (x2, y2) = geometricFunctions.rotatePoint((x2, y2), (x0Roll, y0Roll), alphaRoll)
            (x3, y3) = geometricFunctions.rotatePoint((x3, y3), (x0Roll, y0Roll), alphaRoll)
            (x4, y4) = geometricFunctions.rotatePoint((x4, y4), (x0Roll, y0Roll), alphaRoll)

            # Apply shift2 cartesian shift transformation
            x1, y1 = x1 + shiftX, y1 + shiftY
            x2, y2 = x2 + shiftX, y2 + shiftY
            x3, y3 = x3 + shiftX, y3 + shiftY
            x4, y4 = x4 + shiftX, y4 + shiftY

            # Assign x- and y-positions of the four edges
            x4pos = [x1, x2, x3, x4]
            y4pos = [y1, y2, y3, y4]

            x.append(x4pos)
            y.append(y4pos)
            I.append(current)

        # Set calculated values as attributes of BlockParameter object
        if flagBare == False:
            self.setXYPos(x, y)
        elif flagBare == True:
            self.setXYBarePos(x, y)

        return x, y, I


    def findStrandPositions(self, conductorSigma):
        '''
            **Returns strand positions**

            Function to find strand x-y positions and strand current

            :param conductorSigma: ConductorSigma object with the conductor parameters
            :type conductorSigma: ConductorSigma

            :return: numpy.ndarray
        '''

        xBarePos = self.xBarePos
        yBarePos = self.yBarePos
        current = self.current
        nConductors = self.nco
        imag = self.imag

        wBare = conductorSigma.wBare
        hInBare = conductorSigma.hInBare
        hOutBare = conductorSigma.hOutBare
        noOfStrands = conductorSigma.noOfStrands
        nColumns = conductorSigma.noOfStrandsPerLayer
        nLayers = conductorSigma.noOfLayers

        #     print('conductorSigma.name = {}'.format(conductorSigma.name))
        #     print('wBare = {}'.format(wBare))
        #     print('hInBare = {}'.format(hInBare))
        #     print('hOutBare = {}'.format(hOutBare))
        #     print('wInsulNarrow = {}'.format(wInsulNarrow))
        #     print('wInsulWide = {}'.format(wInsulWide))

        # Define x/y strand positions
        xS = []
        yS = []
        iS = []
        for c in range(nConductors):
            x2Bare, y2Bare = xBarePos[c][1], yBarePos[c][1]
            x3Bare, y3Bare = xBarePos[c][2], yBarePos[c][2]
            alpha = math.atan2(y3Bare - y2Bare, x3Bare - x2Bare)

            for r in range(nLayers):
                for c in range(nColumns):
                    if imag == 0:
                        xStrand = x2Bare + wBare / nColumns * (c + 1 / 2) * math.cos(alpha) - (
                                    hInBare + (hOutBare - hInBare) * (c + 1 / 2) / nColumns) * (
                                              r + 1 / 2) / nLayers * math.sin(alpha)
                        yStrand = y2Bare + wBare / nColumns * (c + 1 / 2) * math.sin(alpha) + (
                                    hInBare + (hOutBare - hInBare) * (c + 1 / 2) / nColumns) * (
                                              r + 1 / 2) / nLayers * math.cos(alpha)
                    elif imag == 1:
                        xStrand = x2Bare + wBare / nColumns * (c + 1 / 2) * math.cos(alpha) + (
                                    hInBare + (hOutBare - hInBare) * (c + 1 / 2) / nColumns) * (
                                              r + 1 / 2) / nLayers * math.sin(alpha)
                        yStrand = y2Bare + wBare / nColumns * (c + 1 / 2) * math.sin(alpha) - (
                                    hInBare + (hOutBare - hInBare) * (c + 1 / 2) / nColumns) * (
                                              r + 1 / 2) / nLayers * math.cos(alpha)

                    currentStrand = current / noOfStrands

                    xS.append(xStrand)
                    yS.append(yStrand)
                    iS.append(currentStrand)

        #                 print(len(xS))
        #                 print(x2Bare)
        #                 print(y2Bare)
        #                 print(alpha/math.pi*180)
        #                 print()

        # Set calculated values as attributes of BlockParameter object
        self.setXYStrandPosAndCurrent(xS, yS, iS)

        return xS, yS, iS


    def makeReturnBlock(self, N, n):
        '''
            **Make a conductor block with the return lines of the original block, according to a N-order multiple symmetry**

            Function returns a BlockParameter object that defines the conductor block with the return lines of the original block

            :param N: symmetry order (N=1: Dipole; N=2: Quadrupole; N=3: Sextupole;...)
            :type N: int
            :param n: index that will be assigned to the block as noBlock attribute
            :type n: int

            :return: BlockParameter
        '''

        returnBlock = BlockParameters(noBlock=n,
                                      typeBlock=self.typeBlock,
                                      nco=self.nco,
                                      radius=self.radius,
                                      phi=self.phi,
                                      alpha=self.alpha,
                                      current=-self.current,  # NOTE THE CHANGE
                                      condname=self.condname,
                                      n1=self.n1,
                                      n2=self.n2,
                                      imag=1 - self.imag,  # NOTE THE CHANGE (this will switch between +1 and 0)
                                      turn=self.turn + 360 / (2 * N),  # NOTE THE CHANGE
                                      )

        return returnBlock