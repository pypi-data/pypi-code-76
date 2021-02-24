# encoding: utf8
from ordered_enum import OrderedEnum
from enum import Enum


class EnumChannelBand(OrderedEnum):
    F = 'F'
    G = 'G'
    D = 'D'
    C = 'C'
    E = 'E'
    S = 'S'
    H = 'H'
    B = 'B'
    M = 'M'
    L = 'L'
    V = 'V'
    U = 'U'
    R = 'R'
    P = 'P'
    T = 'T'
    Q = 'Q'
    A = 'A'
    O = 'O'


class EnumChannelInstrument(Enum):
    H = 'H'  # High gain seismometer
    L = 'L'  # Low gain seismometer
    G = 'G'  # Gravimeter
    M = 'M'  # Mass position seismometer
    N = 'N'  # Accelerometer
    A = 'A'  # Tilt meter
    B = 'B'  # Creep meter
    C = 'C'  # Calibration input
    D = 'D'  # Pressure
    E = 'E'  # Electronic test point
    F = 'F'  # Magnetometer
    I = 'I'  # Humidity
    J = 'J'  # High gain seismometer
    K = 'K'  # Temperature
    O = 'O'  # Water current
    P = 'P'  # Geophone
    Q = 'Q'  # Electric potential
    R = 'R'  # Rainfall
    S = 'S'  # Linear strain
    T = 'T'  # Tide
    U = 'U'  # Bolometer
    V = 'V'  # Volumetric strain
    W = 'W'  # Wind
    X = 'X'  # Derived or generated channel
    Y = 'Y'  # Non-specific instrument
    Z = 'Z'  # Synthesized beams
