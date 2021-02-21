from abc import ABCMeta, abstractmethod

import numpy as np

from chi1chi2.utils.constants import ChiException, simeq

POLAR = "alpha"
HYPER = "beta"
CHI1 = "chi1"
CHI2 = "chi2"

__LARGE_NUMBER = 1000
NUMBBER_OF_DIGITS = 5
TOLERANCE = np.math.pow(10, -NUMBBER_OF_DIGITS)
FLOAT_FORMAT = "{: ." + str(NUMBBER_OF_DIGITS) + "f}"


def _get_zero_or_number(u):
    return 0 if simeq(u, 0, TOLERANCE) else u


class TensorialProperty(metaclass=ABCMeta):
    @abstractmethod
    def transform(self, rotation):
        pass


class FirstOrdPolTens(TensorialProperty):
    def __init__(self, vector):
        if not type(vector) is np.ndarray and vector.shape != (3,):
            raise ChiException("first order polar tensor should be a one-dimensional numpy array of size 3")
        self.vector = vector

    @classmethod
    def zero(cls):
        return cls(np.zeros(3))

    def transform(self, rotation):
        transformed = np.zeros(3)
        for i in range(3):
            for j in range(3):
                transformed[i] += self.vector[j] * rotation[j, i]
        return Vector(transformed)

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, FirstOrdPolTens):
            return False
        if other is self:
            return True
        return all(simeq(self.vector[i], other.vector[i]) for i in range(3))

    @classmethod
    def from_line(cls, line: str):
        try:
            return cls(np.array([float(u) for u in line.split()[:3]]))
        except ValueError:
            # print(f"first order tensor ignored")
            return cls(np.zeros(3))

    def __repr__(self):
        return ' '.join(str(FLOAT_FORMAT.format(_get_zero_or_number(u))) for u in self.vector) + '\n'


class Vector(FirstOrdPolTens):
    pass


class PermanentPolarization(FirstOrdPolTens):
    def __repr__(self):
        # not implemented, used as a stub for title of bulk properties
        return "bulk properties\n"


class SecOrdPolTen(TensorialProperty):
    def __init__(self, tensor, name):
        if not type(tensor) is np.ndarray and tensor.shape != (3, 3):
            raise ChiException("second-order tensor should be two-dimensional numpy array of size (3, 3)")
        self.tensor = tensor
        self.name = name

    def transform(self, rotation):
        transformed = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        transformed[i, j] += self.tensor[k, l] * rotation[k, i] * rotation[l, j]
        return SecOrdPolTen(transformed, self.name)

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, SecOrdPolTen):
            return False
        if other is self:
            return True
        return all(simeq(self.tensor.reshape(9)[i], other.tensor.reshape(9)[i]) for i in range(9))

    @classmethod
    def from_lines(cls, lines: list):
        if len(lines) != 3:
            raise ChiException("wrong number of lines for reading second-order tensor")
        raw_polar = []
        for i in range(3):
            raw_polar.extend(float(u) for u in lines[i].split()[:3])
        return cls(np.array(raw_polar).reshape((3, 3)))

    def __repr__(self):
        lines = ""
        for i in range(3):
            lines += ' '.join(str((FLOAT_FORMAT.format(_get_zero_or_number(u)))) for u in self.tensor[i, :]) + '\n'
        return lines

    @classmethod
    def zero(cls, name):
        return cls(np.zeros(9).reshape((3, 3)), name)


class Polar(SecOrdPolTen):
    def __init__(self, tensor):
        super().__init__(tensor, POLAR)

    def to_distributed(self, N: int):
        partial_polar = Polar(self.tensor / N)
        return DistributedPolar([partial_polar for i in range(N)])

    def transform(self, rotation):
        return Polar(super().transform(rotation).tensor)


def _is_not_symmetric_3x3(tensor):
    for i, j in ((0, 1), (0, 2), (1, 2)):
        if not simeq(tensor[i, j], tensor[j, i]):
            return True
    return False


def _max_out_of_diagonal(tensor: np.ndarray):
    return max(abs(tensor[ij]) for ij in ((0, 1), (0, 2), (1, 2)))


def _get_min_ij(tensor: np.ndarray):
    return min(((0, 1), (2, 0), (1, 2)),
               key=lambda ij: abs(tensor[ij]) if abs(tensor[ij]) > TOLERANCE else __LARGE_NUMBER)


def diagonalize(tensor: np.ndarray):
    if _is_not_symmetric_3x3(tensor):
        raise ChiException("non-symmetric 2nd rank tensor provided")
    rotation = np.identity(3)

    while _max_out_of_diagonal(tensor) > TOLERANCE:
        i, j = _get_min_ij(tensor)
        rot = _get_rotation_ij(tensor, i, j)
        rotation = np.dot(rotation, rot)
        tensor = np.dot(rot.T, np.dot(tensor, rot))

    return rotation, tensor


def _get_rotation_ij(tensor, i, j):
    if abs((tensor[i, i] - tensor[j, j])) < TOLERANCE:
        th = np.pi / 180.
    else:
        th = .5 * np.arctan(2 * tensor[i, j] / (tensor[i, i] - tensor[j, j]))
    rot = np.identity(3)
    rot[i, i] = np.cos(th)
    rot[j, j] = np.cos(th)
    rot[i, j] = -np.sin(th)
    rot[j, i] = np.sin(th)
    return rot


class Chi(SecOrdPolTen):
    def __init__(self, tensor):
        super().__init__(tensor, CHI1)

    def transform(self, rotation):
        return Chi(super().transform(rotation).tensor)

    def refr_ind_rot_mat(self, initial_rotation=None):
        eps = self.tensor + np.identity(3)
        if initial_rotation is None:
            rotation, diagonalized = diagonalize(eps)
        else:
            pre_rotated_eps = np.dot(initial_rotation.T, np.dot(eps, initial_rotation))
            rotation2, diagonalized = diagonalize(pre_rotated_eps)
            rotation = np.dot(initial_rotation, rotation2)
        refr_ind = np.sqrt(np.diag(diagonalized)).tolist()
        return refr_ind, rotation


class DistributedPolar(TensorialProperty):
    def __init__(self, polar_list):
        self.polar_list = polar_list

    @classmethod
    def from_file(cls, file, legacy=False):
        with open(file) as f:
            lines = f.readlines()
        polar_list = []
        if legacy:
            _extract_legacy_polarizabilities(lines, polar_list)
        else:
            _extract_polarizabilities(lines, polar_list)
        return cls(polar_list)

    def to_molecular_polar(self):
        return Polar(sum(u.tensor for u in self.polar_list))

    def transform(self, rotation):
        return DistributedPolar([polar.transform(rotation) for polar in self.polar_list])


def _extract_legacy_polarizabilities(lines, polar_list):
    for line in lines:
        tokens = line.split()
        raw_polar = np.zeros((3, 3))
        for i in range(3):
            raw_polar[i, i] = float(tokens[i + 3])
        raw_polar[0, 1] = np.average([float(tokens[u]) for u in (6, 7)])
        raw_polar[1, 0] = raw_polar[0, 1]
        raw_polar[0, 2] = np.average([float(tokens[u]) for u in (8, 9)])
        raw_polar[2, 0] = raw_polar[0, 2]
        raw_polar[1, 2] = np.average([float(tokens[u]) for u in (10, 11)])
        raw_polar[2, 1] = raw_polar[1, 2]
        polar_list.append(Polar(raw_polar))


def _extract_polarizabilities(lines, polar_list):
    for line in lines:
        tokens = line.split()
        raw_polar = np.zeros((3, 3))
        for i, ij in enumerate(((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))):
            raw_polar[ij] = float(tokens[i])
        for ij in ((0, 1), (0, 2), (1, 2)):
            raw_polar[ij[1], ij[0]] = raw_polar[ij]
        polar_list.append(Polar(raw_polar))


class ThirdOrdPolarTensor(TensorialProperty):
    def __init__(self, tensor, name):
        if not type(tensor) is np.ndarray and tensor.shape != (3, 3, 3):
            raise ChiException("third order tensor should be three-dimensional numpy array of size (3, 3, 3)")
        self.tensor = tensor
        self.name = name

    def transform(self, rotation):
        transformed = np.zeros((3, 3, 3))
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        for m in range(3):
                            for n in range(3):
                                transformed[i, j, k] += self.tensor[l, m, n] * rotation[l, i] * rotation[
                                    m, j] * rotation[n, k]
        return ThirdOrdPolarTensor(transformed, self.name)

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, ThirdOrdPolarTensor):
            return False
        if other is self:
            return True
        return all(simeq(self.tensor.reshape(27)[i], other.tensor.reshape(27)[i]) for i in
                   range(27))

    @classmethod
    def from_lines(cls, lines: list):
        if len(lines) != 9:
            raise ChiException("wrong number of lines for reading of third-order polar tensor")
        raw_hyper = []
        for i in range(9):
            raw_hyper.extend(float(u) for u in lines[i].split()[:3])
        return cls(np.array(raw_hyper).reshape((3, 3, 3)))

    def __repr__(self):
        lines = ""
        for i in range(3):
            for j in range(3):
                lines += ' '.join(
                    str((FLOAT_FORMAT.format(_get_zero_or_number(u)))) for u in self.tensor[i, j, :]) + '\n'
        return lines

    @classmethod
    def zero(cls, name):
        return cls(np.zeros(27).reshape((3, 3, 3)), name)


class Hyper(ThirdOrdPolarTensor):
    def __init__(self, tensor):
        super().__init__(tensor, CHI2)

    def transform(self, rotation):
        return Hyper(super().transform(rotation).tensor)

    def to_distributed(self, N: int):
        partial_hyper = Hyper(self.tensor / N)
        return DistributedHyper([partial_hyper for i in range(N)])


class Chi2(ThirdOrdPolarTensor):
    def __init__(self, tensor):
        super().__init__(tensor, CHI2)

    def transform(self, rotation):
        return Chi2(super().transform(rotation).tensor)


class DistributedHyper(TensorialProperty):
    def __init__(self, hyper_list):
        self.hyper_list = hyper_list

    def to_molecular_hyper(self):
        return Hyper(sum(u.tensor for u in self.hyper_list))

    def transform(self, rotation):
        return DistributedHyper([hyper.transform(rotation) for hyper in self.hyper_list])


class Lorentz:
    def __init__(self, lorentz_tensor: np.array):
        if lorentz_tensor.shape[0] != lorentz_tensor.shape[1]:
            raise ChiException(f"Lorentz tensor should be a square matrix! Actual shape {lorentz_tensor.shape[0]} x "
                               f"{lorentz_tensor.shape[1]}")
        self.lorentz_tensor = lorentz_tensor
        # self.lorentz_tensor = np.identity(276) / 3.
        self.dimension = lorentz_tensor.shape[0]

    @classmethod
    def from_file(cls, file):
        with open(file) as f:
            lines = f.readlines()
        if lines[1].find("results not fully converged") > -1:
            raise ChiException("Lorentz tensor not converged, most problem with input, if OK increase r_cut")
        current_line = 2
        l_tmp = []
        while current_line < len(lines):
            l_tmp.append(_get_tensor_from_line(lines[current_line]))
            current_line += 1
        number_of_submolecules = _get_number_of_submolecules(len(l_tmp))
        L = np.zeros((number_of_submolecules * 3, number_of_submolecules * 3))
        current_lorentz_ind = 0
        for i in range(number_of_submolecules):
            for j in range(i, number_of_submolecules):
                L[3 * i:3 * (i + 1), 3 * j:3 * (j + 1)] = l_tmp[current_lorentz_ind][:, :]
                if i != j:
                    L[3 * j:3 * (j + 1), 3 * i:3 * (i + 1)] = l_tmp[current_lorentz_ind][:, :]
                current_lorentz_ind += 1
        return cls(L)

    def __eq__(self, other):
        if other is None or not isinstance(other, Lorentz):
            return False
        if other is self:
            return True
        dimsq = self.dimension ** 2
        return all([simeq(self.lorentz_tensor.reshape(dimsq)[i], other.lorentz_tensor.reshape(dimsq)[i]) for i in
                    range(dimsq)])


def _get_tensor_from_line(line):
    L = np.zeros((3, 3))
    indices = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
    tokens = line.split()[:6]
    for i, tk in enumerate(indices):
        L[indices[i]] = float(tokens[i])
    for ind in ((0, 1), (0, 2), (1, 2)):
        L[ind[1], ind[0]] = L[ind[0], ind[1]]
    return L


def _get_number_of_submolecules(number_of_lines: int) -> int:
    return int((np.sqrt(1 + 8 * number_of_lines) - 1) / 2)
