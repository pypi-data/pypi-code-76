
STANDARD_ROBDEF_NAMES = [
    'com.robotraconteur.action',
    'com.robotraconteur.actuator',
    'com.robotraconteur.bignum',
    'com.robotraconteur.color',
    'com.robotraconteur.datatype',
    'com.robotraconteur.datetime.clock',
    'com.robotraconteur.datetime',
    'com.robotraconteur.device.clock',
    'com.robotraconteur.device.isoch',
    'com.robotraconteur.device',
    'com.robotraconteur.eventlog',
    'com.robotraconteur.geometry',
    'com.robotraconteur.geometry.shapes',
    'com.robotraconteur.geometryf',
    'com.robotraconteur.geometryi',
    'com.robotraconteur.gps',
    'com.robotraconteur.hid.joystick',
    'com.robotraconteur.identifier',
    'com.robotraconteur.image',
    'com.robotraconteur.imaging.camerainfo',
    'com.robotraconteur.imaging',
    'com.robotraconteur.imu',
    'com.robotraconteur.laserscan',
    'com.robotraconteur.laserscanner',
    'com.robotraconteur.lighting',
    'com.robotraconteur.objectrecognition',
    'com.robotraconteur.octree',
    'com.robotraconteur.param',
    'com.robotraconteur.pid',
    'com.robotraconteur.pointcloud',
    'com.robotraconteur.pointcloud.sensor',
    'com.robotraconteur.resource',
    'com.robotraconteur.robotics.joints',
    'com.robotraconteur.robotics.payload',
    'com.robotraconteur.robotics.planning',
    'com.robotraconteur.robotics.robot',
    'com.robotraconteur.robotics.scene',
    'com.robotraconteur.robotics.tool',
    'com.robotraconteur.robotics.trajectory',
    'com.robotraconteur.sensor',
    'com.robotraconteur.sensordata',
    'com.robotraconteur.servo',
    'com.robotraconteur.signal',
    'com.robotraconteur.units',
    'com.robotraconteur.uuid'
]

STANDARD_ROBDEF_TEXT={}

def _load_standard_robdef_text():
    import importlib_resources
    for n in STANDARD_ROBDEF_NAMES:
        robdef_text = importlib_resources.read_text(__package__, n + '.robdef')
        STANDARD_ROBDEF_TEXT[n] = robdef_text

_load_standard_robdef_text()

def RegisterStdRobDefServiceTypes(node):
    robdefs_text = list(STANDARD_ROBDEF_TEXT.values())
    node.RegisterServiceTypes(robdefs_text)