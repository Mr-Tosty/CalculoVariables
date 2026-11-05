"""Motor matemático centralizado y robusto basado en POO.

Integra los solucionadores de derivadas[cite: 1, 6] e integrales[cite: 2, 5],
así como el análisis de límites multivariables y tablas de aproximación[cite: 3].
"""

from sympy import Symbol, sympify, limit
from sympy.core.sympify import SympifyError
from core.solvers.derivative_solver import DerivativeSolver
from core.solvers.integral_solver import IntegralSolver


class MathEngine:
    """Clase principal de control matemático que coordina los subsistemas POO."""

    def __init__(self):
        self.x = Symbol("x")
        self.y = Symbol("y")
        self.z = Symbol("z")

        # Instanciación de los módulos especializados de cálculo
        self.der_solver = DerivativeSolver(self.x, self.y, self.z)
        self.int_solver = IntegralSolver(self.x, self.y, self.z)

    def parse_expression(self, expr_str: str):
        """Analiza y convierte una cadena de texto en una expresión de SymPy de forma segura."""
        if not expr_str or not expr_str.strip():
            raise ValueError("La expresión matemática de entrada no puede estar vacía.")
        try:
            clean_str = (
                expr_str.replace("^", "**")
                .replace("sen", "sin")
                .replace("tg", "tan")
            )
            return sympify(clean_str)
        except SympifyError as exc:
            raise ValueError(
                "Sintaxis matemática inválida. Verifique operadores (*, +, -, ^, sin, cos)."
            ) from exc
        except Exception as e:
            raise ValueError(f"Error inesperado al procesar la expresión: {str(e)}")

    def evaluate_derivative(self, expr_str: str, var_str: str, order_str: str):
        """Ejecuta el cálculo de derivadas parciales y mixtas siguiendo el formulario oficial[cite: 1, 6]."""
        return self.der_solver.solve(expr_str, var_str, order_str)

    def evaluate_single_integral(self, expr_str: str, var_str: str, a: str = "", b: str = ""):
        """Calcula integrales simples definidas o indefinidas usando identidades básicas[cite: 2, 5]."""
        return self.int_solver.solve_single(expr_str, var_str, a, b)

    def evaluate_double_integral(
        self, expr_str: str, xa: str, xb: str, ya: str, yb: str
    ):
        """Calcula integrales dobles iteradas con soporte para límites algebraicos o constantes."""
        return self.int_solver.solve_double(expr_str, xa, xb, ya, yb)

    def evaluate_triple_integral(
        self,
        expr_str: str,
        xa: str,
        xb: str,
        ya: str,
        yb: str,
        za: str,
        zb: str,
    ):
        """Calcula integrales triples iteradas para dominios tridimensionales complejos."""
        return self.int_solver.solve_triple(expr_str, xa, xb, ya, yb, za, zb)

    def generate_limit_table(self, expr_str: str):
        """Genera la tabla de aproximación numérica de límites multivariables hacia (0,0,0)[cite: 3]."""
        expr = self.parse_expression(expr_str)
        points = [1.0, 0.5, 0.1, 0.05, 0.01]
        table_rows = []

        for p in points:
            try:
                val = float(
                    expr.subs({self.x: p, self.y: p, self.z: p}).evalf()
                )
                table_rows.append(f"({p}, {p}, {p})  ==>  f(x,y,z) = {val:.6f}")
            except Exception:
                table_rows.append(f"({p}, {p}, {p})  ==>  Indeterminado / Rompe")

        # Cálculo analítico secuencial del límite global
        lim_val = limit(
            limit(limit(expr, self.z, 0), self.y, 0), self.x, 0
        )

        steps = (
            f"=== ANÁLISIS DE LÍMITES Y TRAYECTORIAS (APUNTES) ===\n"
            f"Función evaluada: f(x,y,z) = {expr}\n"
            f"Aproximación sucesiva hacia el punto (0,0,0):\n"
            + "\n".join(table_rows)
            + f"\n\nLímite analítico global (x,y,z) -> (0,0,0): {lim_val}"
        )
        return steps