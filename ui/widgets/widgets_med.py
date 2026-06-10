"""
widgets_med.py - Dialog de cadastro de medicamentos.
"""

from datetime import datetime
from typing import Dict, Optional

from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox, QDateEdit, QDialog, QDoubleSpinBox,
    QFormLayout, QHBoxLayout, QLineEdit, QMessageBox,
    QPushButton, QSpinBox, QTextEdit,
)


class DialogCadastroMedicamento(QDialog):
    medicamento_salvo = pyqtSignal(dict)

    def __init__(self, parent=None, medicamento: Optional[Dict] = None,
                 fornecedores: Optional[list] = None):
        super().__init__(parent)
        self.medicamento = medicamento
        self.fornecedores = fornecedores or []
        self._build()
        if medicamento:
            self._carregar()

    def _build(self):
        self.setWindowTitle("Cadastro de Medicamento")
        self.setMinimumWidth(480)
        layout = QFormLayout(self)

        self.nome            = QLineEdit()
        self.principio_ativo = QLineEdit()
        self.preco           = QDoubleSpinBox()
        self.preco.setRange(0.01, 99999.99)
        self.preco.setDecimals(2)
        self.preco.setPrefix("R$ ")
        self.estoque = QSpinBox()
        self.estoque.setRange(0, 999999)
        self.lote          = QLineEdit()
        self.data_validade = QDateEdit(QDate.currentDate())
        self.data_validade.setCalendarPopup(True)
        self.fabricante = QLineEdit()
        self.descricao  = QTextEdit()
        self.descricao.setFixedHeight(80)
        self.fornecedor = QComboBox()
        self.fornecedor.addItem("Nenhum", None)
        for f in self.fornecedores:
            self.fornecedor.addItem(f.get("nome", ""), f.get("id"))

        layout.addRow("Nome:", self.nome)
        layout.addRow("Principio Ativo:", self.principio_ativo)
        layout.addRow("Preco:", self.preco)
        layout.addRow("Estoque:", self.estoque)
        layout.addRow("Lote:", self.lote)
        layout.addRow("Data de Validade:", self.data_validade)
        layout.addRow("Fabricante:", self.fabricante)
        layout.addRow("Fornecedor:", self.fornecedor)
        layout.addRow("Descricao:", self.descricao)

        bts = QHBoxLayout()
        ok = QPushButton("Salvar")
        ok.clicked.connect(self._salvar)
        cn = QPushButton("Cancelar")
        cn.clicked.connect(self.reject)
        bts.addWidget(ok)
        bts.addWidget(cn)
        layout.addRow(bts)

    def _carregar(self):
        m = self.medicamento
        self.nome.setText(m.get("nome", ""))
        self.principio_ativo.setText(m.get("principio_ativo", ""))
        self.preco.setValue(float(m.get("preco", 0)))
        self.estoque.setValue(int(m.get("estoque", 0)))
        self.lote.setText(m.get("lote", ""))
        val = m.get("data_validade", "")
        if val:
            try:
                d = datetime.strptime(str(val)[:10], "%Y-%m-%d").date()
                self.data_validade.setDate(QDate(d.year, d.month, d.day))
            except ValueError:
                pass
        self.fabricante.setText(m.get("fabricante", "") or "")
        self.descricao.setPlainText(m.get("descricao", "") or "")
        id_forn = m.get("id_fornecedor")
        if id_forn is not None:
            idx = self.fornecedor.findData(id_forn)
            if idx >= 0:
                self.fornecedor.setCurrentIndex(idx)

    def _salvar(self):
        nome = self.nome.text().strip()
        principio = self.principio_ativo.text().strip()
        lote = self.lote.text().strip()
        if not nome or not principio or not lote:
            QMessageBox.warning(self, "Validacao",
                                "Nome, Principio Ativo e Lote sao obrigatorios.")
            return
        dados = {
            "nome": nome, "principio_ativo": principio,
            "preco": self.preco.value(), "estoque": self.estoque.value(),
            "lote": lote,
            "data_validade": self.data_validade.date().toString("yyyy-MM-dd"),
            "fabricante": self.fabricante.text().strip() or None,
            "descricao": self.descricao.toPlainText().strip() or None,
            "id_fornecedor": self.fornecedor.currentData(),
        }
        if self.medicamento and self.medicamento.get("id"):
            dados["id"] = self.medicamento["id"]
        self.medicamento_salvo.emit(dados)
        self.accept()
