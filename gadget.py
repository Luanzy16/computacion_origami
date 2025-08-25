
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Iterable, Tuple
from pleat import Pleat, Signal


class GadgetError(Exception):
    pass


@dataclass
class Gadget:
    """
    Gadget base: bloque lógico con listas de nombres de Entrada/Salida.
    Las conexiones reales a objetos Pleat las resuelve la Network.
    """
    gid: str
    input_names: List[str]
    output_names: List[str]

    # Conexiones resueltas por la Network:
    inputs: List[Pleat] = field(default_factory=list, init=False)
    outputs: List[Pleat] = field(default_factory=list, init=False)

    def bind(self, name_to_pleat: Dict[str, Pleat]) -> None:
        self.inputs = [name_to_pleat[n] for n in self.input_names]
        self.outputs = [name_to_pleat[n] for n in self.output_names]
        self._validate_arity()

    # Política de indefinidos: si alguna entrada es None, deja salidas en None.
    undefined_policy: str = "propagate_none"  # o "raise"

    def _validate_arity(self) -> None:
        # Por defecto no impone aridad específica; las subclases sí.
        pass

    def evaluate(self) -> None:
        """
        Calcula las salidas a partir de entradas según la política.
        Subclases deben implementar _evaluate_defined(inputs)->list[bool].
        """
        if any(p.value is None for p in self.inputs):
            if self.undefined_policy == "raise":
                raise GadgetError(f"{self.gid}: entrada indefinida")
            # Deja salidas en None
            for o in self.outputs:
                o.value = None
            return

        in_values = [bool(p.value) for p in self.inputs]
        out_values = self._evaluate_defined(in_values)
        if len(out_values) != len(self.outputs):
            raise GadgetError(f"{self.gid}: número de salidas no coincide")
        for pleat, val in zip(self.outputs, out_values):
            pleat.value = bool(val)

    # Método a implementar en subclases
    def _evaluate_defined(self, in_values: List[bool]) -> List[bool]:
        raise NotImplementedError
    
    def __hash__(self):
        return id(self)
