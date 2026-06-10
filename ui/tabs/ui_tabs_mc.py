"""
ui_tabs_mc.py - Abas de Medicamentos e Clientes.
"""

from PyQt5.QtWidgets import (
    QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout, QWidget,
)

from api.api_client import APIClient
from ui.helpers.ui_helpers import criar_tabela, preencher_tabela
from ui.widgets.widgets import DialogCadastroCliente, DialogCadastroMedicamento


class AbaMedicamentos(QWidget):
    def __init__(self, api: APIClient, cache: dict):
        super().__init__()
        self.api, self.cache = api, cache
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        barra = QHBoxLayout()
        self.busca = QLineEdit()
        self.busca.setPlaceholderText("Buscar por nome...")
        self.busca.textChanged.connect(self._filtrar)
        barra.addWidget(QLabel("Buscar:"))
        barra.addWidget(self.busca)
        for texto, slot in [("Novo", self._novo), ("Editar", self._editar),
                             ("Deletar", self._deletar), ("Atualizar", self.carregar)]:
            b = QPushButton(texto)
            b.clicked.connect(slot)
            barra.addWidget(b)
        self.tabela = criar_tabela(["ID", "Nome", "Principio Ativo", "Preco",
                                    "Estoque", "Lote", "Validade", "Fabricante"])
        layout.addLayout(barra)
        layout.addWidget(self.tabela)

    def carregar(self):
        self.cache["medicamentos"] = self.api.listar_medicamentos()
        preencher_tabela(self.tabela,
                         ["id", "nome", "principio_ativo", "preco",
                          "estoque", "lote", "data_validade", "fabricante"],
                         self.cache["medicamentos"])

    def _novo(self):
        d = DialogCadastroMedicamento(self, fornecedores=self.cache.get("fornecedores", []))
        d.medicamento_salvo.connect(self._salvar)
        d.exec_()

    def _editar(self):
        row = self.tabela.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Aviso", "Selecione um medicamento.")
        med = self.api.obter_medicamento(int(self.tabela.item(row, 0).text()))
        if med:
            med["id"] = int(self.tabela.item(row, 0).text())
            d = DialogCadastroMedicamento(self, medicamento=med,
                                          fornecedores=self.cache.get("fornecedores", []))
            d.medicamento_salvo.connect(self._salvar)
            d.exec_()

    def _deletar(self):
        row = self.tabela.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Aviso", "Selecione um medicamento.")
        med_id = int(self.tabela.item(row, 0).text())
        if QMessageBox.question(self, "Confirmar", "Deletar medicamento?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            if self.api.deletar_medicamento(med_id):
                self.carregar()

    def _salvar(self, dados: dict):
        med_id = dados.pop("id", None)
        try:
            if med_id:
                self.api.atualizar_medicamento(med_id, dados)
            else:
                self.api.criar_medicamento(dados)
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def _filtrar(self):
        texto = self.busca.text().lower()
        for row in range(self.tabela.rowCount()):
            item = self.tabela.item(row, 1)
            self.tabela.setRowHidden(row, texto not in (item.text().lower() if item else ""))


class AbaClientes(QWidget):
    def __init__(self, api: APIClient, cache: dict):
        super().__init__()
        self.api, self.cache = api, cache
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        barra = QHBoxLayout()
        self.busca = QLineEdit()
        self.busca.setPlaceholderText("Buscar por nome ou CPF...")
        self.busca.textChanged.connect(self._filtrar)
        barra.addWidget(QLabel("Buscar:"))
        barra.addWidget(self.busca)
        for texto, slot in [("Novo", self._novo), ("Editar", self._editar),
                             ("Deletar", self._deletar), ("Atualizar", self.carregar)]:
            b = QPushButton(texto)
            b.clicked.connect(slot)
            barra.addWidget(b)
        self.tabela = criar_tabela(["ID", "CPF", "Nome", "Email", "Telefone", "Ativo"])
        layout.addLayout(barra)
        layout.addWidget(self.tabela)

    def carregar(self):
        self.cache["clientes"] = self.api.listar_clientes()
        preencher_tabela(self.tabela,
                         ["id", "cpf", "nome", "email", "telefone", "ativo"],
                         self.cache["clientes"])

    def _novo(self):
        d = DialogCadastroCliente(self)
        d.cliente_salvo.connect(lambda dados: self._op(None, dados))
        d.exec_()

    def _editar(self):
        row = self.tabela.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Aviso", "Selecione um cliente.")
        cid = int(self.tabela.item(row, 0).text())
        c = self.api.obter_cliente(cid)
        if c:
            c["id"] = cid
            d = DialogCadastroCliente(self, cliente=c)
            d.cliente_salvo.connect(lambda dados: self._op(cid, dados))
            d.exec_()

    def _deletar(self):
        row = self.tabela.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Aviso", "Selecione um cliente.")
        cid = int(self.tabela.item(row, 0).text())
        if QMessageBox.question(self, "Confirmar", "Deletar cliente?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            if self.api.deletar_cliente(cid):
                self.carregar()

    def _op(self, cid, dados):
        try:
            if cid:
                self.api.atualizar_cliente(cid, dados)
            else:
                self.api.criar_cliente(dados)
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def _filtrar(self):
        texto = self.busca.text().lower()
        for row in range(self.tabela.rowCount()):
            nome = (self.tabela.item(row, 2).text().lower() if self.tabela.item(row, 2) else "")
            cpf  = (self.tabela.item(row, 1).text().lower() if self.tabela.item(row, 1) else "")
            self.tabela.setRowHidden(row, texto not in nome and texto not in cpf)
