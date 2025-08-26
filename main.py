from network import Network
from xor_composed import add_xor
from gadgets import AND

net = Network()
net.add_pleat("a")
net.add_pleat("b")
net.add_pleat("sum")
net.add_pleat("carry")

# sum = XOR(a,b)
add_xor(net, "xor1", "a", "b", "sum")

# carry = AND(a,b)
net.add_gadget(AND(gid="carry_and", input_names=["a","b"], output_names=["carry"]))

# Probar todas las combinaciones
cases = [(False, False), (False, True), (True, False), (True, True)]
for a_val, b_val in cases:
    net.set_inputs({"a": a_val, "b": b_val})
    net.run()
    vals = net.values(["a","b","sum","carry"])
    print(vals)
