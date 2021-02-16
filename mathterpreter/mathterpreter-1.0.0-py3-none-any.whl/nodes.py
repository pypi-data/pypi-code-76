from dataclasses import dataclass
import math


@dataclass
class Node:
    def evaluate(self) -> float:
        pass


@dataclass
class NumberNode(Node):
    value: float

    def __repr__(self):
        return str(self.value)

    def evaluate(self):
        return self.value


@dataclass
class PolarityNode(Node):
    node: Node


@dataclass
class PositiveNode(PolarityNode):
    def __repr__(self):
        return f"(+{self.node})"

    def evaluate(self) -> float:
        return +(self.node.evaluate())


@dataclass
class NegativeNode(PolarityNode):
    def __repr__(self):
        return f"(-{self.node})"

    def evaluate(self) -> float:
        return -(self.node.evaluate())


@dataclass
class OperationNode(Node):
    first_operand: Node
    second_operand: Node


@dataclass
class AdditionNode(OperationNode):
    def __repr__(self):
        return f"({self.first_operand}+{self.second_operand})"

    def evaluate(self):
        return self.first_operand.evaluate() + self.second_operand.evaluate()


@dataclass
class SubtractionNode(OperationNode):
    def __repr__(self):
        return f"({self.first_operand}-{self.second_operand})"

    def evaluate(self) -> float:
        return self.first_operand.evaluate() - self.second_operand.evaluate()


@dataclass
class MultiplicationNode(OperationNode):
    def __repr__(self):
        return f"({self.first_operand}*{self.second_operand})"

    def evaluate(self) -> float:
        return self.first_operand.evaluate() * self.second_operand.evaluate()


@dataclass
class DivisionNode(OperationNode):
    def __repr__(self):
        return f"({self.first_operand}/{self.second_operand})"

    def evaluate(self) -> float:
        try:
            return self.first_operand.evaluate() / self.second_operand.evaluate()
        except ZeroDivisionError:
            return math.inf


@dataclass
class RootNode(OperationNode):
    def __repr__(self):
        return f"({self.first_operand}√{self.second_operand})"

    def evaluate(self) -> float:
        return self.second_operand.evaluate() ** (1/self.first_operand.evaluate())


@dataclass
class ExponentiationNode(OperationNode):
    def __repr__(self):
        return f"({self.first_operand}^{self.second_operand})"

    def evaluate(self) -> float:
        return self.first_operand.evaluate() ** self.second_operand.evaluate()
