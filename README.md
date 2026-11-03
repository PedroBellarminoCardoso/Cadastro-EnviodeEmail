# Projeto para implementar o cadastro de funcionários

## Objetivo

Aprender e desenvolver uma implementação em Python que automatize o cadastro de funcionários no site [OrangeHRM](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login).

O projeto tem como objetivo ler uma planilha localizada na raiz do projeto, utilizar os dados nela contidos para realizar o cadastro dos funcionários no site e, logo após, enviar um e-mail ao destinatário informado.

## Tecnologias utilizadas

- **Poetry:** gerenciamento de dependências e ambiente virtual do projeto.
- **Python:** linguagem de programação utilizada no desenvolvimento.
- **SMTP:** protocolo utilizado para o envio de e-mails.
- **python-dotenv:** gerenciamento de variáveis de ambiente.
- **Pandas:** leitura e processamento dos dados da planilha.
- **Argparse:** recebimento e tratamento de argumentos pela linha de comando.
- **HTTPX:** realização de requisições HTTP.
- **HTML:** estruturação de conteúdo HTML, quando necessário.

## Como executar o projeto

### Pré-requisitos

- Python instalado.
- Poetry instalado.
- Planilha com os dados dos funcionários localizada na raiz do projeto.

### Instalação

1. Clone o repositório e acesse a pasta do projeto.

2. Instale as dependências utilizando o Poetry:

```bash
poetry install
```

### Execução

Para executar o programa, utilize o comando abaixo, substituindo `Nome` pelo nome da planilha que deseja:

```bash
poetry run -idt "Nome"
```

O programa irá utilizar os dados da planilha para realizar o cadastro do funcionário no OrangeHRM e, após a conclusão, enviar um e-mail ao destinatário informado.
