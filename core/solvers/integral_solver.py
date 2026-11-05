"""Módulo POO para la resolución de integrales simples y múltiples.

Basado en las fórmulas del formulario de integración (potencias, logaritmos, etc.).
"""

from sympy import Symbol, integrate, sympify
from sympy.core.sympify import SympifyError


class IntegralSolver:
    """Clase especializada en la resolución de integrales indefinidas y definidas."""

    def __init__(self, x: Symbol, y: Symbol, z: Symbol):
        self.x = x
        self.y = y
        self.z = z

    def solve_single(self, expr_str: str, var_str: str, a: str, b: str):
        """Calcula integral simple aplicando reglas inmediatas del formulario."""
        expr = sympify(expr_str.replace("^", "**"))
        var = Symbol(var_str.lower().strip())
        is_defined = bool(a.strip() and b.strip())

        if is_defined:
            ia, ib = sympify(a), sympify(b)
            result = integrate(expr, (var, ia, ib))
            steps = (
                f"--- FORMULARIO DE INTEGRALES (Definida) ---\n"
                f"1. Integrando f({var}) = {expr}\n"
                f"2. Límites de integración: desde {ia} hasta {ib}\n"
                f"3. Resultado exacto: {result}"
            )
        else:
            result = integrate(expr, var)
            steps = (
                f"--- FORMULARIO DE INTEGRALES (Indefinida) ---\n"
                f"1. Integrando f({var}) = {expr}\n"
                f"2. Antiderivada inmediata (Fórmula básica)\n"
                f"3. Resultado exacto: {result} + C"
            )
        return str(result), steps

    def solve_double(self, expr_str: str, xa: str, xb: str, ya: str, yb: str):
        """Calcula integral doble iterada."""
        expr = sympify(expr_str.replace("^", "**"))
        x_inf, x_sup = sympify(xa), sympify(xb)
        y_inf, y_sup = sympify(ya), sympify(yb)

        res_inner = integrate(expr, (self.y, y_inf, y_sup))
        result = integrate(res_inner, (self.x, x_inf, x_sup))

        steps = (
            f"--- INTEGRAL DOBLE ITERADA ---\n"
            f"1. Función f(x,y) = {expr}\n"
            f"2. Rango interno dy: [{y_inf}, {y_sup}] -> {res_inner}\n"
            f"3. Rango externo dx: [{x_inf}, {x_sup}] -> {result}"
        )
        return str(result), steps

    def solve_triple(self, expr_str: str, xa: str, xb: str, ya: str, yb: str, za: str, zb: str):
        """Calcula integral triple iterada."""
        expr = sympify(expr_str.replace("^", "**"))
        xi, xs = sympify(xa), sympify(xb)
        yi, ys = sympify(ya), sympify(yb)
        zi, zs = sympify(za), sympify(zb)

        r1 = integrate(expr, (self.z, zi, zs))
        r2 = integrate(r1, (self.y, yi, ys))
        result = integrate(r2, (self.x, xi, xs))

        steps = (
            f"--- INTEGRAL TRIPLE ITERADA ---\n"
            f"1. Función f(x,y,z) = {expr}\n"
            f"2. Integración sucesiva dz -> dy -> dx\n"
            f"3. Resultado exacto: {result}"
        )
        return str(result), steps