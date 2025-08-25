
from __future__ import annotations
from typing import List
from gadget import Gadget, GadgetError


class NOT(Gadget):
    def _validate_arity(self) -> None:
        if len(self.input_names) != 1 or len(self.output_names) != 1:
            raise GadgetError(f"{self.gid}: NOT requiere 1 entrada y 1 salida")

    def _evaluate_defined(self, in_values: List[bool]) -> List[bool]:
        return [not in_values[0]]


class AND(Gadget):
    def _validate_arity(self) -> None:
        if len(self.input_names) != 2 or len(self.output_names) != 1:
            raise GadgetError(f"{self.gid}: AND requiere 2 entradas y 1 salida")

    def _evaluate_defined(self, in_values: List[bool]) -> List[bool]:
        return [in_values[0] and in_values[1]]


class OR(Gadget):
    def _validate_arity(self) -> None:
        if len(self.input_names) != 2 or len(self.output_names) != 1:
            raise GadgetError(f"{self.gid}: OR requiere 2 entradas y 1 salida")

    def _evaluate_defined(self, in_values: List[bool]) -> List[bool]:
        return [in_values[0] or in_values[1]]


class NAND(Gadget):
    def _validate_arity(self) -> None:
        if len(self.input_names) != 2 or len(self.output_names) != 1:
            raise GadgetError(f"{self.gid}: NAND requiere 2 entradas y 1 salida")

    def _evaluate_defined(self, in_values: List[bool]) -> List[bool]:
        return [not (in_values[0] and in_values[1])]
