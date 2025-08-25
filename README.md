
# Simulador de Cómputo por Pliegues (Origami) – Lógica Booleana

Este proyecto modela "pleats" (tiras) y gadgets lógicos (AND, OR, NOT, NAND) que se interconectan en una red acíclica (DAG). Soporta valores `None` como señal indefinida (política por defecto: propagar `None` a la salida).

## Estructura
- `pleat.py`: clase `Pleat`.
- `gadget.py`: clase base `Gadget` y política de indefinidos.
- `gadgets.py`: NOT, AND, OR, NAND.
- `network.py`: gestión de pleats y gadgets, orden topológico, ejecución y detección de ciclos.
- `io_spec.py`: carga una red desde un JSON (esquema simple) con registro de tipos.
- `xor_composed.py`: helper para componer XOR a partir de gadgets básicos.
- `main.py`: ejemplos (medio sumador e instanciación desde JSON).
- `tests/`: pruebas unitarias de tablas de verdad y caso de integración (half-adder).

## Uso rápido
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
python3 main.py
```

## Política de indefinidos
Si cualquier entrada de un gadget es `None`, las salidas quedan en `None`. Puedes cambiar la política a `"raise"` en instancias específicas si prefieres que se lance una excepción.
