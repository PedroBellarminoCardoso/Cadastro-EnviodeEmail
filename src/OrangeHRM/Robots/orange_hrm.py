import html
import re
import random
from pathlib import Path
import httpx
import pandas as pd


class OrangeHRM:
    BASE_URL = "https://opensource-demo.orangehrmlive.com
    
    def __init__(self):
        self.session = httpx.Client(
            base_url=self.BASE_URL,
            timeout=30,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        self.arquivo = (
            Path(__file__).resolve().parents[3]
            / "data"
            / "Funcionarios.xlsx"
        )

    def login(self):
        resposta = self.session.get("/web/index.php/auth/login")
        resposta.raise_for_status()

        token_match = re.search(r':token="([^"]+)"', resposta.text)

        if not token_match:
            raise RuntimeError("Token de login não encontrado.")

        token = html.unescape(token_match.group(1)).strip('"')

        resposta = self.session.post(
            "/web/index.php/auth/validate",
            data={
                "_token": token,
                "username": self.USERNAME,
                "password": self.PASSWORD,
            },
            follow_redirects=False,
        )

        destino = resposta.headers.get("location", "")

        if resposta.status_code not in (301, 302, 303, 307, 308):
            raise RuntimeError(
                f"Falha no login. HTTP {resposta.status_code}"
            )

        if "/dashboard/" not in destino:
            raise RuntimeError(
                f"Login não confirmado. Destino: {destino}"
            )

        print("Login realizado com sucesso!")

    @staticmethod
    def _texto(valor):
        if pd.isna(valor):
            return ""

        return str(valor).strip()

    def cadastrar_funcionarios(self, funcionarios):
        colunas = {"Nome", "Nome do meio", "Sobrenome"}
        faltantes = colunas - set(funcionarios.columns)

        if faltantes:
            raise ValueError(
                f"Colunas ausentes na planilha: "
                f"{', '.join(sorted(faltantes))}"
            )

        total = 0

        for indice, funcionario in funcionarios.iterrows():
            nome = self._texto(funcionario["Nome"])
            nome_meio = self._texto(funcionario["Nome do meio"])
            sobrenome = self._texto(funcionario["Sobrenome"])

            if not nome or not sobrenome:
                print(
                    f"Linha {indice + 2} ignorada: "
                    "nome ou sobrenome vazio."
                )
                continue

            employee_id = str(random.randint(1, 9999))

            dados = {
                "firstName": nome,
                "middleName": nome_meio,
                "lastName": sobrenome,
                "employeeId": employee_id,
                "empPicture": None,
            }

            resposta = self.session.post(
                "/web/index.php/api/v2/pim/employees",
                json=dados,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": (
                        f"{self.BASE_URL}/web/index.php/pim/addEmployee"
                    ),
                },
            )

            if resposta.status_code not in (200, 201):
                raise RuntimeError(
                    f"Falha ao cadastrar {nome} {sobrenome}. "
                    f"HTTP {resposta.status_code}: "
                    f"{resposta.text[:500]}"
                )

            try:
                resultado = resposta.json()
            except ValueError as erro:
                raise RuntimeError(
                    f"Resposta inesperada ao cadastrar "
                    f"{nome} {sobrenome}."
                ) from erro

            funcionario_criado = resultado.get("data", {})
            numero = funcionario_criado.get("empNumber", "não informado")
            id_salvo = funcionario_criado.get("employeeId", employee_id)

            print(
                f"Funcionário cadastrado: "
                f"{nome} {nome_meio} {sobrenome} "
                f"| Employee ID: {id_salvo} "
            )

            total += 1

        print(
            f"\nProcesso concluído: "
            f"{total} funcionário(s) cadastrado(s)."
        )
