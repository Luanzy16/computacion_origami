
from __future__ import annotations
from network import Network
from gadgets import OR, AND, NOT

def add_xor(net: Network, gid_prefix: str, a: str, b: str, out: str) -> None:
    """
    Implementa XOR(a,b) = (a OR b) AND NOT(a AND b)
    Crea pleats intermedios si no existen: o_ab, a_and_b, not_and
    """
    o_ab = f"{gid_prefix}_o_ab"
    a_and_b = f"{gid_prefix}_a_and_b"
    not_and = f"{gid_prefix}_not_and"

    # OR
    net.add_gadget(OR(gid=f"{gid_prefix}_OR", input_names=[a, b], output_names=[o_ab]))
    # AND
    net.add_gadget(AND(gid=f"{gid_prefix}_AND", input_names=[a, b], output_names=[a_and_b]))
    # NOT
    net.add_gadget(NOT(gid=f"{gid_prefix}_NOT", input_names=[a_and_b], output_names=[not_and]))
    # AND final para XOR
    net.add_gadget(AND(gid=f"{gid_prefix}_XOR_AND", input_names=[o_ab, not_and], output_names=[out]))
