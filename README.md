# Point - Lambda Point Save

## Introdução

Este projeto consiste em uma função Lambda na AWS que é acionada para salvar o ponto de um funcionário em um banco de dados. A função é responsável por receber um token JWT de autorização, extrair o ID do funcionário a partir dele, e então chamar o caso de uso PunchClockUseCase para salvar o registro de ponto.

## Arquitetura

A arquitetura do projeto envolve os seguintes componentes:

1. Função Lambda: Implementa a lógica para salvar o ponto do funcionário.
2. AWS Secrets Manager: Armazena as credenciais de acesso ao banco de dados.
3. Caso de Uso PunchClock: Lida com a lógica de negócios para salvar o ponto do funcionário.
4. JWT Util: Utilitário para manipular tokens JWT de autorização.
5. Logger: Registra mensagens de log para monitoramento e depuração.

## Fluxo de Trabalho

1. A função Lambda é acionada por uma solicitação HTTP.
2. A função extrai o ID do funcionário do token JWT.
3. A função chama o caso de uso PunchClockUseCase para salvar o ponto do funcionário.
4. Se houver algum erro durante o processo, a função registra uma mensagem de log.

## Configuração

Antes de implantar a função Lambda, é necessário configurar os seguintes recursos:

1. AWS Secrets Manager: Criar um segredo para armazenar as credenciais do banco de dados.
2. AWS IAM Role: Uma função IAM que permite que a função Lambda acesse os recursos necessários.

## Implantação

A implantação do projeto é realizada da seguinte maneira:

1. Os arquivos de configuração Terraform são preparados com as informações necessárias, como região da AWS e IDs de recursos.
2. Os recursos são criados e implantados na AWS usando o Terraform.
3. A função Lambda é configurada com as credenciais do banco de dados e as dependências necessárias.

## Recursos

- Terraform: Utilizado para a automação da infraestrutura na AWS.
- AWS Lambda: Serviço de computação serverless da AWS.
- AWS Secrets Manager: Serviço de gerenciamento de segredos da AWS.
- Python 3.11: Linguagem de programação utilizada para implementar a lógica da função Lambda.

## Conclusão

Este projeto oferece uma solução simples e eficaz para salvar o ponto de funcionários em um banco de dados usando uma função Lambda na AWS. Ele demonstra como integrar diferentes serviços da AWS para criar uma aplicação serverless escalável e segura.
