"""
api_client.py - Cliente HTTP para comunicacao com a API FastAPI.

Uso:
    from api_client import APIClient
    api = APIClient()
    medicamentos = api.listar_medicamentos()
"""

from typing import Dict, List, Optional

import requests


class APIClient:
    """Cliente HTTP para a API de farmacia."""


    def __init__(self, base_url: str = "http://localhost:8080/api"):
        self.base_url = base_url
        self.session = requests.Session()

    def _get(self, path: str, params: dict = None) -> Optional[object]:
        response = self.session.get(f"{self.base_url}{path}", params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, dados: dict) -> Optional[Dict]:
        response = self.session.post(f"{self.base_url}{path}", json=dados)
        response.raise_for_status()
        return response.json()

    def _put(self, path: str, dados: dict) -> Optional[Dict]:
        response = self.session.put(f"{self.base_url}{path}", json=dados)
        response.raise_for_status()
        return response.json()

    def _delete(self, path: str) -> bool:
        response = self.session.delete(f"{self.base_url}{path}")
        response.raise_for_status()
        return True

    # ------------------------------------------------------------------
    # Medicamentos
    # ------------------------------------------------------------------

    def listar_medicamentos(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        return self._get("/medicamentos", {"skip": skip, "limit": limit})

    def obter_medicamento(self, med_id: int) -> Optional[Dict]:
        return self._get(f"/medicamentos/{med_id}")

    def criar_medicamento(self, dados: Dict) -> Optional[Dict]:
        return self._post("/medicamentos", dados)

    def atualizar_medicamento(self, med_id: int, dados: Dict) -> Optional[Dict]:
        return self._put(f"/medicamentos/{med_id}", dados)

    def deletar_medicamento(self, med_id: int) -> bool:
        return self._delete(f"/medicamentos/{med_id}")

    # ------------------------------------------------------------------
    # Clientes
    # ------------------------------------------------------------------

    def listar_clientes(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        return self._get("/clientes", {"skip": skip, "limit": limit})

    def obter_cliente(self, cliente_id: int) -> Optional[Dict]:
        return self._get(f"/clientes/{cliente_id}")

    def criar_cliente(self, dados: Dict) -> Optional[Dict]:
        return self._post("/clientes", dados)

    def atualizar_cliente(self, cliente_id: int, dados: Dict) -> Optional[Dict]:
        return self._put(f"/clientes/{cliente_id}", dados)

    def deletar_cliente(self, cliente_id: int) -> bool:
        return self._delete(f"/clientes/{cliente_id}")

    # ------------------------------------------------------------------
    # Fornecedores
    # ------------------------------------------------------------------

    def listar_fornecedores(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        return self._get("/fornecedores", {"skip": skip, "limit": limit})

    def obter_fornecedor(self, fornecedor_id: int) -> Optional[Dict]:
        return self._get(f"/fornecedores/{fornecedor_id}")

    def criar_fornecedor(self, dados: Dict) -> Optional[Dict]:
        return self._post("/fornecedores", dados)

    def atualizar_fornecedor(self, fornecedor_id: int, dados: Dict) -> Optional[Dict]:
        return self._put(f"/fornecedores/{fornecedor_id}", dados)

    def deletar_fornecedor(self, fornecedor_id: int) -> bool:
        return self._delete(f"/fornecedores/{fornecedor_id}")

    # ------------------------------------------------------------------
    # Vendas
    # ------------------------------------------------------------------

    def listar_vendas(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        return self._get("/vendas", {"skip": skip, "limit": limit})

    def obter_venda(self, venda_id: int) -> Optional[Dict]:
        return self._get(f"/vendas/{venda_id}")

    def criar_venda(self, dados: Dict) -> Optional[Dict]:
        return self._post("/vendas", dados)

    def atualizar_venda(self, venda_id: int, dados: Dict) -> Optional[Dict]:
        return self._put(f"/vendas/{venda_id}", dados)

    def deletar_venda(self, venda_id: int) -> bool:
        return self._delete(f"/vendas/{venda_id}")
