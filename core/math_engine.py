"""Motor de Matematica Pura (SymPy + Numpy).

Procesa calculo multivariable analitico y tablas de aproximacion de limites.
"""

from sympy import Symbol, sympify, limit, diff, integrate
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
                "Sintaxis invalida. Use operadores correctos (*, +, -, ^)."
            )
        except Exception as e:
            raise ValueError(f"Error al procesar expresion: {str(e)}")

    def evaluate_derivative(
        self, expr_str: str, x_val: str, y_val: str, sequence: str
    ):
        """Calcula derivada parcial/mixta y evalua en punto (estilo Web MVC)."""
        expr = self.parse_expression(expr_str)

        # Analisis de secuencia
        if sequence == "∂f / ∂x":
            der_expr = diff(expr, self.x)
            var_name = "x"
        elif sequence == "∂f / ∂y":
            der_expr = diff(expr, self.y)
            var_name = "y"
        elif sequence == "∂²f / ∂x²":
            der_expr = diff(expr, self.x, 2)
            var_name = "x^2"
        elif sequence == "∂²f / ∂y²":
            der_expr = diff(expr, self.y, 2)
            var_name = "y^2"
        elif sequence == "∂²f / (∂x ∂y)":
            der_expr = diff(diff(expr, self.x), self.y)
            var_name = "x y"
        else:
            der_expr = diff(expr, self.x)
            var_name = "x"

        # Evaluacion en el punto si existen valores
        eval_text = "N/A"
        if x_val.strip() and y_val.strip():
            try:
                xv = float(self.parse_expression(x_val).evalf())
                yv = float(self.parse_expression(y_val).evalf())
                num_res = der_expr.subs({self.x: xv, self.y: yv}).evalf()
                eval_text = f"f_{var_name}({xv}, {yv}) = {float(num_res):.6f}"
            except Exception:
                eval_text = "No se pudo evaluar en el punto especificado."

        steps = (
            f"FUNCIÓN INGRESADA: f(x, y) = {expr}\n"
            f"PUNTO DE EVALUACIÓN: (x = {x_val or 0}, y = {y_val or 0})\n"
            f"--------------------------------------------------\n"
            f"DERIVADA SIMBÓLICA: ∂f/∂{var_name} = {der_expr}\n"
            f"--------------------------------------------------\n"
            f"PASO 1: Expresion de entrada f = {expr}\n"
            f"PASO 2: Derivando respecto a '{var_name}' -> {der_expr}\n"
            f"EVALUACIÓN EN EL PUNTO: {eval_text}"
        )
        return str(der_expr), steps

    def generate_limit_table(self, expr_str: str):
        """Genera la tabla de aproximacion numerica (como en los apuntes)."""
        expr = self.parse_expression(expr_str)
        points = [1.0, 0.5, 0.1, 0.05, 0.01]
        table_rows = []

        for p in points:
            try:
                val = float(
                    expr.subs({self.x: p, self.y: p, self.z: p}).evalf()
                )
                table_rows.append(f"({p}, {p}, {p})  -->  f = {val:.6f}")
            except Exception:
                table_rows.append(f"({p}, {p}, {p})  -->  Indeterminado")

        lim_val = limit(
            limit(limit(expr, self.z, 0), self.y, 0), self.x, 0
        )

        steps = (
            f"Aproximación de Límites Multivariables (Apuntes):\n"
            f"Función: f(x,y,z) = {expr}\n"
            f"Evaluando aproximación a (0,0,0):\n"
            + "\n".join(table_rows)
            + f"\n\nLímite Analítico (x,y,z)->(0,0,0): {lim_val}"
        )
        return steps

    def evaluate_double_integral(
        self, expr_str: str, xa: str, xb: str, ya: str, yb: str
    ):
        """Calcula integral doble iterada."""
        expr = self.parse_expression(expr_str)
        x_inf, x_sup = self.parse_expression(xa), self.parse_expression(xb)
        y_inf, y_sup = self.parse_expression(ya), self.parse_expression(yb)

        res_inner = integrate(expr, (self.y, y_inf, y_sup))
        result = integrate(res_inner, (self.x, x_inf, x_sup))

        steps = (
            f"FUNCIÓN INGRESADA: f(x, y) = {expr}\n"
            f"LÍMITES INTEGRACIÓN: X:[{x_inf}, {x_sup}] | Y:[{y_inf}, {y_sup}]\n"
            f"--------------------------------------------------\n"
            f"RESULTADO INTEGRAL DOBLE: {result}\n"
            f"--------------------------------------------------\n"
            f"PASO 1: Integral interna dy respecto a Y -> {res_inner}\n"
            f"PASO 2: Integral externa dx respecto a X -> {result}"
        )
        return str(result), steps

    def evaluate_triple_integral(
        self, expr_str: str, xa: str, xb: str, ya: str, yb: str, za: str, zb: str
    ):
        """Calcula integral triple iterada."""
        expr = self.parse_expression(expr_str)
        x_inf, x_sup = self.parse_expression(xa), self.parse_expression(xb)
        y_inf, y_sup = self.parse_expression(ya), self.parse_expression(yb)
        z_inf, z_sup = self.parse_expression(za), self.parse_expression(zb)

        r1 = integrate(expr, (self.z, z_inf, z_sup))
        r2 = integrate(r1, (self.y, y_inf, y_sup))
        result = integrate(r2, (self.x, x_inf, x_sup))

        steps = (
            f"FUNCIÓN INGRESADA: f(x, y, z) = {expr}\n"
            f"RESULTADO INTEGRAL TRIPLE: {result}\n"
            f"--------------------------------------------------\n"
            f"PASO 1: Integral dz -> {r1}\n"
            f"PASO 2: Integral dy -> {r2}\n"
            f"PASO 3: Integral dx -> {result}"
        )
        return str(result), steps