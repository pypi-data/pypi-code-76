import math

import numpy as np


class EquationSystem:
    """
    Система линейных уравнений, класс для решения системы матричным способом
    """

    def __init__(self,
                 a_matrix: np.ndarray,
                 l_matrix: np.ndarray = None,
                 p_matrix: np.ndarray = None):

        self._a_matrix = a_matrix
        self._l_matrix = l_matrix
        self._p_matrix = p_matrix

    def normalize(self) -> tuple:
        """
        Приведение системы линейных уравнений к нормальному виду
        :return: Нормальная матрица A, Нормальная матрица L
        """
        # Проверка системы на неравноточные измерения
        if self._p_matrix is None:
            rows, _ = np.shape(self._a_matrix)
            self._p_matrix = np.eye(rows)

        # Приведении системы уравнений к нормальному виду
        a_matrix_transposed = self._a_matrix.transpose()
        normal_coefficient = a_matrix_transposed.dot(self._p_matrix)
        normal_a_matrix = normal_coefficient.dot(self._a_matrix)
        if self._l_matrix is not None:
            normal_l_matrix = normal_coefficient.dot(self._l_matrix)
        else:
            normal_l_matrix = None
        return normal_a_matrix, normal_l_matrix

    def solve(self) -> tuple:
        """
        Решение системы нормальных уравнений и вычисление вектора поправок
        :return: Матрица неизвестных нормальных уравнений X, Решение исходной системы уоавнений V
        """
        normal_a_matrix, normal_l_matrix = self.normalize()
        if normal_l_matrix is not None:
            # Решение системы нормальных уравнений
            x_matrix = np.linalg.solve(normal_a_matrix, -normal_l_matrix)
            # Вычисление матрицы поправок
            v_matrix = self._a_matrix.dot(x_matrix) + self._l_matrix
            return x_matrix, v_matrix
        else:
            raise ValueError("l_matrix is None")

    def errors(self, extra_measures: int) -> np.ndarray:
        """
        Вычисление ковариационной матрицы системы нормальных линейных уравнений
        :return: Ковариационная матрица К
        """
        # Оценка точности решения системы нормальных уравнений
        # Вычисление обратной весовой матрицы

        normal_a_matrix, _ = self.normalize()
        q_matrix = np.linalg.inv(normal_a_matrix)

        _, v_matrix = self.solve()

        # Вычисление СКП единицы веса
        v_matrix_transposed = v_matrix.transpose()
        normal_coefficient = v_matrix_transposed.dot(self._p_matrix)
        pvv_sum = normal_coefficient.dot(v_matrix)
        mu = math.sqrt(pvv_sum / extra_measures)

        # Вычисление ковариационной матрицы К
        k_matrix = mu ** 2 * q_matrix
        return k_matrix

    def condition(self) -> float:
        """
        Вычисление числа обусловленности задачи
        :return: nu
        """
        normal_a_matrix, _ = self.normalize()
        # Эвквидова норма матриц А и А-1
        norma_a = math.sqrt(np.sum(normal_a_matrix ** 2))
        norma_a_inv = math.sqrt(np.sum(np.linalg.inv(normal_a_matrix) ** 2))
        nu = norma_a * norma_a_inv
        return nu

