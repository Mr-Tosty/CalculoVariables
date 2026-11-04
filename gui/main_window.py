"""Modulo de Interfaz de Usuario con Pestañas y Apuntes Integrados.

Diseno ultra visible, resultados llamativos y formulario integrado para evitar buscar notas.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from core.math_engine import MathEngine

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.engine = MathEngine()

        self.title("Asistente de Calculo Multivariable - Educativo Pro")
        self.geometry("1250 x 820")
        self.minsize(1000, 700)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self._build_main_layout()

    def _build_main_layout(self):
        # Contenedor de Pestañas Principal (Integra Calculadora y Apuntes)
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.tab_calc = self.tab_view.add("🧮 Calculadora")
        self.tab_notes = self.tab_view.add("📚 Apuntes y Fórmulas")

        self._build_calculator_tab(self.tab_calc)
        self._build_notes_tab(self.tab_notes)

        # Panel Derecho: Resultados Gigantes y Grafica (Siempre visible)
        self._build_results_panel()

    def _build_calculator_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)

        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # Funcion
        ctk.CTkLabel(
            scroll, text="1. Ingresa la Función f(x, y, z):",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 2))
        self.entry_expr = ctk.CTkEntry(
            scroll, placeholder_text="Ej: x^2 + 3*x*y - sin(z)",
            height=40, font=ctk.CTkFont(size=14)
        )
        self.entry_expr.pack(fill="x", padx=10, pady=2)

        # Operacion
        ctk.CTkLabel(
            scroll, text="2. Selecciona la Operación:",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=10, pady=(15, 2))
        self.op_var = ctk.StringVar(value="Derivar Parcialmente")
        self.combo_op = ctk.CTkOptionMenu(
            scroll,
            values=[
                "Derivar Parcialmente",
                "Evaluar Limite",
                "Integral Simple",
                "Integral Doble",
                "Integral Triple",
            ],
            variable=self.op_var,
            command=self._toggle_operation_fields,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.combo_op.pack(fill="x", padx=10, pady=2)

        # Marco Dinamico de Parametros
        self.param_frame = ctk.CTkFrame(scroll, fg_color=("gray90", "gray17"))
        self.param_frame.pack(fill="x", padx=5, pady=15)
        self._build_derivative_fields()

        # Boton de Calculo Ultra Llamativo
        btn_calc = ctk.CTkButton(
            scroll,
            text="🚀 CALCULAR AHORA",
            command=self._execute_calculation,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1f8a4c",
            hover_color="#145c32",
        )
        btn_calc.pack(fill="x", padx=10, pady=20)

    def _build_notes_tab(self, parent):
        """Pestaña con los apuntes y formulario exactos para no buscar fuera."""
        scroll = ctk.CTkScrollableFrame(parent)
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        title = ctk.CTkLabel(
            scroll, text="Formulario Oficial de Cálculo (Apuntes)",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(anchor="w", padx=10, pady=10)

        notes_text = (
            "📌 REGLAS BÁSICAS DE DERIVADAS E INTEGRALES:\n\n"
            "1. DERIVADAS:\n"
            "   • Constante: d/dx (k) = 0\n"
            "   • Identidad: d/dx (x) = 1\n"
            "   • Potencia: d/dx (x^n) = n * x^(n-1)\n"
            "   • Exponencial: d/dx (e^u) = e^u * du/dx\n"
            "   • Logarítmica: d/dx (ln u) = (1/u) * du/dx\n"
            "   • Trigonométricas: d/dx(sin u) = cos u * du/dx | d/dx(cos u) = -sin u * du/dx\n\n"
            "2. INTEGRALES:\n"
            "   • Constante: ∫ k dx = kx + C\n"
            "   • Potencia: ∫ x^n dx = x^(n+1) / (n+1) + C  (para n ≠ -1)\n"
            "   • Logarítmica: ∫ (1/x) dx = ln|x| + C\n"
            "   • Exponencial: ∫ e^x dx = e^x + C\n"
            "   • Trigonométricas: ∫ sin u du = -cos u + C | ∫ cos u du = sin u + C\n"
            "   • Por partes: ∫ u dv = u*v - ∫ v du\n\n"
            "3. CONSEJOS DE SINTAXIS EN LA APP:\n"
            "   • Usa siempre asteriscos para multiplicar: 3*x (no 3x).\n"
            "   • Usa '^' o '**' para potencias: x^2.\n"
            "   • Si usas la variable 'z', la gráfica 2D se omite automáticamente para darte "
            "el resultado analítico exacto sin errores."
        )

        lbl_notes = ctk.CTkLabel(
            scroll, text=notes_text, justify="left",
            font=ctk.CTkFont(size=13)
        )
        lbl_notes.pack(anchor="w", padx=10, pady=5)

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
        ctk.CTkLabel(self.param_frame, text="Variable (x, y, z):", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=2)
        self.entry_var = ctk.CTkEntry(self.param_frame, placeholder_text="x", height=32)
        self.entry_var.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(self.param_frame, text="Orden de derivada:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 2))
        self.entry_p1 = ctk.CTkEntry(self.param_frame, placeholder_text="1", height=32)
        self.entry_p1.pack(fill="x", padx=10, pady=10)

    def _build_limit_fields(self):
        ctk.CTkLabel(self.param_frame, text="Variable que tiende:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=2)
        self.entry_var = ctk.CTkEntry(self.param_frame, placeholder_text="x", height=32)
        self.entry_var.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(self.param_frame, text="Valor al que tiende (Punto):", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 2))
        self.entry_p1 = ctk.CTkEntry(self.param_frame, placeholder_text="0 o oo", height=32)
        self.entry_p1.pack(fill="x", padx=10, pady=10)

    def _build_single_integral_fields(self):
        ctk.CTkLabel(self.param_frame, text="Variable de integración:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=2)
        self.entry_var = ctk.CTkEntry(self.param_frame, placeholder_text="x", height=32)
        self.entry_var.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(self.param_frame, text="Límite Inf (a) y Sup (b) [Opcionales]:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 2))
        self.entry_p1 = ctk.CTkEntry(self.param_frame, placeholder_text="Ej: 0 (Inf)", height=32)
        self.entry_p1.pack(fill="x", padx=10, pady=2)
        self.entry_p2 = ctk.CTkEntry(self.param_frame, placeholder_text="Ej: 1 (Sup)", height=32)
        self.entry_p2.pack(fill="x", padx=10, pady=10)

    def _build_double_integral_fields(self):
        ctk.CTkLabel(self.param_frame, text="Límites X [Inf, Sup]:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=2)
        self.entry_xa = ctk.CTkEntry(self.param_frame, placeholder_text="0", height=28)
        self.entry_xa.pack(fill="x", padx=10, pady=2)
        self.entry_xb = ctk.CTkEntry(self.param_frame, placeholder_text="1", height=28)
        self.entry_xb.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(self.param_frame, text="Límites Y [Inf, Sup]:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(6, 2))
        self.entry_ya = ctk.CTkEntry(self.param_frame, placeholder_text="0", height=28)
        self.entry_ya.pack(fill="x", padx=10, pady=2)
        self.entry_yb = ctk.CTkEntry(self.param_frame, placeholder_text="1-x", height=28)
        self.entry_yb.pack(fill="x", padx=10, pady=10)

    def _build_triple_integral_fields(self):
        ctk.CTkLabel(self.param_frame, text="Límites X [Inf, Sup] | Y [Inf, Sup] | Z [Inf, Sup]:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=2)
        self.entry_xa = ctk.CTkEntry(self.param_frame, placeholder_text="X inf (0)", height=24)
        self.entry_xa.pack(fill="x", padx=10, pady=1)
        self.entry_xb = ctk.CTkEntry(self.param_frame, placeholder_text="X sup (1)", height=24)
        self.entry_xb.pack(fill="x", padx=10, pady=1)
        self.entry_ya = ctk.CTkEntry(self.param_frame, placeholder_text="Y inf (0)", height=24)
        self.entry_ya.pack(fill="x", padx=10, pady=1)
        self.entry_yb = ctk.CTkEntry(self.param_frame, placeholder_text="Y sup (1)", height=24)
        self.entry_yb.pack(fill="x", padx=10, pady=1)
        self.entry_za = ctk.CTkEntry(self.param_frame, placeholder_text="Z inf (0)", height=24)
        self.entry_za.pack(fill="x", padx=10, pady=1)
        self.entry_zb = ctk.CTkEntry(self.param_frame, placeholder_text="Z sup (1)", height=24)
        self.entry_zb.pack(fill="x", padx=10, pady=6)

    def _build_results_panel(self):
        """Panel derecho totalmente llamativo para que el usuario vea el resultado al instante."""
        self.res_frame = ctk.CTkFrame(self, fg_color=("gray85", "gray15"))
        self.res_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.res_frame.grid_rowconfigure(1, weight=2)
        self.res_frame.grid_rowconfigure(3, weight=3)
        self.res_frame.grid_columnconfigure(0, weight=1)

        # Encabezado muy visible
        lbl_header = ctk.CTkLabel(
            self.res_frame,
            text="🎯 RESULTADO Y PROCEDIMIENTO",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1f538d"
        )
        lbl_header.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))

        # Caja de texto grande con letra clara
        self.txt_output = ctk.CTkTextbox(
            self.res_frame, font=ctk.CTkFont(size=14, weight="bold")
        )
        self.txt_output.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
        self.txt_output.insert("1.0", ">> El resultado aparecerá aquí inmediatamente al presionar 'CALCULAR AHORA'.")

        # Contenedor de Gráfica
        lbl_plot = ctk.CTkLabel(
            self.res_frame,
            text="📈 VISUALIZACIÓN GRÁFICA",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        lbl_plot.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 2))

        self.plot_container = ctk.CTkFrame(self.res_frame, fg_color=("white", "gray20"))
        self.plot_container.grid(row=3, column=0, sticky="nsew", padx=15, pady=(5, 15))

    def _display_error(self, message: str):
        self.txt_output.configure(text_color="#FF3333")
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("1.0", f"❌ ERROR DE CÁLCULO O SINTAXIS:\n\n{message}")

    def _display_success(self, text: str):
        self.txt_output.configure(text_color="#2b8a3e" if ctk.get_appearance_mode()=="Light" else "#51cf66")
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("1.0", f"✅ ¡CÁLCULO EXITOSO!\n\n{text}")

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
                raise ValueError("Operación no reconocida.")

            self._display_success(steps)
            self._render_plot(expr)

        except (ValueError, ArithmeticError) as e:
            self._display_error(str(e))
        except Exception as e:
            self._display_error(f"Error inesperado: {str(e)}")

    def _render_plot(self, expr_str: str):
        for widget in self.plot_container.winfo_children():
            widget.destroy()

        if "z" in expr_str.lower() or "doble" in self.op_var.get().lower() or "triple" in self.op_var.get().lower():
            lbl = ctk.CTkLabel(
                self.plot_container,
                text="ℹ️ Gráfica 2D omitida por contener Z o Integral Múltiple.\nEl resultado analítico exacto está arriba.",
                text_color="#D97706",
                font=ctk.CTkFont(size=12, weight="bold"),
            )
            lbl.pack(expand=True, padx=10, pady=10)
            return

        try:
            fig, ax = plt.subplots(figsize=(4, 2.8), dpi=100)
            x_vals = np.linspace(-10, 10, 200)
            sym_expr = self.engine.parse_expression(expr_str)

            if self.engine.y in sym_expr.free_symbols:
                sym_expr = sym_expr.subs(self.engine.y, 1)

            f_num = lambda val: float(sym_expr.subs(self.engine.x, val).evalf())
            y_vals = [f_num(v) for v in x_vals]

            ax.plot(x_vals, y_vals, color="#1f77b4", linewidth=2.5)
            ax.set_title("Gráfica Transversal f(x)", fontsize=10, fontweight="bold")
            ax.grid(True, linestyle="--", alpha=0.6)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception:
            lbl = ctk.CTkLabel(
                self.plot_container,
                text="⚠️ No se pudo renderizar la gráfica para esta función.",
                text_color="#D97706",
                font=ctk.CTkFont(size=12),
            )
            lbl.pack(expand=True)