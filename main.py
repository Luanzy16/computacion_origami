
import json
from network import Network
from io_spec import load_network_from_json
from xor_composed import add_xor
from gadgets import AND

def example_half_adder() -> None:
    net = Network()
    # Entradas/salidas
    net.add_pleat("a")
    net.add_pleat("b")
    net.add_pleat("sum")
    net.add_pleat("carry")
    # XOR compuesto
    add_xor(net, "xor1", "a", "b", "sum")
    # carry
    net.add_gadget(AND(gid="carry_and", input_names=["a","b"], output_names=["carry"]))

    # Prueba de las 4 combinaciones
    cases = [(False, False), (False, True), (True, False), (True, True)]
    for a_val, b_val in cases:
        net.set_inputs({"a": a_val, "b": b_val})
        log = net.run(log=True)
        vals = net.values(["a","b","sum","carry"])
        print(f"Entradas a={a_val} b={b_val} -> sum={vals['sum']} carry={vals['carry']}")
        # Descomenta si quieres ver el log:
        # for line in log: print("  ", line)

def example_from_json() -> None:
    payload = {
        "pleats": ["a","b","sum","carry"],
        "gadgets": [
            {"type":"AND","id":"carry_and","inputs":["a","b"],"outputs":["carry"]}
        ],
        "inputs": {"a": True, "b": True}
    }
    net = load_network_from_json(payload)
    net.run()
    print(net.values(["a","b","carry"]))

if __name__ == "__main__":
    print("== Medio Sumador (Half-Adder) ==")
    example_half_adder()
    print("\n== Desde JSON ==")
    example_from_json()
