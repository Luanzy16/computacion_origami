
import unittest
from network import Network
from gadgets import AND, OR, NOT, NAND

class TestGadgetsTruthTables(unittest.TestCase):
    def setUp(self):
        self.net = Network()
        self.net.add_pleat("a")
        self.net.add_pleat("b")
        self.net.add_pleat("o")

    def eval_gate(self, gate_cls):
        self.net.gadgets.clear()
        self.net.writers.clear()
        g = gate_cls(gid="g", input_names=["a","b"] if gate_cls is not NOT else ["a"], output_names=["o"])
        self.net.add_gadget(g)

        cases = [
            (False, False),
            (False, True),
            (True, False),
            (True, True),
        ]
        results = []
        for a,b in cases:
            self.net.set_inputs({"a": a, "b": b})
            self.net.run()
            results.append(self.net.values(["o"])["o"])
        return results

    def test_and(self):
        res = self.eval_gate(AND)
        self.assertEqual(res, [False, False, False, True])

    def test_or(self):
        res = self.eval_gate(OR)
        self.assertEqual(res, [False, True, True, True])

    def test_nand(self):
        res = self.eval_gate(NAND)
        self.assertEqual(res, [True, True, True, False])

    def test_not(self):
        # For NOT, ignore b input
        self.net.gadgets.clear()
        self.net.writers.clear()
        g = NOT(gid="g", input_names=["a"], output_names=["o"])
        self.net.add_gadget(g)
        cases = [False, True]
        results = []
        for a in cases:
            self.net.set_inputs({"a": a})
            self.net.run()
            results.append(self.net.values(["o"])["o"])
        self.assertEqual(results, [True, False])

if __name__ == "__main__":
    unittest.main()
