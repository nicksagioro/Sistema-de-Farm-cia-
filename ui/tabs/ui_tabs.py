"""
ui_tabs.py - Re-exporta todas as abas da interface Qt5.

Modulos:
    ui_tabs_mc  -> AbaMedicamentos, AbaClientes
    ui_tabs_fv  -> AbaFornecedores, AbaVendas
"""

from ui.tabs.ui_tabs_mc import AbaClientes, AbaMedicamentos
from ui.tabs.ui_tabs_fv import AbaFornecedores, AbaVendas

__all__ = ["AbaMedicamentos", "AbaClientes", "AbaFornecedores", "AbaVendas"]
