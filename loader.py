
from __future__ import annotations
from typing import Dict, Any, List, Tuple, Type
import json

from network import Network
from gadget import Gadget
from gadgets import AND, OR, NOT, NAND


GATE_MAP  = {
    "AND": AND,
    "OR": OR,
    "NOT": NOT,
    "NAND": NAND,
}


def load_circuit_from_json(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    # Diccionario de señales
    signals = {name: bool(val) for name, val in data["inputs"].items()}

    # Diccionario de compuertas
    gates = {}

    for gate in data["gates"]:
        gate_type = gate["type"]
        gate_class = GATE_MAP[gate_type]
        
        # Resolver entradas: pueden ser señales o salidas de otras compuertas
        inputs = []
        for inp in gate["inputs"]:
            if inp in signals:
                inputs.append(lambda s=signals[inp]: s)  
            else:
                inputs.append(lambda g=inp: gates[g].output())
        
        # Crear compuerta
        gates[gate["id"]] = gate_class(inputs)

    # Ejecutar y recolectar outputs
    outputs = {}
    for out in data["outputs"]:
        if out in gates:
            outputs[out] = gates[out].output()
        elif out in signals:
            outputs[out] = signals[out]

    return outputs
