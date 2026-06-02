from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QDateEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QTableWidget, QTableWidgetItem, QWidget, QHeaderView,
    QFormLayout, QTextEdit
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from typing import Dict, Optional
from datetime import date, datetime

class DialogCadastroMedicamento(QDialog):
    """Dialog para cadastro/edição de medicamentos"""
    medicamento_salvo = pyqtSignal(dict)
    
    def __init__(self, parent=None, medicamento: Dict = None, fornecedores: list = None):
        super().__init__(parent)
        self.medicamento = medicamento
        self.fornecedores = fornecedores or []
        self.init_ui()
        if medicamento:
            self.carregar_dados()
    
    def init_ui(self):
        self.setWindowTitle("Cadastro de Medicamento")
        self.setGeometry(100, 100, 500, 400)
        
        layout = QFormLayout()
        
        self.nome = QLineEdit()
        self.principio_ativo = QLineEdit()
        self.preco = QDoubleSpinBox()
        self.preco.setMinimum(0.01)
        self.preco.setDecimals(2)
        self.estoque = QSpinBox()
        self.estoque.setMinimum(0)
        self.lote = QLineEdit()
        self.data_validade = QDateEdit()
        self.data_validade.setDate(QDate.currentDate())
        self.fabricante = QLineEdit()
        self.descricao = QTextEdit()
        
        self.fornecedor = QComboBox()
        self.fornecedor.addItem("Selecione um fornecedor", None)
        for forn in self.fornecedores:
            self.fornecedor.addItem(forn.get("nome", ""), forn.get("id"))
        
        layout.addRow("Nome:", self.nome)
        layout.addRow("Princípio Ativo:", self.principio_ativo)
        layout.addRow("Preço:", self.preco)
        layout.addRow("Estoque:", self.estoque)
        layout.addRow("Lote:", self.lote)
        layout.addRow("Data Validade:", self.data_validade)
        layout.addRow("Fabricante:", self.fabricante)
        layout.addRow("Fornecedor:", self.fornecedor)
        layout.addRow("Descrição:", self.descricao)
        
        botoes_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_cancelar = QPushButton("Cancelar")
        
        btn_salvar.clicked.connect(self.salvar)
        btn_cancelar.clicked.connect(self.reject)
        
        botoes_layout.addWidget(btn_salvar)
        botoes_layout.addWidget(btn_cancelar)
        layout.addRow(botoes_layout)
        
        self.setLayout(layout)
    
    def carregar_dados(self):
        if self.medicamento:
            self.nome.setText(self.medicamento.get("nome", ""))
            self.principio_ativo.setText(self.medicamento.get("principio_ativo", ""))
            self.preco.setValue(float(self.medicamento.get("preco", 0)))
            self.estoque.setValue(self.medicamento.get("estoque", 0))
            self.lote.setText(self.medicamento.get("lote", ""))
            
            data_val = datetime.strptime(self.medicamento.get("data_validade", ""), "%Y-%m-%d").date()
            self.data_validade.setDate(QDate(data_val.year, data_val.month, data_val.day))
            
            self.fabricante.setText(self.medicamento.get("fabricante", ""))
            self.descricao.setPlainText(self.medicamento.get("descricao", ""))
    
    def salvar(self):
        if not self.nome.text() or not self.principio_ativo.text():
            QMessageBox.warning(self, "Erro", "Nome e Princípio Ativo são obrigatórios")
            return
        
        dados = {
            "nome": self.nome.text(),
            "principio_ativo": self.principio_ativo.text(),
            "preco": self.preco.value(),
            "estoque": self.estoque.value(),
            "lote": self.lote.text(),
            "data_validade": self.data_validade.date().toString("yyyy-MM-dd"),
            "fabricante": self.fabricante.text() or None,
            "descricao": self.descricao.toPlainText() or None,
            "id_fornecedor": self.fornecedor.currentData()
        }
        
        self.medicamento_salvo.emit(dados)
        self.accept()


class DialogCadastroCliente(QDialog):
    """Dialog para cadastro/edição de clientes"""
    cliente_salvo = pyqtSignal(dict)
    
    def __init__(self, parent=None, cliente: Dict = None):
        super().__init__(parent)
        self.cliente = cliente
        self.init_ui()
        if cliente:
            self.carregar_dados()
    
    def init_ui(self):
        self.setWindowTitle("Cadastro de Cliente")
        self.setGeometry(100, 100, 500, 350)
        
        layout = QFormLayout()
        
        self.cpf = QLineEdit()
        self.cpf.setMaxLength(11)
        self.nome = QLineEdit()
        self.email = QLineEdit()
        self.telefone = QLineEdit()
        self.endereco = QTextEdit()
        
        layout.addRow("CPF:", self.cpf)
        layout.addRow("Nome:", self.nome)
        layout.addRow("Email:", self.email)
        layout.addRow("Telefone:", self.telefone)
        layout.addRow("Endereço:", self.endereco)
        
        botoes_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_cancelar = QPushButton("Cancelar")
        
        btn_salvar.clicked.connect(self.salvar)
        btn_cancelar.clicked.connect(self.reject)
        
        botoes_layout.addWidget(btn_salvar)
        botoes_layout.addWidget(btn_cancelar)
        layout.addRow(botoes_layout)
        
        self.setLayout(layout)
    
    def carregar_dados(self):
        if self.cliente:
            self.cpf.setText(self.cliente.get("cpf", ""))
            self.cpf.setReadOnly(True)  # CPF não pode ser alterado
            self.nome.setText(self.cliente.get("nome", ""))
            self.email.setText(self.cliente.get("email", ""))
            self.telefone.setText(self.cliente.get("telefone", ""))
            self.endereco.setPlainText(self.cliente.get("endereco", ""))
    
    def salvar(self):
        cpf = self.cpf.text().strip()
        nome = self.nome.text().strip()
        
        if not cpf or not nome:
            QMessageBox.warning(self, "Erro", "CPF e Nome são obrigatórios")
            return
        
        if len(cpf) != 11 or not cpf.isdigit():
            QMessageBox.warning(self, "Erro", "CPF deve conter 11 dígitos")
            return
        
        dados = {
            "cpf": cpf,
            "nome": nome,
            "email": self.email.text() or None,
            "telefone": self.telefone.text() or None,
            "endereco": self.endereco.toPlainText() or None
        }
        
        self.cliente_salvo.emit(dados)
        self.accept()


class DialogCadastroFornecedor(QDialog):
    """Dialog para cadastro/edição de fornecedores"""
    fornecedor_salvo = pyqtSignal(dict)
    
    def __init__(self, parent=None, fornecedor: Dict = None):
        super().__init__(parent)
        self.fornecedor = fornecedor
        self.init_ui()
        if fornecedor:
            self.carregar_dados()
    
    def init_ui(self):
        self.setWindowTitle("Cadastro de Fornecedor")
        self.setGeometry(100, 100, 500, 350)
        
        layout = QFormLayout()
        
        self.nome = QLineEdit()
        self.cnpj = QLineEdit()
        self.cnpj.setMaxLength(14)
        self.telefone = QLineEdit()
        self.email = QLineEdit()
        self.endereco = QTextEdit()
        
        layout.addRow("Nome:", self.nome)
        layout.addRow("CNPJ:", self.cnpj)
        layout.addRow("Telefone:", self.telefone)
        layout.addRow("Email:", self.email)
        layout.addRow("Endereço:", self.endereco)
        
        botoes_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_cancelar = QPushButton("Cancelar")
        
        btn_salvar.clicked.connect(self.salvar)
        btn_cancelar.clicked.connect(self.reject)
        
        botoes_layout.addWidget(btn_salvar)
        botoes_layout.addWidget(btn_cancelar)
        layout.addRow(botoes_layout)
        
        self.setLayout(layout)
    
    def carregar_dados(self):
        if self.fornecedor:
            self.nome.setText(self.fornecedor.get("nome", ""))
            self.cnpj.setText(self.fornecedor.get("cnpj", ""))
            self.cnpj.setReadOnly(True)
            self.telefone.setText(self.fornecedor.get("telefone", ""))
            self.email.setText(self.fornecedor.get("email", ""))
            self.endereco.setPlainText(self.fornecedor.get("endereco", ""))
    
    def salvar(self):
        nome = self.nome.text().strip()
        cnpj = self.cnpj.text().strip()
        
        if not nome or not cnpj:
            QMessageBox.warning(self, "Erro", "Nome e CNPJ são obrigatórios")
            return
        
        if len(cnpj) != 14 or not cnpj.isdigit():
            QMessageBox.warning(self, "Erro", "CNPJ deve conter 14 dígitos")
            return
        
        dados = {
            "nome": nome,
            "cnpj": cnpj,
            "telefone": self.telefone.text() or None,
            "email": self.email.text() or None,
            "endereco": self.endereco.toPlainText() or None
        }
        
        self.fornecedor_salvo.emit(dados)
        self.accept()


def preencher_tabela(tabela: QTableWidget, colunas: list, dados: list):
    """Preenche uma tabela com dados"""
    tabela.setColumnCount(len(colunas))
    tabela.setHorizontalHeaderLabels(colunas)
    tabela.setRowCount(len(dados))
    
    for row, item in enumerate(dados):
        for col, coluna in enumerate(colunas):
            valor = item.get(coluna, "")
            tabela.setItem(row, col, QTableWidgetItem(str(valor)))
    
    tabela.resizeColumnsToContents()
    header = tabela.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.Stretch)
