"""
widgets_cf.py - Dialogs de cadastro de clientes e fornecedores.
"""

from typing import Dict, Optional

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QLineEdit,
    QMessageBox, QPushButton, QTextEdit,
)


class DialogCadastroCliente(QDialog):
    cliente_salvo = pyqtSignal(dict)

    def __init__(self, parent=None, cliente: Optional[Dict] = None):
        super().__init__(parent)
        self.cliente = cliente
        self._build()
        if cliente:
            self._carregar()

    def _build(self):
        self.setWindowTitle("Cadastro de Cliente")
        self.setMinimumWidth(440)
        layout = QFormLayout(self)

        self.cpf = QLineEdit()
        self.cpf.setMaxLength(11)
        self.cpf.setPlaceholderText("11 digitos numericos")
        self.nome     = QLineEdit()
        self.email    = QLineEdit()
        self.telefone = QLineEdit()
        self.endereco = QTextEdit()
        self.endereco.setFixedHeight(60)

        layout.addRow("CPF:", self.cpf)
        layout.addRow("Nome:", self.nome)
        layout.addRow("Email:", self.email)
        layout.addRow("Telefone:", self.telefone)
        layout.addRow("Endereco:", self.endereco)

        bts = QHBoxLayout()
        ok = QPushButton("Salvar")
        ok.clicked.connect(self._salvar)
        cn = QPushButton("Cancelar")
        cn.clicked.connect(self.reject)
        bts.addWidget(ok)
        bts.addWidget(cn)
        layout.addRow(bts)

    def _carregar(self):
        c = self.cliente
        self.cpf.setText(c.get("cpf", ""))
        self.cpf.setReadOnly(True)
        self.nome.setText(c.get("nome", ""))
        self.email.setText(c.get("email", "") or "")
        self.telefone.setText(c.get("telefone", "") or "")
        self.endereco.setPlainText(c.get("endereco", "") or "")

    def _salvar(self):
        cpf  = self.cpf.text().strip()
        nome = self.nome.text().strip()
        if not cpf or not nome:
            QMessageBox.warning(self, "Validacao", "CPF e Nome sao obrigatorios.")
            return
        if len(cpf) != 11 or not cpf.isdigit():
            QMessageBox.warning(self, "Validacao",
                                "CPF deve conter exatamente 11 digitos numericos.")
            return
        self.cliente_salvo.emit({
            "cpf": cpf, "nome": nome,
            "email":    self.email.text().strip() or None,
            "telefone": self.telefone.text().strip() or None,
            "endereco": self.endereco.toPlainText().strip() or None,
        })
        self.accept()


class DialogCadastroFornecedor(QDialog):
    fornecedor_salvo = pyqtSignal(dict)

    def __init__(self, parent=None, fornecedor: Optional[Dict] = None):
        super().__init__(parent)
        self.fornecedor = fornecedor
        self._build()
        if fornecedor:
            self._carregar()

    def _build(self):
        self.setWindowTitle("Cadastro de Fornecedor")
        self.setMinimumWidth(440)
        layout = QFormLayout(self)

        self.nome = QLineEdit()
        self.cnpj = QLineEdit()
        self.cnpj.setMaxLength(14)
        self.cnpj.setPlaceholderText("14 digitos numericos")
        self.telefone = QLineEdit()
        self.email    = QLineEdit()
        self.endereco = QTextEdit()
        self.endereco.setFixedHeight(60)

        layout.addRow("Nome:", self.nome)
        layout.addRow("CNPJ:", self.cnpj)
        layout.addRow("Telefone:", self.telefone)
        layout.addRow("Email:", self.email)
        layout.addRow("Endereco:", self.endereco)

        bts = QHBoxLayout()
        ok = QPushButton("Salvar")
        ok.clicked.connect(self._salvar)
        cn = QPushButton("Cancelar")
        cn.clicked.connect(self.reject)
        bts.addWidget(ok)
        bts.addWidget(cn)
        layout.addRow(bts)

    def _carregar(self):
        f = self.fornecedor
        self.nome.setText(f.get("nome", ""))
        self.cnpj.setText(f.get("cnpj", ""))
        self.cnpj.setReadOnly(True)
        self.telefone.setText(f.get("telefone", "") or "")
        self.email.setText(f.get("email", "") or "")
        self.endereco.setPlainText(f.get("endereco", "") or "")

    def _salvar(self):
        nome = self.nome.text().strip()
        cnpj = self.cnpj.text().strip()
        if not nome:
            QMessageBox.warning(self, "Validacao", "Nome e obrigatorio.")
            return
        if len(cnpj) != 14 or not cnpj.isdigit():
            QMessageBox.warning(self, "Validacao",
                                "CNPJ deve conter exatamente 14 digitos numericos.")
            return
        self.fornecedor_salvo.emit({
            "nome": nome, "cnpj": cnpj,
            "telefone": self.telefone.text().strip() or None,
            "email":    self.email.text().strip() or None,
            "endereco": self.endereco.toPlainText().strip() or None,
        })
        self.accept()
