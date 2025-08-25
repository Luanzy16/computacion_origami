
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Iterable, Tuple, Optional, Set
from pleat import Pleat, Signal
from gadget import Gadget, GadgetError


class CycleError(Exception):
    pass


@dataclass
class Network:
    pleats: Dict[str, Pleat] = field(default_factory=dict)
    gadgets: List[Gadget] = field(default_factory=list)
    # Mapea nombre de pleat -> gadget escritor (para detectar múltiples escritores)
    writers: Dict[str, Gadget] = field(default_factory=dict)

    def add_pleat(self, name: str, initial: Signal = None) -> Pleat:
        if name in self.pleats:
            # Permitir redefinir el valor inicial
            self.pleats[name].value = initial
            return self.pleats[name]
        p = Pleat(name=name, value=initial)
        self.pleats[name] = p
        return p

    def add_gadget(self, gadget: Gadget) -> None:
        # Crear pleats referenciados si no existen aún
        for n in set(gadget.input_names + gadget.output_names):
            if n not in self.pleats:
                self.add_pleat(n)
        # Verificar escritor único por salida
        for out in gadget.output_names:
            if out in self.writers:
                raise GadgetError(f"Pleat '{out}' ya tiene escritor: {self.writers[out].gid}")
            self.writers[out] = gadget
        self.gadgets.append(gadget)

    def bind_all(self) -> None:
        for g in self.gadgets:
            g.bind(self.pleats)

    def set_inputs(self, values: Dict[str, Signal]) -> None:
        for name, val in values.items():
            if name not in self.pleats:
                self.add_pleat(name, val)
            else:
                self.pleats[name].value = val

    def _build_dependency_graph(self) -> Dict[Gadget, List[Gadget]]:
        """
        Grafo dirigido g->h si alguna salida de g alimenta una entrada de h.
        """
        # Mapear pleat -> lista de gadgets que lo leen
        readers: Dict[str, List[Gadget]] = {n: [] for n in self.pleats}
        for g in self.gadgets:
            for n in g.input_names:
                readers[n].append(g)
        graph: Dict[Gadget, List[Gadget]] = {g: [] for g in self.gadgets}
        for g in self.gadgets:
            for out in g.output_names:
                for h in readers.get(out, []):
                    if h is not g:
                        graph[g].append(h)
        return graph

    def _topological_order(self) -> List[Gadget]:
        graph = self._build_dependency_graph()
        indeg: Dict[Gadget, int] = {g: 0 for g in self.gadgets}
        for g, neighs in graph.items():
            for h in neighs:
                indeg[h] += 1
        # Kahn
        q = [g for g, d in indeg.items() if d == 0]
        order: List[Gadget] = []
        while q:
            g = q.pop(0)
            order.append(g)
            for h in graph[g]:
                indeg[h] -= 1
                if indeg[h] == 0:
                    q.append(h)
        if len(order) != len(self.gadgets):
            raise CycleError("Ciclo de dependencias detectado")
        return order

    def run(self, max_passes: int = 3, log: bool = False) -> List[str]:
        """
        Propaga señales en orden topológico. Retorna un log de evaluación si log=True.
        """
        self.bind_all()
        order = self._topological_order()
        history: List[str] = []
        for _ in range(max_passes):
            changed = False
            for g in order:
                before = {p.name: p.value for p in g.outputs}
                g.evaluate()
                after = {p.name: p.value for p in g.outputs}
                if log:
                    history.append(f"{g.gid}: {before} -> {after}")
                if before != after:
                    changed = True
            if not changed:
                break
        return history

    def values(self, names: Optional[Iterable[str]] = None) -> Dict[str, Signal]:
        if names is None:
            names = self.pleats.keys()
        return {n: self.pleats[n].value for n in names}
