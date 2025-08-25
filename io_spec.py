
from __future__ import annotations
from typing import Dict, Any, List, Tuple, Type
import json

from network import Network
from gadget import Gadget
from gadgets import AND, OR, NOT, NAND

REGISTRY: Dict[str, Type[Gadget]] = {
    "AND": AND,
    "OR": OR,
    "NOT": NOT,
    "NAND": NAND,
}

def load_network_from_json(payload: Dict[str, Any]) -> Network:
    """
    Esquema esperado:
    {
      "pleats": ["a","b","sum","carry"],
      "gadgets": [
        {"type":"AND","id":"and1","inputs":["a","b"],"outputs":["carry"]},
        {"type":"OR","id":"or1","inputs":["a","b"],"outputs":["o1"]},
        {"type":"AND","id":"and2","inputs":["a","b"],"outputs":["o2"]}
      ],
      "inputs": {"a": true, "b": false}
    }
    """
    net = Network()
    for name in payload.get("pleats", []):
        net.add_pleat(name)
    for gdesc in payload.get("gadgets", []):
        gtype = gdesc["type"].upper()
        gid = gdesc["id"]
        cls = REGISTRY.get(gtype)
        if not cls:
            raise ValueError(f"Tipo de gadget desconocido: {gtype}")
        gadget = cls(gid=gid, input_names=gdesc["inputs"], output_names=gdesc["outputs"])
        net.add_gadget(gadget)
    if "inputs" in payload:
        net.set_inputs(payload["inputs"])
    return net
