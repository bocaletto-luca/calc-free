# Software Name: Calc
# Author: Bocaletto Luca
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMenuBar, QLabel, QDialog

class Calcolatrice(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calc Free")  # Imposta il titolo della finestra
        self.setGeometry(100, 100, 400, 400)  # Imposta le dimensioni e la posizione iniziale della finestra
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)  # Imposta il widget centrale come contenitore principale
        self.layout = QVBoxLayout()  # Crea un layout verticale per organizzare gli elementi
        self.display = QLineEdit()  # Crea una casella di testo per il display della calcolatrice
        self.display.setStyleSheet("font-size: 20px; background-color: #f0f0f0;")  # Stile per il display
        self.layout.addWidget(self.display)  # Aggiunge il display al layout
        button_layout = [  # Definizione dei pulsanti in un elenco di liste
            ["7", "8", "9", "+"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "*"],
            ["0", ".", "=", "/", "CANC"],
            ["sqrt", "cbrt", "%"]
        ]
        for row in button_layout:  # Itera sulle righe dei pulsanti
            row_layout = QHBoxLayout()  # Crea un layout orizzontale per organizzare i pulsanti in una riga
            for button_text in row:  # Itera sui testi dei pulsanti nella riga corrente
                button = QPushButton(button_text)  # Crea un pulsante con il testo corrente
                if button_text == "CANC":
                    button.setStyleSheet("font-size: 20px; background-color: #f44336; color: #fff;")  # Imposta lo stile per il pulsante CANCEL
                else:
                    button.setStyleSheet("font-size: 20px; background-color: #4caf50; color: #fff;")  # Imposta lo stile per gli altri pulsanti
                button.clicked.connect(self.button_click)  # Collega il click del pulsante alla funzione button_click
                row_layout.addWidget(button)  # Aggiunge il pulsante al layout della riga corrente
            self.layout.addLayout(row_layout)  # Aggiunge il layout della riga al layout principale
        self.central_widget.setLayout(self.layout)  # Imposta il layout principale per il widget centrale
        self.result = None  # Variabile per memorizzare il risultato
        self.operator = None  # Variabile per memorizzare l'operatore corrente
        self.clear_flag = False  # Flag per determinare se cancellare l'input
        self.current_input = ""  # Memorizza l'input dell'utente corrente
        self.percent_flag = False  # Flag per gestire il calcolo percentuale
        menubar = self.menuBar()  # Crea una barra del menu
        about_menu = menubar.addMenu("About")  # Crea un menu "About"
        about_action = QAction("About", self)  # Crea un'azione "About"
        about_menu.addAction(about_action)  # Aggiunge l'azione al menu "About"
        about_action.triggered.connect(self.show_about_dialog)  # Collega l'azione al metodo show_about_dialog

    def button_click(self):
        button = self.sender()  # Ottiene il pulsante che ha generato il segnale
        text = button.text()  # Ottiene il testo del pulsante premuto
        if text.isnumeric() or text == ".":  # Se il testo è numerico o un punto decimale
            self.current_input += text  # Aggiunge il testo all'input corrente
            self.display.setText(self.current_input)  # Aggiorna il display con l'input corrente
        elif text in ["+", "-", "*", "/"]:  # Se il testo è un operatore
            if self.result is None:  # Se non c'è ancora un risultato parziale
                self.result = float(self.current_input)  # Memorizza l'input corrente come risultato
            else:
                self.result = self.perform_calculation()  # Altrimenti, esegui un calcolo parziale
            self.operator = text  # Memorizza l'operatore corrente
            self.clear_flag = True  # Imposta il flag per cancellare l'input
            self.current_input = ""  # Resetta l'input corrente
            self.percent_flag = False  # Resetta il flag percentuale
        elif text == "=":  # Se il testo è "=", esegui il calcolo finale
            if self.operator:
                if self.current_input:
                    operand = float(self.current_input)
                    if self.operator == "%":  # Se l'operatore è "%", calcola la percentuale
                        result = self.result * (operand / 100)
                    else:
                        result = self.perform_calculation(operand)  # Altrimenti, esegui l'operazione corrispondente
                    self.display.setText(str(result))  # Mostra il risultato nel display
                    self.clear_flag = True  # Imposta il flag per cancellare l'input successivo
                    self.operator = None  # Resetta l'operatore
                    self.current_input = ""  # Resetta l'input corrente
        elif text == "sqrt":  # Se il testo è "sqrt", calcola la radice quadrata
            if self.current_input:
                num = float(self.current_input)
                if num >= 0:
                    result = num ** 0.5
                    self.display.setText(str(result))
                    self.current_input = str(result)
                    self.percent_flag = False  # Resetta il flag percentuale
        elif text == "cbrt":  # Se il testo è "cbrt", calcola la radice cubica
            if self.current_input:
                num = float(self.current_input)
                result = num ** (1/3)
                self.display.setText(str(result))
                self.current_input = str(result)
                self.percent_flag = False  # Resetta il flag percentuale
        elif text == "%":  # Se il testo è "%", gestisci il calcolo percentuale
            if self.current_input and not self.percent_flag:
                value = float(self.current_input)
                self.result = value  # Memorizza il valore come risultato parziale
                self.operator = "%"  # Imposta l'operatore come "%"
                self.display.setText(self.current_input + "%")  # Mostra il simbolo "%" nel display
                self.current_input = ""  # Resetta l'input corrente
                self.percent_flag = True  # Imposta il flag percentuale
        elif text == "CANC":  # Se il testo è "CANC", resetta tutto
            self.current_input = ""
            self.display.clear()
            self.result = None

    def perform_calculation(self, operand=None):
        if operand is None:
            operand = float(self.current_input)
        if self.operator == "+":
            return self.result + operand
        elif self.operator == "-":
            return self.result - operand
        elif self.operator == "*":
            return self.result * operand
        elif self.operator == "/":
            if operand != 0:
                return self.result / operand
            else:
                return "Errore"

    def show_about_dialog(self):
        about_dialog = QDialog(self)  # Crea una finestra di dialogo "About"
        about_dialog.setWindowTitle("About")  # Imposta il titolo della finestra
        about_dialog.setFixedWidth(300)  # Imposta la larghezza fissa della finestra
        about_dialog.setFixedHeight(150)  # Imposta l'altezza fissa della finestra

        about_layout = QVBoxLayout()  # Crea un layout verticale per la finestra di dialogo
        about_label = QLabel("Questa è una semplice calcolatrice GUI in Python con PyQt6.")  # Crea una label con testo
        
        # Imposta il colore del testo su bianco
        about_label.setStyleSheet("color: #fff;")
        
        # Imposta lo sfondo della finestra "About" come i pulsanti
        palette = about_dialog.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#4caf50"))  # Colore personalizzato
        about_dialog.setPalette(palette)
        
        about_layout.addWidget(about_label)  # Aggiunge la label al layout
        about_dialog.setLayout(about_layout)  # Imposta il layout per la finestra di dialogo
        
        about_dialog.exec()  # Esegui la finestra di dialogo

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Crea un'applicazione PyQt
    window = Calcolatrice()  # Crea l'istanza della Calcolatrice
    about_action = window.menuBar().findChild(QAction, "About")  # Trova l'azione "About" nel menu
    if about_action:
        about_action.setStyleSheet("color: #fff;")  # Imposta il colore del testo dell'azione "About" in bianco

    window.show()  # Mostra la finestra della Calcolatrice
    sys.exit(app.exec())  # Esegui l'applicazione PyQt
