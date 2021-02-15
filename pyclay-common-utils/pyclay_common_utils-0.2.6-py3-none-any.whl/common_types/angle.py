from __future__ import annotations
import math
import numpy as np
from typing import List
from ..check_utils import check_type_from_list
from ..constants import number_types
from scipy.spatial.transform import Rotation
from ..base.basic import BasicLoadableObject, BasicLoadableHandler, BasicHandler

class EulerAngle(BasicLoadableObject['EulerAngle']):
    def __init__(self, roll, pitch, yaw):
        super().__init__()
        check_type_from_list(item_list=[roll, pitch, yaw], valid_type_list=number_types)
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def __str__(self) -> str:
        return f"EulerAngle({self.roll},{self.pitch},{self.yaw})"

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, other: EulerAngle) -> EulerAngle:
        if isinstance(other, EulerAngle):
            return EulerAngle(roll=self.roll+other.roll, pitch=self.pitch+other.pitch, yaw=self.yaw+other.yaw)
        elif isinstance(other, (int, float)):
            return EulerAngle(roll=self.roll+other, pitch=self.pitch+other, yaw=self.yaw+other)
        else:
            raise TypeError

    def __sub__(self, other: EulerAngle) -> EulerAngle:
        if isinstance(other, EulerAngle):
            return EulerAngle(roll=self.roll-other.roll, pitch=self.pitch-other.pitch, yaw=self.yaw-other.yaw)
        elif isinstance(other, (int, float)):
            return EulerAngle(roll=self.roll-other, pitch=self.pitch-other, yaw=self.yaw-other)
        else:
            raise TypeError

    def __mul__(self, other) -> EulerAngle:
        if isinstance(other, (int, float)):
            return EulerAngle(roll=self.roll*other, pitch=self.pitch*other, yaw=self.yaw*other)
        else:
            raise TypeError

    def __truediv__(self, other) -> EulerAngle:
        if isinstance(other, (int, float)):
            return EulerAngle(roll=self.roll/other, pitch=self.pitch/other, yaw=self.yaw/other)
        else:
            raise TypeError

    def __eq__(self, other: EulerAngle) -> bool:
        if isinstance(other, EulerAngle):
            return self.roll == other.roll and self.pitch == other.pitch and self.yaw == other.yaw
        else:
            return NotImplemented

    def to_list(self) -> list:
        return [self.roll, self.pitch, self.yaw]

    @classmethod
    def from_list(self, val_list: list, from_deg: bool=False) -> EulerAngle:
        roll, pitch, yaw = val_list
        if from_deg:
            return EulerAngle(roll=roll*math.pi/180, pitch=pitch*math.pi/180, yaw=yaw*math.pi/180)
        else:
            return EulerAngle(roll=roll, pitch=pitch, yaw=yaw)
    
    def to_numpy(self) -> np.ndarray:
        return np.array(self.to_list())
    
    @classmethod
    def from_numpy(self, arr: np.ndarray, from_deg: bool=False) -> EulerAngle:
        return EulerAngle.from_list(arr.tolist(), from_deg=from_deg)

    def to_quaternion(self, seq: str='xyz') -> Quaternion:
        return Quaternion.from_list(Rotation.from_euler(seq=seq, angles=self.to_list()).as_quat().tolist())

    def to_deg(self, find_smallest_congruent: bool=False) -> EulerAngle:
        result = EulerAngle(roll=self.roll*180/math.pi, pitch=self.pitch*180/math.pi, yaw=self.yaw*180/math.pi)
        if find_smallest_congruent:
            result.roll = result.roll % 360
            if abs(result.roll - 360) < abs(result.roll):
                result.roll -= 360
            elif abs(result.roll + 360) < abs(result.roll):
                result.roll += 360
            result.pitch = result.pitch % 360
            if abs(result.pitch - 360) < abs(result.pitch):
                result.pitch -= 360
            elif abs(result.pitch + 360) < abs(result.pitch):
                result.pitch += 360
            result.yaw = result.yaw % 360
            if abs(result.yaw - 360) < abs(result.yaw):
                result.yaw -= 360
            elif abs(result.yaw + 360) < abs(result.yaw):
                result.yaw += 360
        return result
    
    def to_rad(self) -> EulerAngle:
        return EulerAngle(roll=self.roll*math.pi/180, pitch=self.pitch*math.pi/180, yaw=self.yaw*math.pi/180)

    def to_deg_list(self) -> list:
        return [val * 180 / math.pi for val in self.to_list()]
    
    def magnitude(self, degree: bool=False) -> float:
        mag = (self.roll**2 + self.pitch**2 + self.yaw**2)**0.5
        if degree:
            return mag * 180 / math.pi
        else:
            return mag

    # Note: This method is pointless.
    # def angle_from(self, other: EulerAngle, in_deg: bool=False) -> float:
    #     # Assume XYZ order
    #     assert isinstance(other, EulerAngle)
        
    #     def get_z_axis_vector(euler: EulerAngle, in_deg: bool=False) -> list:
    #         if in_deg:
    #             euler0 = euler.to_rad()
    #         else:
    #             euler0 = euler
    #         return [math.sin(euler0.pitch), -math.cos(euler0.pitch)*math.sin(euler0.roll), math.cos(euler0.pitch)*math.cos(euler0.roll)]
        
    #     Z0, Z1 = get_z_axis_vector(euler=self, in_deg=in_deg), get_z_axis_vector(euler=other, in_deg=in_deg)
    #     norm_cross = np.linalg.norm(np.cross(Z0, Z1)).tolist()
    #     dot = np.dot(Z0, Z1).tolist()
    #     result = math.atan2(norm_cross, dot)
    #     if in_deg:
    #         result *= 180 / math.pi
    #     return result

    def angle_from(self, other: EulerAngle, in_deg: bool=False) -> float:
        q0 = Rotation.from_euler('xyz', self.to_list(), degrees=in_deg)
        q1 = Rotation.from_euler('xyz', other.to_list(), degrees=in_deg)

        # sin(theta/2) = norm of the vector part of the quaternion product q1*q2^(-1)
        sin_theta_2 = q0*q1.inv()
        sin_theta_2 = sin_theta_2.as_quat() # 正規化
        sin_theta_2_vec = (sin_theta_2[0]**2+sin_theta_2[1]**2+sin_theta_2[2]**2)**0.5 # vector部のnorm

        angle = 2 * math.asin(sin_theta_2_vec)
        angle = math.degrees(angle)
        return angle

class EulerAngleList(
    BasicLoadableHandler['EulerAngleList', 'EulerAngle'],
    BasicHandler['EulerAngleList', 'EulerAngle']
):
    def __init__(self, angles: List[EulerAngle]=None):
        super().__init__(obj_type=EulerAngle, obj_list=angles)
        self.angles = self.obj_list
    
    @classmethod
    def from_dict_list(cls, dict_list: List[dict]) -> EulerAngleList:
        return EulerAngleList([EulerAngle.from_dict(item_dict) for item_dict in dict_list])

    def to_list(self) -> List[List[float]]:
        return [angle.to_list() for angle in self]

    @classmethod
    def from_list(cls, vals_list: List[List[float]]) -> EulerAngleList:
        return EulerAngleList([EulerAngle.from_list(vals) for vals in vals_list])

    def to_numpy(self) -> np.ndarray:
        return np.array(self.to_list())
    
    @classmethod
    def from_numpy(self, arr: np.ndarray) -> EulerAngleList:
        return EulerAngleList.from_list(arr.tolist())

class Quaternion(BasicLoadableObject['Quaternion']):
    def __init__(self, qw, qx, qy, qz):
        super().__init__()
        check_type_from_list(item_list=[qw, qx, qy, qz], valid_type_list=number_types)
        self.qw = qw
        self.qx = qx
        self.qy = qy
        self.qz = qz

    def __str__(self) -> str:
        return f"Quaternion({self.qw},{self.qx},{self.qy},{self.qz})"

    def __repr__(self) -> str:
        return self.__str__()

    def to_list(self) -> list:
        return [self.qw, self.qx, self.qy, self.qz]

    @classmethod
    def from_list(self, val_list: list) -> Quaternion:
        qw, qx, qy, qz = val_list
        return Quaternion(qw=qw, qx=qx, qy=qy, qz=qz)

    def to_numpy(self) -> np.ndarray:
        return np.array(self.to_list())
    
    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> Quaternion:
        return cls.from_list(arr.tolist())

    def to_euler(self, seq: str='xyz') -> EulerAngle:
        return EulerAngle.from_list(Rotation.from_quat(self.to_list()).as_euler(seq=seq).tolist())

class QuaternionList(
    BasicLoadableHandler['QuaternionList', 'Quaternion'],
    BasicHandler['QuaternionList', 'Quaternion']
):
    def __init__(self, angles: List[Quaternion]=None):
        super().__init__(obj_type=Quaternion, obj_list=angles)
        self.angles = self.obj_list
    
    @classmethod
    def from_dict_list(cls, dict_list: List[dict]) -> QuaternionList:
        return QuaternionList([Quaternion.from_dict(item_dict) for item_dict in dict_list])

    def to_list(self) -> List[List[float]]:
        return [angle.to_list() for angle in self]

    @classmethod
    def from_list(cls, vals_list: List[List[float]]) -> QuaternionList:
        return QuaternionList([Quaternion.from_list(vals) for vals in vals_list])
    
    def to_numpy(self) -> np.ndarray:
        return np.array(self.to_list())
    
    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> QuaternionList:
        return cls.from_list(arr.tolist())