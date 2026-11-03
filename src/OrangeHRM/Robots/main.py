import pandas as pd
import argparse
from pathlib import Path
from .orange_hrm import OrangeHRM
from OrangeHRM.emailsend.send import enviar


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-idt", required=True)
    args = parser.parse_args()

    sistema = OrangeHRM()

    try:
        funcionarios = pd.read_excel(sistema.arquivo)

        pasta_reports = Path(__file__).resolve().parents[3] / "reports"
        pasta_reports.mkdir(parents=True, exist_ok=True)

        print(f"Planilha carregada: {len(funcionarios)} funcionário(s).")

        sistema.login()
        sistema.cadastrar_funcionarios(funcionarios)

        funcionarios.to_excel(
            pasta_reports / f"{args.idt}.xlsx",
            index=False,
        )

        enviar(args.idt)

    finally:
        sistema.session.close()

if __name__ == "__main__":
    main()