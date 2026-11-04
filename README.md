\# Asistente de Cálculo Multivariable (MVP)



Un entorno de simulación numérica y simbólica lineal diseñado de forma nativa para el escritorio. Este software permite procesar, validar y resolver operaciones complejas de cálculo de varias variables (límites, derivadas parciales de orden superior/mixtas e integrales) a través de una arquitectura limpia y modular de software, ofreciendo un desglose analítico paso a paso y una interfaz gráfica interactiva.



\---



\## 🚀 Características Clave



\- \*\*Interfaz Gráfica Intuitiva:\*\* Formularios ordenados y controles dinámicos construidos con `customtkinter` que guían al usuario según la operación seleccionada.

\- \*\*Motor Matemático Avanzado:\*\* Procesamiento simbólico de alta precisión respaldado por `SymPy`.

\- \*\*Desglose de Procedimientos:\*\* Registro analítico de los pasos lógicos intermedios realizados por el sistema en cada cálculo.

\- \*\*Gráficos 2D Integrados:\*\* Visualización interactiva mediante cortes transversales f(x) generados con `matplotlib`.

\- \*\*Mitigación de Indeterminaciones:\*\* Algoritmos de aproximación por entornos para resolver límites complejos cuando la sustitución directa genera conflictos.

\- \*\*Sistema Failsafe Incorporado:\*\* 

&#x20; - Captura y manejo estructurado de excepciones matemáticas para evitar bloqueos (\*crashes\*) en producción.

&#x20; - Conmutación automática que congela el renderizado 2D al detectar la variable z para proteger la memoria, priorizando el resultado algebraico exacto.



\---



\## 🛠️ Requisitos del Sistema



Para ejecutar este proyecto de forma local, necesitas contar con \*\*Python 3.10 o superior\*\* instalado en tu sistema. El software utiliza las siguientes dependencias de terceros:



\- \*\*`customtkinter`\*\* (Para el entorno visual moderno)

\- \*\*`sympy`\*\* (Para el motor de álgebra computacional)

\- \*\*`matplotlib`\*\* (Para el renderizado de gráficos de curvas)

\- \*\*`numpy`\*\* (Para la vectorización y muestreo de puntos en la gráfica)



\---



\## 📥 Instalación y Configuración



Sigue estos pasos secuenciales en tu terminal para clonar y preparar el entorno del proyecto:



1\. \*\*Clona el repositorio o descarga los archivos fuentes:\*\*

&#x20;  ```bash

&#x20;  git clone https://github.com

&#x20;  cd calculus-multivariable-assistant

&#x20;  ```



2\. \*\*Instala las dependencias requeridas:\*\*

&#x20;  Puedes instalar los paquetes necesarios utilizando el gestor de paquetes de Python (`pip`):

&#x20;  ```bash

&#x20;  pip install customtkinter sympy matplotlib numpy

&#x20;  ```



\---



\## 🕹️ Ejecución del Software



El proyecto sigue una arquitectura de diseño modular inspirada en componentes tradicionales de desarrollo corporativo. El arranque de la interfaz se gestiona de manera centralizada a través del lanzador principal:



Para iniciar la aplicación, ejecuta el siguiente comando desde la raíz del proyecto:

```bash

python main.py

```



\---



\## 📐 Reglas de Sintaxis para Entrada de Datos



Para garantizar un procesamiento correcto por parte del analizador léxico interno y evitar excepciones de compilación, el usuario debe seguir las siguientes pautas de escritura en el campo de la función:



| Operador / Elemento | Escritura en la App | Ejemplo Válido | Significado Matemático |

| :--- | :--- | :--- | :--- |

| \*\*Multiplicación\*\* | Debe ser explícita con `\*` | `3\*x\*y` | 3xy (No escribir `3xy`) |

| \*\*Potencia\*\* | Doble asterisco `\*\*` | `x\*\*3` | x³ (Soporta también `^`) |

| \*\*Raíz Cuadrada\*\* | Función `sqrt()` | `sqrt(x\*\*2 + y\*\*2)` | \\(\\sqrt{x^2 + y^2}\\) |

| \*\*Funciones Trig.\*\* | En minúsculas | `sin(x) + cos(y)` | \\(\\sin(x) + \\cos(y)\\) |

| \*\*Constantes\*\* | En minúsculas | `pi` o `e` | Valores de π y e con máxima precisión |



\---



\## 📂 Estructura del Repositorio



```text

📦 calculus\_mvp

&#x20;┣ 📂 core                      <- Paquete de lógica matemática pura

&#x20;| ┣ 📜 \_\_init\_\_.py             <- Marcador de inicialización estructural

&#x20;| ┗ 📜 math\_engine.py          <- Procesamiento simbólico de SymPy

&#x20;┣ 📂 gui                       <- Paquete de componentes visuales (UX/UI)

&#x20;| ┣ 📜 \_\_init\_\_.py             <- Marcador de inicialización estructural

&#x20;| ┗ 📜 main\_window.py          <- Formulario y layouts de CustomTkinter

&#x20;┣ 📜 .gitignore                <- Archivo de exclusión de elementos locales (\_\_pycache\_\_)

&#x20;┣ 📜 main.py                   <- Lanzador (Launcher) principal del sistema

&#x20;┗ 📜 README.md                 <- Documentación general del proyecto

```



