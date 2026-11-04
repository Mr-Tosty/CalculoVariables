"""Modulo de Matematica Pura.

Procesa expresiones multivariables usando SymPy sin acoplamiento a la GUI.
"""

from sympy import (
    Symbol,
    sympify,
    limit,
    diff,
    integrate,
    latex,
    N,
)
from sympy.core.sympify import SympifyError


class MathEngine:

    def __init__(self):
        self.x = Symbol("x")
        self.y = Symbol("y")
        self.z = Symbol("z")

    def parse_expression(self, expr_str: str):
        """Convierte una cadena a SymPy y genera errores estilo Java."""
        if not expr_str or not expr_str.strip():
            raise ValueError(
                "NullPointerException: La expresion no puede ser nula o vacia."
            )
            
        clean_str = expr_str.replace("^", "**").strip()
        
        # Detecta patrones comunes de error antes de pasarlo a SymPy
        import re
        
        # Caso A: Multiplicacion implicita detectada (ej. 3x, xy sin *)
        if re.search(r"\d[a-zA-Z]", clean_str) or re.search(
            r"[x-zX-Z][x-zX-Z]", clean_str
        ):
            raise ValueError(
                "ExpressionSyntaxException: Se esperaba un operador '*' entre "
                "coeficientes y variables.\n"
                "  -> Regla Rota: Multiplicacion Implicita (ej: '3x')\n"
                "  -> Solucion sugerida: Reemplaza por '3*x' o 'x*y'."
            )
            
        # Caso B: Parentesis mal balanceados
        if clean_str.count("(") != clean_str.count(")"):
            raise ValueError(
                "ParenthesisMismatchException: Parentesis no balanceados.\n"
                "  -> Regla Rota: Todo '(' abierto debe cerrarse ']'\n"
                "  -> Solucion sugerida: Verifica la agrupacion de tus "
                "funciones."
            )

        try:
            expr = sympify(clean_str)
            return expr
        except SympifyError:
            raise ValueError(
                "ParseException: Error al compilar los tokens de la "
                "expresion.\n"
                "  -> Regla Rota: Estructura algebraica desconocida.\n"
                "  -> Ejemplo Valido: 'x**2 + y*cos(x)'"
            )
        except Exception as e:
            raise ValueError(
                f"MathEngineRuntimeException: {str(e)}"
            )

    def evaluate_limit(self, expr_str: str, var_str: str, point_str: str):
        """Calcula el limite de una funcion cuando una variable tiende a un punto."""
        expr = self.parse_expression(expr_str)
        var_symbol = Symbol(var_str.lower().strip())
        point_val = self.parse_expression(point_str)

        try:
            result = limit(expr, var_symbol, point_val)
            steps = (
                f"PASO 1: Expresion original f({var_symbol}) = {expr}\n"
                f"PASO 2: Evaluando el limite cuando {var_symbol} -> "
                f"{point_val}\n"
                f"RESULTADO: {result}"
            )
            return str(result), steps
        except Exception as e:
            raise ArithmeticError(
                f"Indeterminacion o error al evaluar limite: {str(e)}"
            )

    def evaluate_derivative(self, expr_str: str, var_str: str, order_str: str):
        """Calcula derivadas parciales simples, de orden superior o mixtas."""
        expr = self.parse_expression(expr_str)
        var_clean = var_str.lower().strip()
        
        # Validamos si se trata de una derivada mixta secuencial (ej. xy, yx)
        is_mixed = len(var_clean) > 1 and not var_clean.isdigit()

        try:
            current_expr = expr
            steps_list = [f"PASO 1: Expresion inicial f = {expr}"]
            
            if is_mixed:
                # Procesamiento paso a paso de derivadas parciales mixtas
                for idx, char in enumerate(var_clean, start=2):
                    var_symbol = Symbol(char)
                    current_expr = diff(current_expr, var_symbol, 1)
                    steps_list.append(
                        f"PASO {idx}: Derivando respecto a '{char}' -> "
                        f"{current_expr}"
                    )
                result = current_expr
                steps_list.append(f"RESULTADO MIXTO: {result}")
                steps = "\n".join(steps_list)
                return str(result), steps
            else:
                # Procesamiento clasico de orden numerico directo (ej. x con orden 2)
                var_symbol = Symbol(var_clean)
                order = int(order_str)
                if order < 1:
                    raise ValueError("El orden de derivada debe ser >= 1.")
                
                result = diff(expr, var_symbol, order)
                steps = (
                    f"PASO 1: Expresion f = {expr}\n"
                    f"PASO 2: Derivando parcialmente respecto a {var_symbol} "
                    f"(Orden {order})\n"
                    f"RESULTADO: d^{order}f/d{var_symbol}^{order} = {result}"
                )
                return str(result), steps
                
        except ValueError:
            raise ValueError(
                "Para derivadas simples, el orden debe ser entero. "
                "Para mixtas, escribe la secuencia en la variable principal."
            )
        except Exception as e:
            raise ArithmeticError(f"Error al derivar: {str(e)}")

    def evaluate_integral(
        self, expr_str: str, var_str: str, a_str: str = "", b_str: str = ""
    ):
        """Calcula la integral definida o indefinida."""
        expr = self.parse_expression(expr_str)
        var_symbol = Symbol(var_str.lower().strip())

        # Validacion robusta de campos vacios o inactivos de la GUI
        has_a = bool(a_str and a_str.strip())
        has_b = bool(b_str and b_str.strip())
        is_defined = has_a and has_b

        try:
            if is_defined:
                a_val = self.parse_expression(a_str)
                b_val = self.parse_expression(b_str)
                result = integrate(expr, (var_symbol, a_val, b_val))
                steps = (
                    f"PASO 1: Integrando f({var_symbol}) = {expr}\n"
                    f"PASO 2: Limites de integracion desde {a_val} hasta "
                    f"{b_val}\n"
                    f"RESULTADO DEFINIDO: {result}"
                )
            else:
                result = integrate(expr, var_symbol)
                steps = (
                    f"PASO 1: Integrando f({var_symbol}) = {expr}\n"
                    f"PASO 2: Calculando antiderivada respecto a "
                    f"{var_symbol}\n"
                    f"RESULTADO INDEFINIDO: {result} + C"
                )
            return str(result), steps
        except Exception as e:
            raise ArithmeticError(f"Error al integrar: {str(e)}")
