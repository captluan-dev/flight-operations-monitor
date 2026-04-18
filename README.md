# Flight Operations Monitor

Sistema de coleta e visualização de voos em tempo real para monitorar operações aéreas. O projeto faz busca de voos usando a API `aviationstack`, grava resultados em banco de dados MySQL e expõe um endpoint REST simples em FastAPI.

## Objetivo

O objetivo deste projeto é:
- coletar informações de voo de companhias aéreas e rotas específicas;
- registrar dados em um banco MySQL;
- disponibilizar uma API para listar os voos armazenados.

## Estrutura do Projeto

- `api/main.py` - aplicação FastAPI que lista voos da base de dados.
- `collector/collector.py` - coletor que busca voos pela API e grava no banco de dados.
- `collector/flight_api.py` - cliente de integração com `aviationstack`.
- `collector/run_auto.py` - script para execução automática do coletor.
- `database/schema.sql` - esquema SQL para criação da base de dados e tabela `voos`.
- `scripts/run_collector.sh` - script shell para rodar a coleta automática com ambiente carregado.
- `requirements.txt` - dependências Python do projeto.

## Pré-requisitos

- Python 3.11+ (ou compatível)
- MySQL / MariaDB
- `pip`
- Conta e chave de acesso (`API_KEY`) da API `aviationstack`
- Plataforma: desenvolvido e testado no ambiente Linux

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/captluan-dev/flight-operations-monitor.git
cd flight-operations-monitor
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

1. Crie a base de dados MySQL chamada `flights`.
2. Execute o arquivo SQL para criar a tabela `voos`:

```bash
mysql -u root -p < database/schema.sql
```

3. Crie um arquivo `.env` na raiz do projeto com a chave da API e as configurações do MySQL:

```env
API_KEY=seu_token_aviationstack_aqui
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=flights
```

> Agora `collector/collector.py` e `api/main.py` carregam as credenciais MySQL via variáveis de ambiente.
> Os valores padrão são:
> - `DB_HOST=localhost`
> - `DB_USER=root`
> - `DB_PASSWORD=root`
> - `DB_NAME=flights`

## Como rodar

### 1. Iniciar a API

A API fornece o endpoint `/voos` para listar os registros gravados.

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse em:

```text
http://127.0.0.1:8000/voos
```

### 2. Coletor manual

Rode o coletor manualmente para pesquisar por companhia ou rota específica:

```bash
python collector/collector.py
```

O fluxo atual apresenta um menu com duas opções:
- `1` - Buscar por companhia
- `2` - Buscar por rota específica

### 3. Coleta automática

Execute o script automático para rodar a coleta com pipeline predefinida:

```bash
python collector/run_auto.py
```

Ou use o script shell:

```bash
bash scripts/run_collector.sh
```

## Uso com Docker

O projeto inclui um `Dockerfile` em `collector/Dockerfile` para rodar o coletor em um container. Ele instala as dependências do `requirements.txt` e executa `collector.py`.

### 1. Construir a imagem do coletor

```bash
docker build -t flight-collector ./collector
```

### 2. Executar o MySQL em container

Por exemplo, em Linux:

```bash
docker run --name flight-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=flights -p 3306:3306 -d mysql:8
```

### 3. Rodar o coletor Dockerizado

Como o código atual usa `localhost` para a conexão MySQL, no Linux é mais simples usar `--network host`:

```bash
docker run --rm --network host --env-file .env -v "$PWD":/app -w /app/collector flight-collector
```

Se você criar uma rede Docker personalizada ou usar `docker-compose`, ajuste o host MySQL no código (`collector/collector.py` e `api/main.py`) para o nome do serviço, por exemplo `mysql`.

## Banco de Dados

Tabela principal:

- `voos`
  - `id` INT AUTO_INCREMENT
  - `numero_voo` VARCHAR(10)
  - `origem` VARCHAR(30)
  - `destino` VARCHAR(30)
  - `status` VARCHAR(20)
  - `horario_coleta` DATETIME

## Tecnologias e Conceitos Utilizados

- FastAPI para o serviço REST
- Python para coletor e API
- MySQL para persistência de dados
- `aviationstack` como fonte de dados de voo
- Variáveis de ambiente para configuração segura
- Docker para ambiente isolado de execução do coletor
- Scripts Shell para automatizar a execução
- Arquitetura simples de coleta e exposição de dados via API

## Endpoint Disponível

- `GET /voos`

Retorna todos os registros de voos salvos na tabela `voos`.

## Notas importantes

- A coleta atual insere apenas os primeiros 50 voos retornados pela API.
- O status do voo é armazenado em minúsculas quando disponível.
- Caso nenhum número de voo seja encontrado no resultado, o registro é ignorado.

## Próximos passos sugeridos

- tornar a configuração do banco e da API totalmente baseada em `.env`;
- melhorar o tratamento de erros na coleta e na API;
- adicionar endpoints adicionais ou filtros de pesquisa na API;
- permitir atualização periódica via cron ou scheduler.

---

Autor: Luan Welton
