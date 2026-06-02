import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTabWidget, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit,
    QLabel, QHeaderView, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit,
    QTextEdit, QFormLayout, QDialog
)
from PyQt5.QtCore import Qt, QDate, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from api_client import APIClient
from widgets import (
    DialogCadastroMedicamento, DialogCadastroCliente, 
    DialogCadastroFornecedor, preencher_tabela
)
from datetime import datetime
import json

class AtualizadorDados(QThread):
    """Thread para atualizar dados sem travar a interface"""
    dados_atualizados = pyqtSignal(str, list)
    erro = pyqtSignal(str, str)
    
    def __init__(self, api: APIClient, tipo: str):
        super().__init__()
        self.api = api
        self.tipo = tipo
    
    def run(self):
        try:
            if self.tipo == "medicamentos":
                dados = self.api.listar_medicamentos()
            elif self.tipo == "clientes":
                dados = self.api.listar_clientes()
            elif self.tipo == "fornecedores":
                dados = self.api.listar_fornecedores()
            elif self.tipo == "vendas":
                dados = self.api.listar_vendas()
            else:
                dados = []
            
            self.dados_atualizados.emit(self.tipo, dados)
        except Exception as e:
            self.erro.emit(self.tipo, str(e))


class JanelaPrincipal(QMainWindow):
    """Janela principal da aplicação de farmácia"""
    
    def __init__(self):
        super().__init__()
        self.api = APIClient()
        self.init_ui()
        self.carregar_dados()
    
    def init_ui(self):
        self.setWindowTitle("Sistema de Gerenciamento de Farmácia")
        self.setGeometry(50, 50, 1400, 800)
        
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout()
        
        # Título
        titulo = QLabel("FARMÁCIA - Sistema de Gerenciamento")
        fonte = QFont()
        fonte.setPointSize(16)
        fonte.setBold(True)
        titulo.setFont(fonte)
        layout_principal.addWidget(titulo)
        
        # Abas
        self.abas = QTabWidget()
        
        # Aba Medicamentos
        self.aba_medicamentos = self.criar_aba_medicamentos()
        self.abas.addTab(self.aba_medicamentos, "Medicamentos")
        
        # Aba Clientes
        self.aba_clientes = self.criar_aba_clientes()
        self.abas.addTab(self.aba_clientes, "Clientes")
        
        # Aba Fornecedores
        self.aba_fornecedores = self.criar_aba_fornecedores()
        self.abas.addTab(self.aba_fornecedores, "Fornecedores")
        
        # Aba Vendas
        self.aba_vendas = self.criar_aba_vendas()
        self.abas.addTab(self.aba_vendas, "Vendas")
        
        layout_principal.addWidget(self.abas)
        widget_central.setLayout(layout_principal)
    
    def criar_aba_medicamentos(self) -> QWidget:
        """Cria a aba de medicamentos"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Barra de ferramentas
        layout_ferramentas = QHBoxLayout()
        self.busca_medicamento = QLineEdit()
        self.busca_medicamento.setPlaceholderText("Buscar por nome...")
        self.busca_medicamento.textChanged.connect(self.filtrar_medicamentos)
        
        btn_novo = QPushButton("+ Novo Medicamento")
        btn_novo.clicked.connect(self.novo_medicamento)
        
        btn_editar = QPushButton("✎ Editar")
        btn_editar.clicked.connect(self.editar_medicamento)
        
        btn_deletar = QPushButton("✕ Deletar")
        btn_deletar.clicked.connect(self.deletar_medicamento)
        
        btn_atualizar = QPushButton("⟳ Atualizar")
        btn_atualizar.clicked.connect(lambda: self.carregar_dados("medicamentos"))
        
        layout_ferramentas.addWidget(QLabel("Buscar:"))
        layout_ferramentas.addWidget(self.busca_medicamento)
        layout_ferramentas.addWidget(btn_novo)
        layout_ferramentas.addWidget(btn_editar)
        layout_ferramentas.addWidget(btn_deletar)
        layout_ferramentas.addWidget(btn_atualizar)
        
        layout.addLayout(layout_ferramentas)
        
        # Tabela
        self.tabela_medicamentos = QTableWidget()
        self.tabela_medicamentos.setColumnCount(8)
        self.tabela_medicamentos.setHorizontalHeaderLabels([
            "ID", "Nome", "Princípio Ativo", "Preço", "Estoque", "Lote", "Validade", "Fabricante"
        ])
        self.tabela_medicamentos.resizeColumnsToContents()
        header = self.tabela_medicamentos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.tabela_medicamentos)
        widget.setLayout(layout)
        return widget
    
    def criar_aba_clientes(self) -> QWidget:
        """Cria a aba de clientes"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Barra de ferramentas
        layout_ferramentas = QHBoxLayout()
        self.busca_cliente = QLineEdit()
        self.busca_cliente.setPlaceholderText("Buscar por nome ou CPF...")
        self.busca_cliente.textChanged.connect(self.filtrar_clientes)
        
        btn_novo = QPushButton("+ Novo Cliente")
        btn_novo.clicked.connect(self.novo_cliente)
        
        btn_editar = QPushButton("✎ Editar")
        btn_editar.clicked.connect(self.editar_cliente)
        
        btn_deletar = QPushButton("✕ Deletar")
        btn_deletar.clicked.connect(self.deletar_cliente)
        
        btn_atualizar = QPushButton("⟳ Atualizar")
        btn_atualizar.clicked.connect(lambda: self.carregar_dados("clientes"))
        
        layout_ferramentas.addWidget(QLabel("Buscar:"))
        layout_ferramentas.addWidget(self.busca_cliente)
        layout_ferramentas.addWidget(btn_novo)
        layout_ferramentas.addWidget(btn_editar)
        layout_ferramentas.addWidget(btn_deletar)
        layout_ferramentas.addWidget(btn_atualizar)
        
        layout.addLayout(layout_ferramentas)
        
        # Tabela
        self.tabela_clientes = QTableWidget()
        self.tabela_clientes.setColumnCount(6)
        self.tabela_clientes.setHorizontalHeaderLabels([
            "ID", "CPF", "Nome", "Email", "Telefone", "Ativo"
        ])
        header = self.tabela_clientes.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.tabela_clientes)
        widget.setLayout(layout)
        return widget
    
    def criar_aba_fornecedores(self) -> QWidget:
        """Cria a aba de fornecedores"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Barra de ferramentas
        layout_ferramentas = QHBoxLayout()
        self.busca_fornecedor = QLineEdit()
        self.busca_fornecedor.setPlaceholderText("Buscar por nome ou CNPJ...")
        self.busca_fornecedor.textChanged.connect(self.filtrar_fornecedores)
        
        btn_novo = QPushButton("+ Novo Fornecedor")
        btn_novo.clicked.connect(self.novo_fornecedor)
        
        btn_editar = QPushButton("✎ Editar")
        btn_editar.clicked.connect(self.editar_fornecedor)
        
        btn_deletar = QPushButton("✕ Deletar")
        btn_deletar.clicked.connect(self.deletar_fornecedor)
        
        btn_atualizar = QPushButton("⟳ Atualizar")
        btn_atualizar.clicked.connect(lambda: self.carregar_dados("fornecedores"))
        
        layout_ferramentas.addWidget(QLabel("Buscar:"))
        layout_ferramentas.addWidget(self.busca_fornecedor)
        layout_ferramentas.addWidget(btn_novo)
        layout_ferramentas.addWidget(btn_editar)
        layout_ferramentas.addWidget(btn_deletar)
        layout_ferramentas.addWidget(btn_atualizar)
        
        layout.addLayout(layout_ferramentas)
        
        # Tabela
        self.tabela_fornecedores = QTableWidget()
        self.tabela_fornecedores.setColumnCount(6)
        self.tabela_fornecedores.setHorizontalHeaderLabels([
            "ID", "Nome", "CNPJ", "Email", "Telefone", "Ativo"
        ])
        header = self.tabela_fornecedores.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.tabela_fornecedores)
        widget.setLayout(layout)
        return widget
    
    def criar_aba_vendas(self) -> QWidget:
        """Cria a aba de vendas"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Barra de ferramentas
        layout_ferramentas = QHBoxLayout()
        
        btn_nova = QPushButton("+ Nova Venda")
        btn_nova.clicked.connect(self.nova_venda)
        
        btn_visualizar = QPushButton("👁 Visualizar")
        btn_visualizar.clicked.connect(self.visualizar_venda)
        
        btn_deletar = QPushButton("✕ Deletar")
        btn_deletar.clicked.connect(self.deletar_venda)
        
        btn_atualizar = QPushButton("⟳ Atualizar")
        btn_atualizar.clicked.connect(lambda: self.carregar_dados("vendas"))
        
        layout_ferramentas.addWidget(btn_nova)
        layout_ferramentas.addWidget(btn_visualizar)
        layout_ferramentas.addWidget(btn_deletar)
        layout_ferramentas.addWidget(btn_atualizar)
        layout_ferramentas.addStretch()
        
        layout.addLayout(layout_ferramentas)
        
        # Tabela
        self.tabela_vendas = QTableWidget()
        self.tabela_vendas.setColumnCount(5)
        self.tabela_vendas.setHorizontalHeaderLabels([
            "ID", "Cliente ID", "Data", "Total", "Desconto"
        ])
        header = self.tabela_vendas.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.tabela_vendas)
        widget.setLayout(layout)
        return widget
    
    def carregar_dados(self, tipo: str = "all"):
        """Carrega dados da API"""
        try:
            if tipo == "all" or tipo == "medicamentos":
                medicamentos = self.api.listar_medicamentos()
                self.medicamentos_cache = medicamentos
                colunas = ["id", "nome", "principio_ativo", "preco", "estoque", "lote", "data_validade", "fabricante"]
                dados_tabela = [[str(m.get(col, "")) for col in colunas] for m in medicamentos]
                
                self.tabela_medicamentos.setRowCount(len(dados_tabela))
                for row, dados in enumerate(dados_tabela):
                    for col, valor in enumerate(dados):
                        self.tabela_medicamentos.setItem(row, col, QTableWidgetItem(valor))
            
            if tipo == "all" or tipo == "clientes":
                clientes = self.api.listar_clientes()
                self.clientes_cache = clientes
                colunas = ["id", "cpf", "nome", "email", "telefone", "ativo"]
                dados_tabela = [[str(c.get(col, "")) for col in colunas] for c in clientes]
                
                self.tabela_clientes.setRowCount(len(dados_tabela))
                for row, dados in enumerate(dados_tabela):
                    for col, valor in enumerate(dados):
                        self.tabela_clientes.setItem(row, col, QTableWidgetItem(valor))
            
            if tipo == "all" or tipo == "fornecedores":
                fornecedores = self.api.listar_fornecedores()
                self.fornecedores_cache = fornecedores
                colunas = ["id", "nome", "cnpj", "email", "telefone", "ativo"]
                dados_tabela = [[str(f.get(col, "")) for col in colunas] for f in fornecedores]
                
                self.tabela_fornecedores.setRowCount(len(dados_tabela))
                for row, dados in enumerate(dados_tabela):
                    for col, valor in enumerate(dados):
                        self.tabela_fornecedores.setItem(row, col, QTableWidgetItem(valor))
            
            if tipo == "all" or tipo == "vendas":
                vendas = self.api.listar_vendas()
                self.vendas_cache = vendas
                colunas = ["id", "id_cliente", "data_venda", "total", "desconto"]
                
                self.tabela_vendas.setRowCount(len(vendas))
                for row, venda in enumerate(vendas):
                    for col, coluna in enumerate(colunas):
                        valor = str(venda.get(coluna, ""))
                        self.tabela_vendas.setItem(row, col, QTableWidgetItem(valor))
        
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados: {str(e)}")
    
    # ==================== MEDICAMENTOS ====================
    
    def novo_medicamento(self):
        fornecedores = getattr(self, 'fornecedores_cache', [])
        dialog = DialogCadastroMedicamento(self, fornecedores=fornecedores)
        dialog.medicamento_salvo.connect(self.salvar_medicamento)
        dialog.exec_()
    
    def salvar_medicamento(self, dados):
        med_id = dados.get("id")
        try:
            if med_id:
                self.api.atualizar_medicamento(med_id, dados)
                QMessageBox.information(self, "Sucesso", "Medicamento atualizado com sucesso!")
            else:
                self.api.criar_medicamento(dados)
                QMessageBox.information(self, "Sucesso", "Medicamento criado com sucesso!")
            self.carregar_dados("medicamentos")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar medicamento: {str(e)}")
    
    def editar_medicamento(self):
        linha = self.tabela_medicamentos.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um medicamento para editar")
            return
        
        med_id = int(self.tabela_medicamentos.item(linha, 0).text())
        medicamento = self.api.obter_medicamento(med_id)
        
        if medicamento:
            fornecedores = getattr(self, 'fornecedores_cache', [])
            medicamento['id'] = med_id
            dialog = DialogCadastroMedicamento(self, medicamento=medicamento, fornecedores=fornecedores)
            dialog.medicamento_salvo.connect(self.salvar_medicamento)
            dialog.exec_()
    
    def deletar_medicamento(self):
        linha = self.tabela_medicamentos.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um medicamento para deletar")
            return
        
        med_id = int(self.tabela_medicamentos.item(linha, 0).text())
        resposta = QMessageBox.question(self, "Confirmar", "Deseja realmente deletar este medicamento?", 
                                       QMessageBox.Yes | QMessageBox.No)
        
        if resposta == QMessageBox.Yes:
            if self.api.deletar_medicamento(med_id):
                QMessageBox.information(self, "Sucesso", "Medicamento deletado com sucesso!")
                self.carregar_dados("medicamentos")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao deletar medicamento")
    
    def filtrar_medicamentos(self):
        texto = self.busca_medicamento.text().lower()
        for row in range(self.tabela_medicamentos.rowCount()):
            nome = self.tabela_medicamentos.item(row, 1).text().lower()
            visivel = texto in nome
            self.tabela_medicamentos.setRowHidden(row, not visivel)
    
    # ==================== CLIENTES ====================
    
    def novo_cliente(self):
        dialog = DialogCadastroCliente(self)
        dialog.cliente_salvo.connect(self.salvar_cliente)
        dialog.exec_()
    
    def salvar_cliente(self, dados):
        try:
            self.api.criar_cliente(dados)
            QMessageBox.information(self, "Sucesso", "Cliente criado com sucesso!")
            self.carregar_dados("clientes")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar cliente: {str(e)}")
    
    def editar_cliente(self):
        linha = self.tabela_clientes.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para editar")
            return
        
        cliente_id = int(self.tabela_clientes.item(linha, 0).text())
        cliente = self.api.obter_cliente(cliente_id)
        
        if cliente:
            cliente['id'] = cliente_id
            dialog = DialogCadastroCliente(self, cliente=cliente)
            dialog.cliente_salvo.connect(self.salvar_cliente_edicao)
            dialog.exec_()
    
    def salvar_cliente_edicao(self, dados):
        linha = self.tabela_clientes.currentRow()
        cliente_id = int(self.tabela_clientes.item(linha, 0).text())
        
        try:
            self.api.atualizar_cliente(cliente_id, dados)
            QMessageBox.information(self, "Sucesso", "Cliente atualizado com sucesso!")
            self.carregar_dados("clientes")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar cliente: {str(e)}")
    
    def deletar_cliente(self):
        linha = self.tabela_clientes.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para deletar")
            return
        
        cliente_id = int(self.tabela_clientes.item(linha, 0).text())
        resposta = QMessageBox.question(self, "Confirmar", "Deseja realmente deletar este cliente?",
                                       QMessageBox.Yes | QMessageBox.No)
        
        if resposta == QMessageBox.Yes:
            if self.api.deletar_cliente(cliente_id):
                QMessageBox.information(self, "Sucesso", "Cliente deletado com sucesso!")
                self.carregar_dados("clientes")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao deletar cliente")
    
    def filtrar_clientes(self):
        texto = self.busca_cliente.text().lower()
        for row in range(self.tabela_clientes.rowCount()):
            nome = self.tabela_clientes.item(row, 2).text().lower()
            cpf = self.tabela_clientes.item(row, 1).text().lower()
            visivel = texto in nome or texto in cpf
            self.tabela_clientes.setRowHidden(row, not visivel)
    
    # ==================== FORNECEDORES ====================
    
    def novo_fornecedor(self):
        dialog = DialogCadastroFornecedor(self)
        dialog.fornecedor_salvo.connect(self.salvar_fornecedor)
        dialog.exec_()
    
    def salvar_fornecedor(self, dados):
        try:
            self.api.criar_fornecedor(dados)
            QMessageBox.information(self, "Sucesso", "Fornecedor criado com sucesso!")
            self.carregar_dados("fornecedores")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar fornecedor: {str(e)}")
    
    def editar_fornecedor(self):
        linha = self.tabela_fornecedores.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um fornecedor para editar")
            return
        
        fornecedor_id = int(self.tabela_fornecedores.item(linha, 0).text())
        fornecedor = self.api.obter_fornecedor(fornecedor_id)
        
        if fornecedor:
            fornecedor['id'] = fornecedor_id
            dialog = DialogCadastroFornecedor(self, fornecedor=fornecedor)
            dialog.fornecedor_salvo.connect(self.salvar_fornecedor_edicao)
            dialog.exec_()
    
    def salvar_fornecedor_edicao(self, dados):
        linha = self.tabela_fornecedores.currentRow()
        fornecedor_id = int(self.tabela_fornecedores.item(linha, 0).text())
        
        try:
            self.api.atualizar_fornecedor(fornecedor_id, dados)
            QMessageBox.information(self, "Sucesso", "Fornecedor atualizado com sucesso!")
            self.carregar_dados("fornecedores")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar fornecedor: {str(e)}")
    
    def deletar_fornecedor(self):
        linha = self.tabela_fornecedores.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um fornecedor para deletar")
            return
        
        fornecedor_id = int(self.tabela_fornecedores.item(linha, 0).text())
        resposta = QMessageBox.question(self, "Confirmar", "Deseja realmente deletar este fornecedor?",
                                       QMessageBox.Yes | QMessageBox.No)
        
        if resposta == QMessageBox.Yes:
            if self.api.deletar_fornecedor(fornecedor_id):
                QMessageBox.information(self, "Sucesso", "Fornecedor deletado com sucesso!")
                self.carregar_dados("fornecedores")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao deletar fornecedor")
    
    def filtrar_fornecedores(self):
        texto = self.busca_fornecedor.text().lower()
        for row in range(self.tabela_fornecedores.rowCount()):
            nome = self.tabela_fornecedores.item(row, 1).text().lower()
            cnpj = self.tabela_fornecedores.item(row, 2).text().lower()
            visivel = texto in nome or texto in cnpj
            self.tabela_fornecedores.setRowHidden(row, not visivel)
    
    # ==================== VENDAS ====================
    
    def nova_venda(self):
        QMessageBox.information(self, "Funcionalidade", "Módulo de novas vendas em desenvolvimento")
    
    def visualizar_venda(self):
        linha = self.tabela_vendas.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma venda para visualizar")
            return
        
        venda_id = int(self.tabela_vendas.item(linha, 0).text())
        venda = self.api.obter_venda(venda_id)
        
        if venda:
            detalhes = f"ID: {venda.get('id')}\n"
            detalhes += f"Cliente ID: {venda.get('id_cliente')}\n"
            detalhes += f"Data: {venda.get('data_venda')}\n"
            detalhes += f"Total: R$ {venda.get('total', 0):.2f}\n"
            detalhes += f"Desconto: R$ {venda.get('desconto', 0):.2f}\n"
            detalhes += "\nItens:\n"
            for item in venda.get('itens', []):
                detalhes += f"  - Medicamento {item['id_medicamento']}: {item['quantidade']} x R$ {item['preco_unitario']:.2f}\n"
            
            QMessageBox.information(self, "Detalhes da Venda", detalhes)
    
    def deletar_venda(self):
        linha = self.tabela_vendas.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma venda para deletar")
            return
        
        venda_id = int(self.tabela_vendas.item(linha, 0).text())
        resposta = QMessageBox.question(self, "Confirmar", "Deseja realmente deletar esta venda?",
                                       QMessageBox.Yes | QMessageBox.No)
        
        if resposta == QMessageBox.Yes:
            if self.api.deletar_venda(venda_id):
                QMessageBox.information(self, "Sucesso", "Venda deletada com sucesso!")
                self.carregar_dados("vendas")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao deletar venda")


def main():
    app_qt = sys.modules.get('PyQt5.QtWidgets')
    if not app_qt:
        from PyQt5.QtWidgets import QApplication
    else:
        QApplication = app_qt.QApplication
    
    aplicacao = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(aplicacao.exec_())


if __name__ == "__main__":
    main()
