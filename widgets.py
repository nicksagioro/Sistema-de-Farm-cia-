"""
widgets.py - Re-exporta todos os dialogs de cadastro Qt5.

Modulos:
    widgets_med -> DialogCadastroMedicamento
    widgets_cf  -> DialogCadastroCliente, DialogCadastroFornecedor
"""

from widgets_med import DialogCadastroMedicamento
from widgets_cf import DialogCadastroCliente, DialogCadastroFornecedor

__all__ = [
    "DialogCadastroMedicamento",
    "DialogCadastroCliente",
    "DialogCadastroFornecedor",
]
