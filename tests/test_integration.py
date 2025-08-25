
import unittest
from network import Network
from xor_composed import add_xor
from gadgets import AND

class TestHalfAdderIntegration(unittest.TestCase):
    def test_half_adder(self):
        net = Network()
        for name in ["a","b","sum","carry"]:
            net.add_pleat(name)
        add_xor(net, "xor1", "a", "b", "sum")
        net.add_gadget(AND(gid="carry_and", input_names=["a","b"], output_names=["carry"]))

        cases = [
            (False, False, False, False),
            (False, True,  True,  False),
            (True,  False, True,  False),
            (True,  True,  False, True),
        ]
        for a,b,exp_sum,exp_carry in cases:
            net.set_inputs({"a": a, "b": b})
            net.run()
            vals = net.values(["sum","carry"])
            self.assertEqual(vals["sum"], exp_sum, f"sum con a={a}, b={b}")
            self.assertEqual(vals["carry"], exp_carry, f"carry con a={a}, b={b}")

if __name__ == "__main__":
    unittest.main()
