from pathlib import Path
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv


load_dotenv()


def enviar(nome_da_planilha):
    try:
        nome_completo = (
            nome_da_planilha
            if nome_da_planilha.lower().endswith(".xlsx")
            else f"{nome_da_planilha}.xlsx"
        )

        raiz_projeto = Path(__file__).resolve().parents[3]
        caminho_anexo = raiz_projeto / "reports" / nome_completo

        if not caminho_anexo.exists():
            print(f"[EmailSend] Arquivo não encontrado: {caminho_anexo}")
            return False

        remetente = os.getenv("GMAIL_USER")
        senha = os.getenv("GMAIL_PASSWORD")
        destinatario = "@gmail.com"

        if not remetente or not senha:
            print("[EmailSend] Credenciais do Gmail não encontradas.")
            return False

        email = EmailMessage()
        email["From"] = remetente
        email["To"] = destinatario
        email["Subject"] = f"Relatório da automação: {nome_da_planilha}"
        email.set_content(
            "A automação terminou de rodar.\n\n"
            "A planilha gerada segue em anexo."
        )

        with open(caminho_anexo, "rb") as arquivo:
            email.add_attachment(
                arquivo.read(),
                maintype="application",
                subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=nome_completo
            )

        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(email)

        print(f"[EmailSend] E-mail enviado de {remetente} para {destinatario}.")
        return True

    except Exception as erro:
        print(f"[EmailSend] Erro ao enviar e-mail: {erro}")
        return False
