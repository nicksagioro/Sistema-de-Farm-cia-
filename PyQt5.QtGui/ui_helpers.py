"""
ui_helpers.py - Utilitarios compartilhados entre as abas Qt5.
"""

from PyQt5.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem


def preencher_tabela(tabela: QTableWidget, colunas: list, dados: list):
    tabela.setRowCount(len(dados))
    for row, item in enumerate(dados):
        for col, chave in enumerate(colunas):
            tabela.setItem(row, col,
                           QTableWidgetItem(str(item.get(chave, "") or "")))


def criar_tabela(colunas: list) -> QTableWidget:
    t = QTableWidget()
    t.setColumnCount(len(colunas))
    t.setHorizontalHeaderLabels(colunas)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return t
