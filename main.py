from loader import load_circuit_from_json

if __name__ == "__main__":
    net = load_circuit_from_json("entrada.json")
    log = net.run(log=True)
    print("Valores finales:", net.values())
    print("\nLog de propagación:")
    for step in log:
        print("  ", step)
