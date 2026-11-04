"""Motor de Matematica Pura (SymPy).

Soporta derivadas parciales, limites, integrales simples, dobles y triples.
"""

from sympy import Symbol, sympify, limit, diff, integrate, oo
from sympy.core.sympify import SympifyError


class MathEngine:

    def __init__(self):
        self.x = Symbol("x")
        self.y = Symbol("y")
        self.z = Symbol("z")

    def parse_expression(self, expr_str: str):
        """Convierte texto a expresion SymPy con sintaxis flexible."""
        if not expr_str or not expr_str.strip():
            raise ValueError("La expresion matematica no puede estar vacia.")
        try:
            clean_str = (
                expr_str.replace("^", "**")
                .replace("sen", "sin")
                .replace("tg", "tan")
            )
            return sympify(clean_str)
        except SympifyError:
            raise ValueError(
                "Sintaxis invalida. Use operadores correctos (*, +, -, ^, sin, cos, ln)."
            )
        except Exception as e:
            raise ValueError(f"Error al procesar expresion: {str(e)}")

    def evaluate_derivative(self, expr_str: str, var_str: str, order_str: str):
        """Calcula derivada parcial con orden especifico."""
        expr = self.parse_expression(expr_str)
        var_symbol = Symbol(var_str.lower().strip())
        try:
            order = int(order_str)
            if order < 1:
                raise ValueError
        except ValueError:
            raise ValueError("El orden de derivada debe ser un entero >= 1.")

        result = diff(expr, var_symbol, order)
        steps = (
            f"--- DERIVADA PARCIAL ---\n"
            f"1. Funcion f = {expr}\n"
            f"2. Variable de derivacion: {var_symbol} (Orden: {order})\n"
            f"3. Resultado exacto: {result}"
        )
        return str(result), steps

    def evaluate_limit(self, expr_str: str, var_str: str, point_str: str):
        """Evalua limite de la funcion en un punto."""
        expr = self.parse_expression(expr_str)
        var_symbol = Symbol(var_str.lower().strip())
        point_val = self.parse_expression(point_str)

        result = limit(expr, var_symbol, point_val)
        steps = (
            f"--- LIMITE ---\n"
            f"1. Funcion f = {expr}\n"
            f"2. Evaluando cuando {var_symbol} -> {point_val}\n"
            f"3. Resultado exacto: {result}"
        )
        return str(result), steps

    def evaluate_integral(
        self, expr_str: str, var_str: str, a_str: str = "", b_str: str = ""
    ):
        """Calcula integral definida o indefinida (simple)."""
        expr = self.parse_expression(expr_str)
        var_symbol = Symbol(var_str.lower().strip())
        is_defined = bool(a_str.strip() and b_str.strip())

        if is_defined:
            a_val = self.parse_expression(a_str)
            b_val = self.parse_expression(b_str)
            result = integrate(expr, (var_symbol, a_val, b_val))
            steps = (
                f"--- INTEGRAL DEFINIDA (SIMPLE) ---\n"
                f"1. Funcion f = {expr}\n"
                f"2. Limites: de {a_val} a {b_val} respecto a {var_symbol}\n"
                f"3. Resultado exacto: {result}"
            )
        else:
            result = integrate(expr, var_symbol)
            steps = (
                f"--- INTEGRAL INDEFINIDA (SIMPLE) ---\n"
                f"1. Funcion f = {expr}\n"
                f"2. Integrando respecto a {var_symbol}\n"
                f"3. Resultado exacto: {result} + C"
            )
        return str(result), steps

    def evaluate_double_integral(
        self, expr_str: str, x_limits: tuple, y_limits: tuple
    ):
        """Calcula integral doble iterada."""
        expr = self.parse_expression(expr_str)
        xa, xb = self.parse_expression(x_limits[0]), self.parse_expression(x_limits[1])
        ya, yb = self.parse_expression(y_limits[0]), self.parse_expression(y_limits[1])

        # Integramos primero respecto a y, luego respecto a x
        res_inner = integrate(expr, (self.y, ya, yb))
        result = integrate(res_inner, (self.x, xa, xb))

        steps = (
            f"--- INTEGRAL DOBLE ---\n"
            f"1. Funcion f(x,y) = {expr}\n"
            f"2. Rango Y: [{ya}, {yb}] | Rango X: [{xa}, {xb}]\n"
            f"3. Resultado exacto: {result}"
        )
        return str(result), steps

    def evaluate_triple_integral(
        self, expr_str: str, x_lim: tuple, y_lim: tuple, z_lim: tuple
    ):
        """Calcula integral triple iterada."""
        expr = self.parse_expression(expr_str)
        xa, xb = self.parse_expression(x_lim[0]), self.parse_expression(x_lim[1])
        ya, yb = self.parse_expression(y_lim[0]), self.parse_expression(y_lim[1])
        za, zb = self.parse_expression(z_lim[0]), self.parse_expression(z_lim[1])

        res1 = integrate(expr, (self.z, za, zb))
        res2 = integrate(res1, (self.y, ya, yb))
        result = integrate(res2, (self.x, xa, xb))

        steps = (
            f"--- INTEGRAL TRIPLE ---\n"
            f"1. Funcion f(x,y,z) = {expr}\n"
            f"2. Rangos Z:[{za},{b_str if 'zb' in locals() else zb}], Y:[{ya},{yb}], X:[{xa},{xb}]\n"
            f"3. Resultado exacto: {result}"
        )
        return str(result), steps