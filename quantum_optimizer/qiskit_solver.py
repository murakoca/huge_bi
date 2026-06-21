"""
Kuantum optimizasyon modülü (Qiskit tabanlı).
Not: Qiskit kütüphanesinin yüklü olması gerekir.
"""

from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms import QAOA
from qiskit import Aer

class QuantumOptimizer:
    """Basit bütçe optimizasyonu için QUBO modeli kurar ve QAOA ile çözer."""

    def solve_budget_allocation(self, items, budget, costs, returns):
        qp = QuadraticProgram()
        # binary değişkenler
        for i in items:
            qp.binary_var(f'x_{i}')
        # amaç: toplam getiriyi maksimize et → minimize -getiri
        linear = {f'x_{i}': -r for i, r in zip(items, returns)}
        qp.minimize(linear=linear)
        # bütçe kısıtı
        qp.linear_constraint(
            linear={f'x_{i}': c for i, c in zip(items, costs)},
            sense='<=',
            rhs=budget
        )
        # QAOA ile çözüm
        backend = Aer.get_backend('statevector_simulator')
        qaoa = MinimumEigenOptimizer(QAOA(reps=1, quantum_instance=backend))
        result = qaoa.solve(qp)
        return result