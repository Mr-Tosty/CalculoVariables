"""Módulo POO para la resolución de derivadas parciales y mixtas.

Basado estrictamente en las reglas del formulario oficial de derivadas.
"""

from sympy import Symbol, diff, sympify
from sympy.core.sympify import SympifyError


class DerivativeSolver:
    """Clase especializada en aplicar reglas de derivación simbólica."""

    def __init__(self, x: Symbol, y: Symbol, z: Symbol):
        self.x = x
        self.y = y
        self.z = z

    def solve(self, expr_str: str, var_str: str, order_str: str):
        """Calcula la derivada parcial aplicando reglas del formulario."""
        if not expr_str or not expr_str.strip():
            raise ValueError("La función de entrada no puede estar vacía.")

        try:
            clean_expr = (
                expr_str.replace("^", "**")
                .replace("sen", "sin")
                .replace("tg", "tan")
            )
            expr = sympify(clean_expr)
            var = Symbol(var_str.lower().strip())
            order = int(order_str)

            if order < 1:
                raise ValueError("El orden de derivada debe ser mayor o igual a 1.")

            result = diff(expr, var, order)
            steps = (
                f"--- FORMULARIO DE DERIVADAS (APLICADO) ---\n"
                f"1. Función original f = {expr}\n"
                f"2. Variable de derivación: {var} (Orden: {order})\n"
                f"3. Regla aplicada: Derivada sucesiva / parcial\n"
                f"4. Resultado exacto: {result}"
            )
            return str(result), steps

        except SympifyError:
            raise ValueError("Sintaxis inválida en la función o variables.")
        except Exception as e:
            raise ArithmeticError(f"Error al procesar la derivada: {str(e)}")