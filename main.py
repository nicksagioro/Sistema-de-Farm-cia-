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

from api.api_client import APIClient
from ui.tabs.ui_tabs import AbaClientes, AbaFornecedores, AbaMedicamentos, AbaVendas


class JanelaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()
        self.api = APIClient()
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

        # Inicializa as abas
        self.aba_med = AbaMedicamentos(self.api, self.cache)
        self.aba_cli = AbaClientes(self.api, self.cache)
        self.aba_forn = AbaFornecedores(self.api, self.cache)
        self.aba_ven = AbaVendas(self.api, self.cache)

        abas = QTabWidget()
        abas.addTab(self.aba_med, "Medicamentos")
        abas.addTab(self.aba_cli, "Clientes")
        abas.addTab(self.aba_forn, "Fornecedores")
        abas.addTab(self.aba_ven, "Vendas")
        layout.addWidget(abas)

    def _carregar_tudo(self):
        """Busca os dados da API e recarrega os componentes visuais das abas"""
        try:
            print("Tentando conectar com a API e carregar dados do host...")
            
            # Testa a conexão buscando os dados das rotas
            self.api.listar_clientes()
            self.api.listar_fornecedores()
            self.api.listar_medicamentos()
            self.api.listar_vendas()
            
            print("Sucesso! Conectado à API.")
            
            # Executa o carregamento visual de cada aba (na ordem correta de dependência)
            print("Populando tabelas da interface...")
            self.aba_forn.carregar()
            self.aba_med.carregar()
            self.aba_cli.carregar()
            self.aba_ven.carregar()
            print("Tudo pronto e carregado!")
            
        except Exception as e:
            print("\n" + "="*50)
            print(f"ERRO CRÍTICO DE CONEXÃO: {e}")
            print("Verifique se o container da API Docker está rodando na porta 8080.")
            print("="*50 + "\n")


def main():
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()