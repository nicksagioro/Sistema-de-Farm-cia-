"""
main.py - Janela principal Qt5 do sistema de farmacia.

Execucao:
    python main.py
"""

import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow,
    QTabWidget, QVBoxLayout, QWidget,
)

from api_client import APIClient
from ui_tabs import AbaClientes, AbaFornecedores, AbaMedicamentos, AbaVendas


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api   = APIClient()
        self.cache = {}
        self._build()
        self._carregar_tudo()

    def _build(self):
        self.setWindowTitle("Sistema de Gerenciamento de Farmacia")
        self.setGeometry(50, 50, 1400, 800)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        titulo = QLabel("FARMACIA - Sistema de Gerenciamento")
        fonte = QFont()
        fonte.setPointSize(16)
        fonte.setBold(True)
        titulo.setFont(fonte)
        layout.addWidget(titulo)

        self.aba_med  = AbaMedicamentos(self.api, self.cache)
        self.aba_cli  = AbaClientes(self.api, self.cache)
        self.aba_forn = AbaFornecedores(self.api, self.cache)
        self.aba_ven  = AbaVendas(self.api, self.cache)

        abas = QTabWidget()
        abas.addTab(self.aba_med,  "Medicamentos")
        abas.addTab(self.aba_cli,  "Clientes")
        abas.addTab(self.aba_forn, "Fornecedores")
        abas.addTab(self.aba_ven,  "Vendas")
        layout.addWidget(abas)

    def _carregar_tudo(self):
        # Fornecedores primeiro (medicamentos dependem deles no combobox)
        self.aba_forn.carregar()
        self.aba_med.carregar()
        self.aba_cli.carregar()
        self.aba_ven.carregar()


def main():
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
