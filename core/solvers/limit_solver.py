"""Módulo POO para el cálculo de límites y tablas de aproximación multivariable.

Basado en el análisis de trayectorias de los apuntes del estudiante.
"""

from sympy import Symbol, limit, sympify


class LimitSolver:
    """Clase especializada en límites y aproximaciones numéricas a puntos."""

    def __init__(self, x: Symbol, y: Symbol, z: Symbol):
        self.x = x
        self.y = y
        self.z = z

    def solve_limit(self, expr_str: str, var_str: str, point_str: str):
        """Evalúa analíticamente el límite de una función."""
        if not expr_str.strip():
            raise ValueError("La función no puede estar vacía.")
        
        expr = sympify(expr_str.replace("^", "**"))
        var = Symbol(var_str.lower().strip())
        point = sympify(point_str)

        result = limit(expr, var, point)
        steps = (
            f"--- ANÁLISIS DE LÍMITE ---\n"
            f"1. Función f({var}) = {expr}\n"
            f"2. Evaluando límite cuando {var} -> {point}\n"
            f"3. Resultado exacto: {result}"
        )
        return str(result), steps

    def generate_approximation_table(self, expr_str: str):
        """Genera la tabla de aproximación numérica por trayectorias."""
        expr = sympify(expr_str.replace("^", "**"))
        points = [1.0, 0.5, 0.1, 0.05, 0.01]
        rows = []

        for p in points:
            try:
                val = float(
                    expr.subs({self.x: p, self.y: p, self.z: p}).evalf()
                )
                rows.append(f"({p}, {p}, {p})  -->  f = {val:.6f}")
            except Exception:
                rows.append(f"({p}, {p}, {p})  -->  Indeterminado")

        lim_val = limit(
            limit(limit(expr, self.z, 0), self.y, 0), self.x, 0
        )
        steps = (
            f"--- TABLA DE APROXIMACIÓN (APUNTES) ---\n"
            f"Función: f(x,y,z) = {expr}\n"
            f"Aproximando a (0,0,0):\n"
            + "\n".join(rows)
            + f"\n\nLímite Global Analítico: {lim_val}"
        )
        return steps