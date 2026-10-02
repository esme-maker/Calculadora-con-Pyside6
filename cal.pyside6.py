import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class VentanaHistorial(QDialog):
    historial_borrado = Signal()

    def __init__(self, principal, parent=None):
        super().__init__(parent)
        self.principal = principal

        self.setWindowTitle("Historial de operaciones")
        self.resize(380, 330)
        self.setStyleSheet(
            f"""
            QDialog {{ background-color: {principal.ROSA_PASTEL}; }}
            QLabel {{
                color: {principal.ROSA_TEXTO};
                font-family: "Segoe UI";
                font-size: 17px;
                font-weight: bold;
                padding: 8px;
            }}
            QListWidget {{
                background-color: {principal.BLANCO};
                color: {principal.TINTA};
                border: none;
                font-family: "Consolas";
                font-size: 13px;
                padding: 6px;
            }}
            QListWidget::item:selected {{
                background-color: {principal.ROSA};
                color: {principal.TINTA};
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        titulo = QLabel("Historial", self)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.lista = QListWidget(self)
        self.lista.setSelectionMode(QListWidget.SingleSelection)
        self.lista.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(self.lista, 1)

        boton_borrar = QPushButton("Borrar historial", self)
        boton_borrar.setCursor(Qt.PointingHandCursor)
        boton_borrar.setFocusPolicy(Qt.NoFocus)
        boton_borrar.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {principal.ROSA_TEXTO};
                color: {principal.BLANCO};
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {principal.TINTA}; }}
            """
        )
        boton_borrar.clicked.connect(self.borrar_historial)
        layout.addWidget(boton_borrar)

    def borrar_historial(self):
        if self.principal is None or not self.principal.historial:
            return

        confirmacion = QMessageBox.question(
            self,
            "Borrar historial",
            "¿Seguro que quieres borrar todo el historial?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirmacion == QMessageBox.Yes:
            self.principal.historial.clear()
            self.lista.clear()
            self.historial_borrado.emit()


class DialogoInformacion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mi información")
        self.setFixedSize(430, 300)

        rosa_fondo = Calculadora.ROSA_FONDO
        rosa_texto = Calculadora.ROSA_TEXTO
        tinta = Calculadora.TINTA

        self.setStyleSheet(
            f"""
            QDialog {{ background-color: {rosa_fondo}; }}
            QLabel#titulo {{
                color: {rosa_texto};
                font-family: "Segoe UI";
                font-size: 21px;
                font-weight: bold;
            }}
            QLabel#texto {{
                color: {tinta};
                font-family: "Segoe UI";
                font-size: 15px;
            }}
            QPushButton {{
                background-color: {rosa_texto};
                color: {Calculadora.BLANCO};
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {tinta}; }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        titulo = QLabel("Hola", self)
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        texto = QLabel(
            "Esmeralda Arispe Jerez\n"
            "carrera de IGN. INFORMATICA\n"
            "segundo año\n\n"
            "Esta calculadora la hice con Python y PySide6.",
            self,
        )
        texto.setObjectName("texto")
        texto.setAlignment(Qt.AlignCenter)
        texto.setWordWrap(True)
        layout.addWidget(texto, 1)

        boton_cerrar = QPushButton("Cerrar", self)
        boton_cerrar.setCursor(Qt.PointingHandCursor)
        boton_cerrar.clicked.connect(self.accept)
        layout.addWidget(boton_cerrar)


class Calculadora(QMainWindow):
    BLANCO = "#FFFFFF"
    ROSA_FONDO = "#FDEFF4"
    ROSA_PASTEL = "#FBD5E3"
    ROSA = "#F6B9D0"
    ROSA_TEXTO = "#C98BA6"
    TINTA = "#8A4B66"

    LIMITE_HISTORIAL = 50

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora")
        self.setFixedSize(460, 700)
        self.setStyleSheet(
            f"""
            QMainWindow, QWidget#contenedor {{ background-color: {self.ROSA_FONDO}; }}
            QMenuBar {{ background-color: {self.ROSA_PASTEL}; color: {self.TINTA}; }}
            QMenuBar::item:selected {{ background-color: {self.ROSA}; }}
            QMenu {{
                background-color: {self.BLANCO};
                color: {self.TINTA};
                border: 1px solid {self.ROSA};
            }}
            QMenu::item:selected {{ background-color: {self.ROSA}; color: {self.TINTA}; }}
            """
        )

        self.numero = "0"
        self.texto_izquierda = ""
        self.pendiente_operador = ""
        self.acumulado = None
        self.esperando_numero = True
        self.resultado_mostrado = False
        self.historial = []
        self.ventana_historial = None

        self.crear_interfaz()
        self.crear_menu()
        self.configurar_teclado()

    # ---------- interfaz ----------

    def crear_interfaz(self):
        contenedor = QWidget(self)
        contenedor.setObjectName("contenedor")
        self.setCentralWidget(contenedor)

        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(20, 16, 20, 20)
        layout.setSpacing(0)

        titulo = QLabel("Calculadora", contenedor)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(
            f"""
            color: {self.ROSA_TEXTO};
            font-family: "Segoe UI";
            font-size: 26px;
            font-weight: bold;
            padding-bottom: 10px;
            """
        )
        layout.addWidget(titulo)

        marco_pantalla = QFrame(contenedor)
        marco_pantalla.setStyleSheet(
            f"""
            QFrame {{
                background-color: {self.ROSA_PASTEL};
                border-radius: 16px;
            }}
            """
        )
        marco_layout = QVBoxLayout(marco_pantalla)
        marco_layout.setContentsMargins(4, 4, 4, 4)

        self.etiqueta_pantalla = QLabel("0", marco_pantalla)
        self.etiqueta_pantalla.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.etiqueta_pantalla.setMinimumHeight(70)
        self.etiqueta_pantalla.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.etiqueta_pantalla.setStyleSheet(
            f"""
            background-color: {self.BLANCO};
            color: {self.TINTA};
            border-radius: 12px;
            font-family: "Consolas";
            font-size: 28px;
            font-weight: bold;
            padding: 14px 16px;
            """
        )
        marco_layout.addWidget(self.etiqueta_pantalla)
        layout.addWidget(marco_pantalla, 1)

        self.boton_historial = self.crear_boton("Historial", self.ROSA_PASTEL, self.TINTA, self.ROSA)
        self.boton_historial.clicked.connect(self.abrir_historial)
        layout.addWidget(self.boton_historial, 0)
        layout.addSpacing(14)

        panel = QWidget(contenedor)
        panel_layout = QGridLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(10)

        botones = [
            [
                ("C", self.limpiar, "claro"),
                ("⌫", self.borrar, "claro"),
                ("%", self.porcentaje, "claro"),
                ("÷", lambda: self.operar("/"), "operador"),
            ],
            [
                ("7", lambda: self.introducir("7"), "numero"),
                ("8", lambda: self.introducir("8"), "numero"),
                ("9", lambda: self.introducir("9"), "numero"),
                ("×", lambda: self.operar("*"), "operador"),
            ],
            [
                ("4", lambda: self.introducir("4"), "numero"),
                ("5", lambda: self.introducir("5"), "numero"),
                ("6", lambda: self.introducir("6"), "numero"),
                ("−", lambda: self.operar("-"), "operador"),
            ],
            [
                ("1", lambda: self.introducir("1"), "numero"),
                ("2", lambda: self.introducir("2"), "numero"),
                ("3", lambda: self.introducir("3"), "numero"),
                ("+", lambda: self.operar("+"), "operador"),
            ],
            [
                ("±", self.cambiar_signo, "claro"),
                ("0", lambda: self.introducir("0"), "numero"),
                (".", lambda: self.introducir("."), "numero"),
                ("=", self.igual, "igual"),
            ],
        ]

        for fila, botones_fila in enumerate(botones):
            for columna, (texto, comando, tipo) in enumerate(botones_fila):
                boton = self.crear_boton(
                    texto,
                    self.color_botones(tipo),
                    self.color_texto(tipo),
                    self.color_activo(tipo),
                )
                boton.clicked.connect(
                    lambda _checked=False, accion=comando: accion()
                )
                panel_layout.addWidget(boton, fila, columna)

        for indice in range(4):
            panel_layout.setColumnStretch(indice, 1)
        for indice in range(5):
            panel_layout.setRowStretch(indice, 1)

        layout.addWidget(panel, 4)

    def crear_boton(self, texto, fondo, texto_color, hover):
        boton = QPushButton(texto, self)
        boton.setCursor(Qt.PointingHandCursor)
        boton.setFocusPolicy(Qt.NoFocus)
        boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tamano = 19 if len(texto) <= 2 else 14
        boton.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {fondo};
                color: {texto_color};
                border: none;
                border-radius: 14px;
                font-family: "Segoe UI";
                font-size: {tamano}px;
                font-weight: bold;
                min-height: 46px;
            }}
            QPushButton:hover {{ background-color: {hover}; }}
            """
        )
        return boton

    def color_botones(self, tipo):
        if tipo == "igual":
            return self.ROSA_TEXTO
        if tipo == "operador":
            return self.ROSA
        if tipo == "claro":
            return self.ROSA_PASTEL
        return self.BLANCO

    def color_texto(self, tipo):
        return self.BLANCO if tipo == "igual" else self.TINTA

    def color_activo(self, tipo):
        if tipo == "igual":
            return self.TINTA
        if tipo == "numero":
            return self.ROSA_FONDO
        return self.ROSA

    def crear_menu(self):
        barra = QMenuBar(self)
        self.setMenuBar(barra)

        menu_principal = barra.addMenu("Menú")
        accion_info = menu_principal.addAction("Mi información")
        accion_info.triggered.connect(self.abrir_informacion)
        menu_principal.addSeparator()
        accion_historial = menu_principal.addAction("Historial")
        accion_historial.triggered.connect(self.abrir_historial)
        menu_principal.addSeparator()
        accion_salir = menu_principal.addAction("Salir")
        accion_salir.triggered.connect(self.close)

        menu_ayuda = barra.addMenu("Ayuda")
        accion_acerca = menu_ayuda.addAction("Acerca de")
        accion_acerca.triggered.connect(self.abrir_informacion)

        self.atajo_info = QShortcut(QKeySequence("Ctrl+I"), self)
        self.atajo_info.activated.connect(self.abrir_informacion)

    # ---------- teclado ----------

    def configurar_teclado(self):
        self.atajo_historial = QShortcut(QKeySequence("Ctrl+H"), self)
        self.atajo_historial.activated.connect(self.abrir_historial)
        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, event):
        tecla = event.key()
        texto = event.text()

        if tecla in (Qt.Key_Return, Qt.Key_Enter):
            self.igual()
            return
        if tecla == Qt.Key_Escape:
            self.limpiar()
            return
        if tecla == Qt.Key_Backspace:
            self.borrar()
            return
        if tecla == Qt.Key_Percent:
            self.porcentaje()
            return
        if tecla in (Qt.Key_Period, Qt.Key_Comma):
            self.introducir(".")
            return
        if tecla == Qt.Key_H:
            self.abrir_historial()
            return
        if texto in "0123456789":
            self.introducir(texto)
            return
        if texto in ("+", "-", "*", "/"):
            self.operar(texto)
            return

        super().keyPressEvent(event)

    # ---------- lógica ----------

    def refrescar_pantalla(self):
        self.etiqueta_pantalla.setText(
            self.texto_izquierda + self.pendiente_operador + self.numero
        )

    def introducir(self, valor):
        if self.resultado_mostrado:
            self.reiniciar_operacion()
            self.numero = ""

        texto = self.numero
        if valor == ".":
            if "." not in texto:
                self.numero = (texto if texto else "0") + "."
        elif texto in ("", "0"):
            self.numero = valor
        elif texto in ("-", "-0"):
            self.numero = "-" + valor
        else:
            self.numero = texto + valor

        self.esperando_numero = False
        self.refrescar_pantalla()

    def valor_actual(self):
        try:
            return float(self.numero)
        except ValueError:
            return 0.0

    def formatear(self, numero):
        if abs(numero) < 1e-12:
            return "0"
        if numero.is_integer() and abs(numero) < 1e15:
            return str(int(numero))
        return f"{numero:.12g}"

    def calcular(self, izquierda, derecha, operador):
        if operador == "+":
            return izquierda + derecha
        if operador == "-":
            return izquierda - derecha
        if operador == "*":
            return izquierda * derecha
        if operador == "/":
            if derecha == 0:
                raise ZeroDivisionError
            return izquierda / derecha
        raise ValueError

    def operar(self, operador):
        if self.pendiente_operador and not self.esperando_numero:
            derecha = self.valor_actual()
            try:
                resultado = self.calcular(
                    self.acumulado, derecha, self.pendiente_operador
                )
            except ZeroDivisionError:
                self.mostrar_error(self.acumulado, derecha, self.pendiente_operador)
                return
            self.acumulado = resultado
            self.texto_izquierda = self.formatear(resultado)
        else:
            self.acumulado = self.valor_actual()
            self.texto_izquierda = self.formatear(self.acumulado)

        self.pendiente_operador = operador
        self.esperando_numero = True
        self.resultado_mostrado = False
        self.numero = ""
        self.refrescar_pantalla()

    def igual(self):
        if not self.pendiente_operador or self.acumulado is None:
            return
        if self.esperando_numero and self.numero == "":
            return

        izquierda = self.formatear(self.acumulado)
        derecha = self.valor_actual()
        operador = self.pendiente_operador

        try:
            resultado = self.calcular(self.acumulado, derecha, operador)
        except ZeroDivisionError:
            self.mostrar_error(self.acumulado, derecha, operador)
            return

        self.registrar(
            f"{izquierda} {operador} {self.formatear(derecha)} = "
            f"{self.formatear(resultado)}"
        )

        self.numero = self.formatear(resultado)
        self.texto_izquierda = ""
        self.pendiente_operador = ""
        self.acumulado = None
        self.esperando_numero = True
        self.resultado_mostrado = True
        self.refrescar_pantalla()

    def porcentaje(self):
        self.numero = self.formatear(self.valor_actual() / 100)
        self.esperando_numero = False
        self.resultado_mostrado = False
        self.refrescar_pantalla()

    def cambiar_signo(self):
        texto = self.numero
        if texto == "":
            return
        if texto.startswith("-"):
            self.numero = texto[1:]
        elif texto != "0":
            self.numero = "-" + texto
        self.refrescar_pantalla()

    def registrar(self, texto):
        self.historial.append(texto)
        if len(self.historial) > self.LIMITE_HISTORIAL:
            del self.historial[0]
        self.actualizar_historial()

    def mostrar_error(self, izquierda, derecha, operador):
        self.registrar(
            f"{self.formatear(izquierda)} {operador} {self.formatear(derecha)}"
            " = Error (división entre cero)"
        )
        self.reiniciar_operacion()
        self.numero = "Error"
        self.esperando_numero = True
        self.resultado_mostrado = True
        self.refrescar_pantalla()
        QMessageBox.critical(
            self,
            "División entre cero",
            "No se puede dividir entre cero.",
        )

    def borrar(self):
        if self.resultado_mostrado:
            self.limpiar()
            return

        texto = self.numero
        if texto:
            self.numero = texto[:-1] if len(texto) > 1 else ""
        elif self.pendiente_operador:
            self.pendiente_operador = ""
            self.texto_izquierda = self.texto_izquierda[:-1]
            self.acumulado = None

        self.refrescar_pantalla()

    def limpiar(self):
        self.reiniciar_operacion()
        self.numero = "0"
        self.refrescar_pantalla()

    def reiniciar_operacion(self):
        self.texto_izquierda = ""
        self.pendiente_operador = ""
        self.acumulado = None
        self.esperando_numero = True
        self.resultado_mostrado = False

    # ---------- historial ----------

    def abrir_historial(self):
        if self.ventana_historial is not None:
            self.ventana_historial.show()
            self.ventana_historial.raise_()
            self.ventana_historial.activateWindow()
            return

        ventana = VentanaHistorial(self, self)
        ventana.historial_borrado.connect(self.actualizar_historial)
        ventana.finished.connect(self.al_cerrar_historial)
        self.ventana_historial = ventana
        self.actualizar_historial()
        ventana.show()

    def al_cerrar_historial(self, _resultado):
        self.ventana_historial = None

    def borrar_historial(self):
        if not self.historial:
            return

        confirmacion = QMessageBox.question(
            self,
            "Borrar historial",
            "¿Seguro que quieres borrar todo el historial?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirmacion == QMessageBox.Yes:
            self.historial.clear()
            self.actualizar_historial()

    def actualizar_historial(self):
        if self.ventana_historial is None:
            return

        lista = self.ventana_historial.lista
        lista.clear()
        for indice, operacion in enumerate(self.historial, start=1):
            lista.addItem(f"{indice}. {operacion}")
        lista.scrollToBottom()

    # ---------- información ----------

    def abrir_informacion(self):
        DialogoInformacion(self).exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    ventana = Calculadora()
    ventana.show()
    sys.exit(app.exec())