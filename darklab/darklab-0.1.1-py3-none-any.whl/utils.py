CONST_LBS: float = 2.205
CONST_FAHRENHEIT: float = 1.8
CONST_FEET: float = 3.2808


class Utils:
    # F = (C * 1.8) +32
    @staticmethod
    def celsius_to_fahrenheit(celsius: float = 0.0):
        return (celsius * CONST_FAHRENHEIT) + 32

    # C = (F - 32) / 1.8
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float = 32.0):
        return (fahrenheit - 32) / CONST_FAHRENHEIT

    # IMC = Kg / (m * m)
    @staticmethod
    def calc_imc_kg_cm(weight: float = 60, height: float = 170):
        return Utils.calc_imc(weight, Utils.cm_to_m(height))

    @staticmethod
    def calc_imc_lb_ft(weight: float = 132.3, height: float = 5.6):
        return Utils.calc_imc(Utils.lb_to_kg(weight), Utils.ft_to_m(height))

    @staticmethod
    def calc_imc(weight: float = 60, height: float = 1.7):
        return weight / (height * height)

    @staticmethod
    def kg_to_lb(kg: float = 60):
        return kg * CONST_LBS

    @staticmethod
    def lb_to_kg(lb: float = 132.3):
        return lb / CONST_LBS

    @staticmethod
    def m_to_ft(m: float = 1.7):
        return m * CONST_FEET

    @staticmethod
    def ft_to_m(ft: float = 5.6):
        return ft / CONST_FEET

    @staticmethod
    def cm_to_ft(cm: float = 170.0):
        return (cm / 100) * CONST_FEET

    @staticmethod
    def ft_to_cm(ft: float = 5.6):
        return (ft / CONST_FEET) * 100

    @staticmethod
    def cm_to_m(cm: float = 0):
        return cm / 100

    @staticmethod
    def m_to_cm(m: float = 0):
        return m * 100
