"""
widgets.py - Re-exporta todos os dialogs de cadastro Qt5.

Modulos:
    widgets_med -> DialogCadastroMedicamento
    widgets_cf  -> DialogCadastroCliente, DialogCadastroFornecedor
"""

from ui.widgets.widgets_med import DialogCadastroMedicamento
from ui.widgets.widgets_cf import DialogCadastroCliente, DialogCadastroFornecedor

__all__ = [
    "DialogCadastroMedicamento",
    "DialogCadastroCliente",
    "DialogCadastroFornecedor",
]
