from .Core import Core, clear

__core = Core()

intro = \
"""
+------------- CUBITUS ROBOTIC ARM -------------+
|                 TUKE FEI KKUI                 |
+------------- USER INTERFACE v1.3 -------------+

   Enter \'help\' to show list of all comands.   
"""

helpstr = \
"""
>> help         Shows all commands.
>> loadxml      Loads user defined XML into system. (needs external command)
>> fold         Folds the arm to its initial position.
>> grip         Sets gripper state to *hold* position. (default)
>> ungrip       Sets gripper state to *open* position.
>> eefangle     Sets end effector angle (X Y Z angles).
>> perform      Perform a specific movement based on input.
>> equation     Perform a custom curve based on input.
>> about        Show application info.
>> reset        Reset application.
>> clear        Clear terminal.
>> exit         Exit interface.
"""

about = \
"""
+--------------------------------------+
|      C.U.B.I.T.U.S. Robotic Arm      |
| Developed by Oliver Kudzia 2020/2021 |
| TUKE FEI KKUI ~> Intelligent Systems |
|          (c) Copyright 2021          |
+--------------------------------------+
"""

def fold_arm():
    """
    Folds the arm to its initial position.

    This calibrates the joints of the arm to predefined folded position.
    """
    __core.FoldArm()

def set_end_effector(unit: str, rho=0.0, omega=0.0, tau=0.0):
    """
    Sets end effector to specific angles (degrees or radians).

    If only 'unit' parameter is given, sets the default angle [0°, 0°, 0°]

    Parameters
    ----------
    unit : str
        'degrees' or 'radians'
    rho, omega, tau : float
        angle values (one for each axis)
    """
    __core.SetEndEffector(unit, rho, omega, tau)

def set_gripper(is_grabbed: bool):
    """
    Sets end effector gripper state.

    ->If true, end effector gripper hold its grasp.
    ->If false the gripper is opened.

    Parameters
    ----------
    is_grabbed : bool
        end effector gripper state
    """
    __core.SetGripper(is_grabbed)

def load_xml(fileName: str, name: str):
    """
    Loads XML file depending on where the file is located.

    ->Note that XML file must be in correct format and in the same directory as python script.
    ->Otherwise fails to proceed.

    Parameters
    ----------
    name : str
        name of the file (e.g. 'cubitus.xml' or 'cubitus')
    """
    if not isinstance(fileName, str) or not isinstance(name, str): raise TypeError("Name and filename must be declared as strings!")
    if fileName != "__file__": print("Parameter fileName MUST be '__file__' because it determines .xml file relativity!"); exit()
    if ".xml" in name: __core.LoadXML(fileName, name[:-4])
    else: __core.LoadXML(fileName, name)

def move_to_point(x: float, y: float, z: float):
    """
    Moves the robotic arm to designated position.

    Depending on OS (Windows / Linux):
    ->Windows:\tplots the result using matplotlib
    ->Linux:\tphysically moves with the arm itself

    Parameters
    ----------
    x, y, z : float or int
        carthesian coordinates for each axis (X, Y, Z)
    """
    __core.PerformPoint([x, y, z])

def perform_line(pointA: list, pointB: list, sampling=50, repeat=1):
    """
    Performs a line and move robotic arm towards computed positions.

    Depending on OS (Windows / Linux):
    ->Windows:\tplots the result using matplotlib
    ->Linux:\tphysically moves with the arm itself

    Parameters
    ----------
    pointA, pointB : list
        points between which a line will be performed
    """
    __core.PerformLine(pointA, pointB, sampling, repeat)

def perform_circle(pointA: list, pointB: list, pointC: list, sampling=50, repeat=1):
    """
    Performs a circle which is formed by 3 carthesian points and move robotic arm towards computed positions.

    Depending on OS (Windows / Linux):
    ->Windows:\tplots the result using matplotlib
    ->Linux:\tphysically moves with the arm itself

    Parameters
    ----------
    pointA, pointB, pointC : list
        points between which a circle will be performed
    """
    __core.PerformCircle(pointA, pointB, pointC, sampling, repeat)

def perform_parabola(quadratic: float, height: int, vertex: float, sampling=50, repeat=1):
    """
    Performs a parabola which is formed by 3 parameters and move robotic arm towards computed positions.

    Depending on OS (Windows / Linux):
    ->Windows:\tplots the result using matplotlib
    ->Linux:\tphysically moves with the arm itself

    Parameters
    ----------
    quadratic, vertex : float
    height : int
        parameters defining parabola which will be performed
    """
    __core.PerformParabola(quadratic, height, vertex, sampling, repeat)

def perform_bezier(pointA: list, pointB: list, pointC: list, sampling=50, repeat=1):
    """
    Performs a bezier curve which is formed by 3 carthesian points and move robotic arm towards computed positions.

    Depending on OS (Windows / Linux):
    ->Windows:\tplots the result using matplotlib
    ->Linux:\tphysically moves with the arm itself

    Parameters
    ----------
    pointA, pointB, pointC : list
        points between which a bezier curve will be performed
    """
    __core.PerformBezier(pointA, pointB, pointC, sampling, repeat)

def perform_custom_curve(Xequation: str, Yequation: str, Zequation: str, sampling=50, repeat=1):
    """
    Performs specific curve with respect to given equations.

    Parameters
    ----------
    sampling : int
        precision of a movement, determines on how many
        pieces is movement broken into
    repeat : int
        how many times should be specific shape performed
    """
    __core.PerformCustomCurve(Xequation, Yequation, Zequation, sampling, repeat)

def run_ui():
    """
    Opens user interface which acts like a simple command terminal.
    """

    def SetEndEffectorAngle():
        print("Insert end effector angles IN DEGREES:")
        ro = input(">> ro\t\t: ")
        omega = input(">> omega\t: ")
        tau = input(">> tau\t\t: ")
        print()
        set_end_effector("degrees", float(ro), float(omega), float(tau))

    def Perform():
        print("What type of shape do you want to perform?\nPossible options:\n• point\n• line\n• circle\n• parabola\n• bezier\n")
        shapeType = input(">> ")
        print()
        if shapeType != "point":
            print("What sampling do you want (means how many IK positions of selected shape will be computed)?\n• insert a whole number from interval <10; 100>\n")
            sampling = int(input(">> "))
            print()
            print("How many times do you want to perform this movement?\n• a whole number from interval <1; inf>\n")
            count = int(input(">> "))
            __core.PerformUIGeometricShape(shape=shapeType, sampling=sampling, repeat=count)
        else: __core.PerformUIGeometricShape(shape=shapeType, sampling=10, repeat=1)

    def PerformEquation():
        print("What sampling do you want (means how many IK positions of selected shape will be computed)?\n• insert a whole number from interval <10; 100>\n")
        sampling = int(input(">> "))
        print()
        print("How many times do you want to perform this movement?\n• a whole number from interval <1; inf>\n")
        count = int(input(">> "))
        __core.PerformUICustomCurve(sampling=sampling, repeat=count)

    print(intro)
    try:
        while True:
            userInput = input('>>  ').lower()
            if userInput == '': pass
            elif userInput == 'help':       print(helpstr)
            elif userInput == 'loadxml':    print("To load custom XML file you need to run 'load_xml()' command.")
            elif userInput == 'fold':       fold_arm()
            elif userInput == 'grip':       set_gripper(True)
            elif userInput == 'ungrip':     set_gripper(False)
            elif userInput == 'eefangle':   SetEndEffectorAngle()
            elif userInput == 'perform':    Perform()
            elif userInput == 'equation':   PerformEquation()
            elif userInput == 'about':      print(about)
            elif userInput == 'reset':      fold_arm(); clear(); print(intro)
            elif userInput == 'clear':      clear()
            elif userInput == 'exit':       fold_arm(); break
            else: print('Unknown command.')
    except KeyboardInterrupt: fold_arm(); clear(); exit()
