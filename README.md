# Notificador de Promoções da Steam

Programa em Python que lê a sua lista de desejos da Steam, verifica o preço atual de cada jogo na loja brasileira e avisa no Discord quando algum estiver em promoção.

> **Status:** em desenvolvimento. Hoje o programa já lê a wishlist e extrai os appids. A consulta de preços e o envio de avisos para o Discord estão sendo implementados.

## Como funciona

1. Busca a sua wishlist pela Web API oficial da Steam.
2. Consulta o preço e o desconto de cada jogo (loja do Brasil, em reais).
3. Se o jogo estiver em promoção, envia um aviso para um canal do Discord via webhook.

## Requisitos

- Python 3.10 ou mais recente
- Uma conta na Steam com o **perfil** e a **lista de desejos públicos**
- Uma chave de API da Steam
- Um webhook do Discord

## Instalação

1. Baixe o projeto (`git clone` ou *Code → Download ZIP* aqui no GitHub).
2. Instale as dependências:

```
py -m pip install -r requirements.txt
```

No Linux/Mac, use `python3 -m pip install -r requirements.txt`.

## Configuração

### 1. SteamID64

É o número de 17 dígitos da sua conta (começa com `7656119`). Se o seu perfil tem URL personalizada, cole-a em [steamid.io](https://steamid.io) para descobrir o número.

### 2. Privacidade

Na Steam, em *Perfil → Editar perfil → Configurações de privacidade*, deixe o perfil e a lista de desejos como **Públicos**.

### 3. Chave de API da Steam

Gere em <https://steamcommunity.com/dev/apikey>. No campo de domínio, pode usar `localhost`. A conta precisa ter pelo menos uma compra feita para liberar a chave.

### 4. Webhook do Discord

1. Tenha um servidor no Discord (pode ser um só seu, vazio).
2. Em um canal de texto: **Editar canal → Integrações → Webhooks → Novo webhook**.
3. Clique em **Copiar URL do webhook**.

### 5. Arquivo `.env`

Crie um arquivo chamado `.env` na pasta do projeto (use o `.env.example` como modelo):

```
STEAM_API_KEY=sua_chave_aqui
STEAM_ID=seu_steamid64_aqui
DISCORD_WEBHOOK_URL=url_do_webhook_aqui
```

Sem espaços em volta do `=`. **Nunca** suba o `.env` para o GitHub: ele contém segredos e já está listado no `.gitignore`.

## Como usar

```
py main.py
```

## Segurança

- A chave da Steam e a URL do webhook são segredos. Guarde-as apenas no `.env`.
- Se alguma delas vazar, gere uma nova (chave da Steam em steamcommunity.com/dev/apikey, webhook nas configurações do canal do Discord).

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).
