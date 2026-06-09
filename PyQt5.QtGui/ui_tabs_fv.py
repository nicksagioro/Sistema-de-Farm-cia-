"""
ui_tabs_fv.py - Abas de Fornecedores e Vendas.
"""

from PyQt5.QtWidgets import (
    QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout, QWidget,
)

from api_client import APIClient
from ui_helpers import criar_tabela, preencher_tabela
from widgets import DialogCadastroFornecedor


class AbaFornecedores(QWidget):
    def __init__(self, api: APIClient, cache: dict):
        super().__init__()
        self.api, self.cache = api, cache
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        barra = QHBoxLayout()
        self.busca = QLineEdit()
        self.busca.setPlaceholderText("Buscar por nome ou CNPJ...")
        self.busca.textChanged.connect(self._filtrar)
        barra.addWidget(QLabel("Buscar:"))
        barra.addWidget(self.busca)
        for texto, slot in [("Novo", self._novo), ("Editar", self._editar),
                             ("Deletar", self._deletar), ("Atualizar", self.carregar)]:
            b = QPushButton(texto)
            b.clicked.connect(slot)
            barra.addWidget(b)
        self.tabela = criar_tabela(["ID", "Nome", "CNPJ", "Email", "Telefone", "Ativo"])
        layout.addLayout(barra)
        layout.addWidget(self.tabela)

    def carregar(self):
        self.cache["fornecedores"] = self.api.listar_fornecedores()
        preencher_tabela(self.tabela,
                         ["id", "nome", "cnpj", "email", "telefone", "ativo"],
                         self.cache["fornecedores"])

    def _novo(self):
        d = DialogCadastroFornecedor(self)
        d.fornecedor_salvo.connect(lambda dados: self._op(None, dados))
        d.exec_()

    def _editar(self):
        row = self.tabela.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Aviso", "Selecione um fornecedor.")
        fid = int(self.tabela.item(row, 0).text())
        f = self.api.obter_fornecedor(fid)
        if f:
            f["id"] = fid
            d = DialogCadastroFornecedor(self, fornecedor=f)
            d.fornecedor_salvo.connect(lambda dados: self._op(fid, dados))
            d.exec_()

    def _deletar(self):
        row = self.tabela.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Aviso", "Selecione um fornecedor.")
        fid = int(self.tabela.item(row, 0).text())
        if QMessageBox.question(self, "Confirmar", "Deletar fornecedor?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            if self.api.deletar_fornecedor(fid):
                self.carregar()

    def _op(self, fid, dados):
        try:
            if fid:
                self.api.atualizar_fornecedor(fid, dados)
            else:
                self.api.criar_fornecedor(dados)
            self.carregar()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def _filtrar(self):
        texto = self.busca.text().lower()
        for row in range(self.tabela.rowCount()):
            nome = (self.tabela.item(row, 1).text().lower() if self.tabela.item(row, 1) else "")
            cnpj = (self.tabela.item(row, 2).text().lower() if self.tabela.item(row, 2) else "")
            self.tabela.setRowHidden(row, texto not in nome and texto not in cnpj)


class AbaVendas(QWidget):
    def __init__(self, api: APIClient, cache: dict):
        super().__init__()
        self.api, self.cache = api, cache
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        barra = QHBoxLayout()
        for texto, slot in [("Visualizar", self._visualizar),
                             ("Deletar", self._deletar),
                             ("Atualizar", self.carregar)]:
            b = QPushButton(texto)
            b.clicked.connect(slot)
            barra.addWidget(b)
        barra.addStretch()
        self.tabela = criar_tabela(["ID", "Cliente ID", "Data", "Total", "Desconto"])
        layout.addLayout(barra)
        layout.addWidget(self.tabela)

    def carregar(self):
        self.cache["vendas"] = self.api.listar_vendas()
        preencher_tabela(self.tabela,
                         ["id", "id_cliente", "data_venda", "total", "desconto"],
                         self.cache["vendas"])

    def _visualizar(self):
        row = self.tabela.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Aviso", "Selecione uma venda.")
        v = self.api.obter_venda(int(self.tabela.item(row, 0).text()))
        if v:
            linhas = [f"ID: {v['id']}", f"Cliente: {v['id_cliente']}",
                      f"Data: {v['data_venda']}",
                      f"Total: R$ {float(v['total']):.2f}",
                      f"Desconto: R$ {float(v['desconto']):.2f}", "", "Itens:"]
            for i in v.get("itens", []):
                linhas.append(f"  Med {i['id_medicamento']}: "
                              f"{i['quantidade']} x R$ {float(i['preco_unitario']):.2f}")
            QMessageBox.information(self, "Detalhes da Venda", "\n".join(linhas))

    def _deletar(self):
        row = self.tabela.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Aviso", "Selecione uma venda.")
        vid = int(self.tabela.item(row, 0).text())
        if QMessageBox.question(self, "Confirmar", "Deletar venda?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            if self.api.deletar_venda(vid):
                self.carregar()
