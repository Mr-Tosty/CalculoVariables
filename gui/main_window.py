"""Modulo de Interfaz de Usuario.

Diseno ultra intuitivo, letras grandes, boton de indicaciones y graficos 2D/3D seguros.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from core.math_engine import MathEngine

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class InstructionsWindow(ctk.CTkToplevel):
    """Ventana independiente para mostrar las instrucciones claras y formularios."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ayuda e Indicaciones del Asistente")
        self.geometry("650 x 550")
        self.minsize(500, 400)

        title_lbl = ctk.CTkLabel(
            self,
            text="Guia de Uso y Formulario Rapido",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        title_lbl.pack(pady=10)

        txt_box = ctk.CTkTextbox(self, font=ctk.CTkFont(size=13))
        txt_box.pack(fill="both", expand=True, padx=15, pady=10)

        guide_text = (
            "BIENVENIDO AL ASISTENTE DE CALCULO MULTIVARIABLE\n\n"
            "1. COMO INGRESAR FUNCIONES:\n"
            "   - Use la sintaxis estandar de Python/SymPy.\n"
            "   - Multiplicacion explicita recomendada: ej. 3*x^2 o 2*x*y.\n"
            "   - Potencias: Use '^' o '**' (ej. x^3).\n"
            "   - Funciones trigonometricas: sin(x), cos(x), tan(x).\n"
            "   - Logaritmos y exponenciales: ln(x) o log(x), exp(x) o e**x.\n\n"
            "2. OPERACIONES DISPONIBLES:\n"
            "   - Derivar: Seleccione la variable (x, y, z) y el orden numerico (1, 2...).\n"
            "   - Limite: Ingrese la variable y el valor al que tiende (ej. 0 o oo).\n"
            "   - Integrar (Simple): Indefinida o definida ingresando limite inferior y superior.\n"
            "   - Integral Doble / Triple: Ingrese limites para cada variable separados por campos.\n\n"
            "3. OBSERVACIONES IMPORTANTES:\n"
            "   - Si la funcion incluye la variable 'z', la grafica 2D se omite automaticamente "
            "para evitar errores visuales, mostrando el resultado analitico con total precision.\n"
            "   - Si ocurre algun error de sintaxis o indeterminacion, la aplicacion lo alertara "
            "en color rojo/naranja sin bloquear el programa (Failsafe activo)."
        )
        txt_box.insert("1.0", guide_text)
        txt_box.configure(state="disabled")

        btn_close = ctk.CTkButton(
            self, text="Entendido, Cerrar", command=self.destroy
        )
        btn_close.pack(pady=10)


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.engine = MathEngine()

        self.title("Asistente de Calculo Multivariable - Educativo")
        self.geometry("1200 x 800")
        self.minsize(950, 700)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_form_panel()
        self._build_results_panel()

    def _build_header(self):
        header = ctk.CTkFrame(self, corner_radius=0, fg_color=("gray85", "gray20"))
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        title = ctk.CTkLabel(
            header,
            text="Asistente de Calculo Multivariable",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        title.pack(side="left", padx=20, pady=10)

        # Boton de indicaciones requerido
        btn_help = ctk.CTkButton(
            header,
            text="📖 Guia e Indicaciones",
            fg_color="#1f538d",
            hover_color="#14375e",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._open_instructions,
        )
        btn_help.pack(side="right", padx=20, pady=10)

    def _open_instructions(self):
        InstructionsWindow(self)

    def _build_form_panel(self):
        form = ctk.CTkScrollableFrame(self, label_text="Panel de Control y Funciones")
        form.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Entrada de funcion con letra clara y grande
        ctk.CTkLabel(
            form, text="Funcion f(x, y, z):", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 2))
        self.entry_expr = ctk.CTkEntry(
            form, placeholder_text="Ej: x^2 + 3*x*y - sin(z)", height=35, font=ctk.CTkFont(size=14)
        )
        self.entry_expr.pack(fill="x", padx=15, pady=2)

        # Selector de operacion
        ctk.CTkLabel(
            form, text="Seleccione Operacion:", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 2))
        self.op_var = ctk.StringVar(value="Derivar Parcialmente")
        self.combo_op = ctk.CTkOptionMenu(
            form,
            values=[
                "Derivar Parcialmente",
                "Evaluar Limite",
                "Integral Simple",
                "Integral Doble",
                "Integral Triple",
            ],
            variable=self.op_var,
            command=self._toggle_operation_fields,
            height=35,
            font=ctk.CTkFont(size=13),
        )
        self.combo_op.pack(fill="x", padx=15, pady=2)

        # Contenedor dinamico para parametros
        self.param_frame = ctk.CTkFrame(form, fg_color="transparent")
        self.param_frame.pack(fill="x", padx=5, pady=10)

        self._build_derivative_fields()

        btn_calc = ctk.CTkButton(
            form,
            text="⚡ Calcular con Precision",
            command=self._execute_calculation,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2b8a3e",
            hover_color="#236f33",
        )
        btn_calc.pack(fill="x", padx=15, pady=20)

    def _toggle_operation_fields(self, choice):
        for widget in self.param_frame.winfo_children():
            widget.destroy()

        if choice == "Derivar Parcialmente":
            self._build_derivative_fields()
        elif choice == "Evaluar Limite":
            self._build_limit_fields()
        elif choice == "Integral Simple":
            self._build_single_integral_fields()
        elif choice == "Integral Doble":
            self._build_double_integral_fields()
        elif choice == "Integral Triple":
            self._build_triple_integral_fields()

    def _build_derivative_fields(self):
        ctk.CTkLabel(self.param_frame, text="Variable (x, y, z):", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=2)
        self.entry_var = ctk.CTkEntry(self.param_frame, placeholder_text="x", font=ctk.CTkFont(size=13))
        self.entry_var.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(self.param_frame, text="Orden de derivada:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(10, 2))
        self.entry_p1 = ctk.CTkEntry(self.param_frame, placeholder_text="1", font=ctk.CTkFont(size=13))
        self.entry_p1.pack(fill="x", padx=10, pady=2)

    def _build_limit_fields(self):
        ctk.CTkLabel(self.param_frame, text="Variable que tiende:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=2)
        self.entry_var = ctk.CTkEntry(self.param_frame, placeholder_text="x", font=ctk.CTkFont(size=13))
        self.entry_var.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(self.param_frame, text="Valor al que tiende (Punto):", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(10, 2))
        self.entry_p1 = ctk.CTkEntry(self.param_frame, placeholder_text="0 o oo", font=ctk.CTkFont(size=13))
        self.entry_p1.pack(fill="x", padx=10, pady=2)

    def _build_single_integral_fields(self):
        ctk.CTkLabel(self.param_frame, text="Variable de integracion:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=2)
        self.entry_var = ctk.CTkEntry(self.param_frame, placeholder_text="x", font=ctk.CTkFont(size=13))
        self.entry_var.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(self.param_frame, text="Limite Inferior (a) [Opcional]:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(10, 2))
        self.entry_p1 = ctk.CTkEntry(self.param_frame, placeholder_text="Ej: 0", font=ctk.CTkFont(size=13))
        self.entry_p1.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(self.param_frame, text="Limite Superior (b) [Opcional]:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(10, 2))
        self.entry_p2 = ctk.CTkEntry(self.param_frame, placeholder_text="Ej: 1", font=ctk.CTkFont(size=13))
        self.entry_p2.pack(fill="x", padx=10, pady=2)

    def _build_double_integral_fields(self):
        ctk.CTkLabel(self.param_frame, text="Limites X [Inf, Sup]:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=2)
        self.entry_xa = ctk.CTkEntry(self.param_frame, placeholder_text="0", font=ctk.CTkFont(size=13))
        self.entry_xa.pack(fill="x", padx=10, pady=2)
        self.entry_xb = ctk.CTkEntry(self.param_frame, placeholder_text="1", font=ctk.CTkFont(size=13))
        self.entry_xb.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(self.param_frame, text="Limites Y [Inf, Sup]:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(10, 2))
        self.entry_ya = ctk.CTkEntry(self.param_frame, placeholder_text="0", font=ctk.CTkFont(size=13))
        self.entry_ya.pack(fill="x", padx=10, pady=2)
        self.entry_yb = ctk.CTkEntry(self.param_frame, placeholder_text="1-x", font=ctk.CTkFont(size=13))
        self.entry_yb.pack(fill="x", padx=10, pady=2)

    def _build_triple_integral_fields(self):
        ctk.CTkLabel(self.param_frame, text="Limites X [Inf, Sup]:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=2)
        self.entry_xa = ctk.CTkEntry(self.param_frame, placeholder_text="0", font=ctk.CTkFont(size=13))
        self.entry_xa.pack(fill="x", padx=10, pady=2)
        self.entry_xb = ctk.CTkEntry(self.param_frame, placeholder_text="1", font=ctk.CTkFont(size=13))
        self.entry_xb.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(self.param_frame, text="Limites Y [Inf, Sup]:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(10, 2))
        self.entry_ya = ctk.CTkEntry(self.param_frame, placeholder_text="0", font=ctk.CTkFont(size=13))
        self.entry_ya.pack(fill="x", padx=10, pady=2)
        self.entry_yb = ctk.CTkEntry(self.param_frame, placeholder_text="1", font=ctk.CTkFont(size=13))
        self.entry_yb.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(self.param_frame, text="Limites Z [Inf, Sup]:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(10, 2))
        self.entry_za = ctk.CTkEntry(self.param_frame, placeholder_text="0", font=ctk.CTkFont(size=13))
        self.entry_za.pack(fill="x", padx=10, pady=2)
        self.entry_zb = ctk.CTkEntry(self.param_frame, placeholder_text="1", font=ctk.CTkFont(size=13))
        self.entry_zb.pack(fill="x", padx=10, pady=2)

    def _build_results_panel(self):
        self.res_frame = ctk.CTkFrame(self)
        self.res_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(
            self.res_frame,
            text="Procedimiento y Resultado Detallado:",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(anchor="w", padx=15, pady=5)

        self.txt_output = ctk.CTkTextbox(
            self.res_frame, height=180, font=ctk.CTkFont(size=13)
        )
        self.txt_output.pack(fill="x", padx=15, pady=5)

        self.plot_container = ctk.CTkFrame(self.res_frame)
        self.plot_container.pack(fill="both", expand=True, padx=15, pady=5)

    def _display_error(self, message: str):
        self.txt_output.configure(text_color="#FF5555")
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("1.0", f"[ATENCION / ERROR EN EL CALCULO]:\n{message}")

    def _display_success(self, text: str):
        self.txt_output.configure(text_color="#2b8a3e" if ctk.get_appearance_mode()=="Light" else "#51cf66")
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("1.0", text)

    def _execute_calculation(self):
        expr = self.entry_expr.get()
        op = self.op_var.get()

        try:
            if op == "Derivar Parcialmente":
                var = self.entry_var.get() or "x"
                order = self.entry_p1.get() or "1"
                res, steps = self.engine.evaluate_derivative(expr, var, order)

            elif op == "Evaluar Limite":
                var = self.entry_var.get() or "x"
                point = self.entry_p1.get() or "0"
                res, steps = self.engine.evaluate_limit(expr, var, point)

            elif op == "Integral Simple":
                var = self.entry_var.get() or "x"
                a = self.entry_p1.get() if hasattr(self, "entry_p1") else ""
                b = self.entry_p2.get() if hasattr(self, "entry_p2") else ""
                res, steps = self.engine.evaluate_integral(expr, var, a, b)

            elif op == "Integral Doble":
                res, steps = self.engine.evaluate_double_integral(
                    expr,
                    (self.entry_xa.get(), self.entry_xb.get()),
                    (self.entry_ya.get(), self.entry_yb.get()),
                )

            elif op == "Integral Triple":
                res, steps = self.engine.evaluate_triple_integral(
                    expr,
                    (self.entry_xa.get(), self.entry_xb.get()),
                    (self.entry_ya.get(), self.entry_yb.get()),
                    (self.entry_za.get(), self.entry_zb.get()),
                )
            else:
                raise ValueError("Operacion no valida.")

            self._display_success(steps)
            self._render_plot(expr)

        except (ValueError, ArithmeticError) as e:
            self._display_error(str(e))
        except Exception as e:
            self._display_error(f"Error inesperado de ejecucion: {str(e)}")

    def _render_plot(self, expr_str: str):
        for widget in self.plot_container.winfo_children():
            widget.destroy()

        # Failsafe para la variable Z o Integrales Multiples
        if "z" in expr_str.lower() or "doble" in self.op_var.get().lower() or "triple" in self.op_var.get().lower():
            lbl = ctk.CTkLabel(
                self.plot_container,
                text="[Grafica 2D omitida: Funcion multivariable con Z o integral multiple detectada]\nResultado analitico exacto mostrado arriba.",
                text_color="#FFA500",
                font=ctk.CTkFont(size=13, weight="bold"),
            )
            lbl.pack(expand=True)
            return

        try:
            fig, ax = plt.subplots(figsize=(5, 3.5), dpi=100)
            x_vals = np.linspace(-10, 10, 200)
            sym_expr = self.engine.parse_expression(expr_str)

            if self.engine.y in sym_expr.free_symbols:
                sym_expr = sym_expr.subs(self.engine.y, 1)

            f_num = lambda val: float(sym_expr.subs(self.engine.x, val).evalf())
            y_vals = [f_num(v) for v in x_vals]

            ax.plot(x_vals, y_vals, color="#1f77b4", linewidth=2)
            ax.set_title("Visualizacion Grafica Transversal f(x)", fontsize=11)
            ax.grid(True, linestyle="--", alpha=0.6)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception:
            lbl = ctk.CTkLabel(
                self.plot_container,
                text="[No se pudo renderizar la grafica para esta expresion]",
                text_color="#FFA500",
                font=ctk.CTkFont(size=13),
            )
            lbl.pack(expand=True)