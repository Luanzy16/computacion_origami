import json
from typing import Dict, Any, Type
from network import Network
from gadgets import AND, OR, NOT, NAND
from gadget import Gadget

# Registro de tipos
GATE_MAP: Dict[str, Type[Gadget]] = {
    "AND": AND,
    "OR": OR,
    "NOT": NOT,
    "NAND": NAND,
}

def load_circuit_from_json(json_file: str) -> Network:
    """Carga un circuito desde un archivo JSON y devuelve la Network lista."""
    with open(json_file, "r") as f:
        data = json.load(f)

    net = Network()

    # Crear pleats declarados
    for name in data.get("pleats", []):
        net.add_pleat(name)

    # Crear gadgets
    for gdesc in data.get("gadgets", []):
        gtype = gdesc["type"].upper()
        gid = gdesc["id"]
        cls = GATE_MAP.get(gtype)
        if not cls:
            raise ValueError(f"Gadget desconocido: {gtype}")
        gadget = cls(
            gid=gid,
            input_names=gdesc["inputs"],
            output_names=gdesc["outputs"]
        )
        net.add_gadget(gadget)

    # Fijar entradas iniciales
    if "inputs" in data:
        net.set_inputs(data["inputs"])

    return net
