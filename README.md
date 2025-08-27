
# 📘 Simulador de Cómputo por Pliegues (Origami Lógico)

Este proyecto implementa un simulador de **cómputo por pliegues** (inspirado en origami), donde:  
- Los **pleats** representan tiras de papel que llevan señales booleanas.  
- Los **gadgets** son patrones de pliegue que implementan compuertas lógicas (AND, OR, NOT, NAND).  
- Una **Network** conecta pleats y gadgets formando un grafo acíclico dirigido (DAG), y permite **propagar señales** desde entradas hasta salidas.  

---

### Integrantes

- Luis Sanchez
- Valentina Andrade
- Mateo Patiño
---

## 📂 Estructura de archivos

- **`pleat.py`** → define la clase `Pleat` (tira con señal booleana o indefinida `None`).  
- **`gadget.py`** → clase base `Gadget` y manejo de aridad, política de indefinidos.  
- **`gadgets.py`** → compuertas concretas: `AND`, `OR`, `NOT`, `NAND`.  
- **`network.py`** → clase `Network`, gestiona pleats, gadgets y la propagación en orden topológico.  
- **`loader.py`** → lee un archivo JSON y construye la `Network`.  
- **`main.py`** → ejemplo de ejecución usando `loader.py`.  
- **`entrada.json`** → ejemplo de circuito definido en JSON.  

---

## 📝 Formato del JSON

Ejemplo (`entrada.json`):

```json
{
  "pleats": ["a","b","sum","carry"],
  "gadgets": [
    {"type":"AND","id":"and1","inputs":["a","b"],"outputs":["carry"]},
    {"type":"OR","id":"or1","inputs":["a","b"],"outputs":["o1"]},
    {"type":"AND","id":"and2","inputs":["a","b"],"outputs":["o2"]}
  ],
  "inputs": {"a": true, "b": false}
}
```

- **`pleats`** → nombres de las tiras (señales).  
- **`gadgets`** → lista de compuertas con:
  - `type`: tipo de compuerta (`AND`, `OR`, `NOT`, `NAND`).  
  - `id`: identificador único.  
  - `inputs`: nombres de pleats de entrada.  
  - `outputs`: nombres de pleats de salida.  
- **`inputs`** → valores iniciales de las entradas (`true`, `false` o `null` para indefinido).  

---

## ▶️ Cómo ejecutar

1. Coloca tu definición del circuito en `entrada.json`.  
2. Corre el programa principal:

```bash
python main.py
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📊 Ejemplo de salida

Ejecutando con el `entrada.json` de arriba:

```
Valores finales: {'a': True, 'b': False, 'sum': None, 'carry': False, 'o1': True, 'o2': False}

Log de propagación:
   and1: {'carry': None} -> {'carry': False}
   or1: {'o1': None} -> {'o1': True}
   and2: {'o2': None} -> {'o2': False}
```

### Cómo leerlo:

1. **Valores finales**  
   - Diccionario con los pleats y su valor al terminar la propagación.  
   - Ejemplo:  
     - `"a": True`, `"b": False` → entradas fijas.  
     - `"carry": False` → salida de `AND(a,b)`.  
     - `"o1": True` → salida de `OR(a,b)`.  
     - `"o2": False` → salida de `AND(a,b)` (compuerta `and2`).  
     - `"sum": None` → quedó sin valor porque no hay gadget que lo produzca.  

2. **Log de propagación**  
   - Muestra cómo cambió cada salida durante la ejecución.  
   - Ejemplo:  
     - `and1: {'carry': None} -> {'carry': False}` significa que antes la salida estaba indefinida (`None`) y después tomó el valor `False`.  

---

