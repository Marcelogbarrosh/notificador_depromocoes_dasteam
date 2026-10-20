# Notificador de Promoções da Steam

Programa em Python que lê a sua lista de desejos da Steam, verifica o preço de cada jogo na loja brasileira e avisa em um canal do Discord quando algum estiver em promoção.

## Como funciona

1. Busca a sua wishlist pela Web API oficial da Steam.
2. Consulta o preço e o desconto de cada jogo (loja do Brasil, em reais).
3. Seleciona os jogos cujo desconto é maior ou igual ao desconto mínimo que você definiu.
4. Envia um aviso para o Discord via webhook, com nome, preço, desconto e link da loja.
5. Guarda os jogos já avisados em `notificados.json`, para não repetir o aviso a cada execução.

### Quando você é avisado

- Quando um jogo da wishlist atinge o desconto mínimo pela primeira vez.
- Quando um jogo já avisado fica ainda mais barato do que no último aviso.
- Quando uma promoção termina e o jogo volta a entrar em promoção depois.

Se a promoção acaba, o jogo é "esquecido" e você será avisado de novo quando ela voltar.

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

Copie o `.env.example` para `.env` e preencha:

```
STEAM_API_KEY=sua_chave_aqui
STEAM_ID=seu_steamid64_aqui
DISCORD_WEBHOOK_URL=url_do_webhook_aqui
DESCONTO_MINIMO=50
```

| Variável | O que é |
|---|---|
| `STEAM_API_KEY` | Sua chave da Steam Web API |
| `STEAM_ID` | Seu SteamID64 |
| `DISCORD_WEBHOOK_URL` | URL do webhook do canal que receberá os avisos |
| `DESCONTO_MINIMO` | Desconto mínimo (em %) para avisar. Padrão: 50 |

Sem espaços em volta do `=`. **Nunca** suba o `.env` para o GitHub: ele contém segredos e já está listado no `.gitignore`.

## Como usar

```
py main.py
```

Na primeira execução, você recebe todas as promoções atuais da sua wishlist. Nas seguintes, só as novidades.

O programa consulta um jogo por vez, com pausa entre as requisições para respeitar o limite da Steam. Com uma wishlist grande, a execução pode levar alguns minutos.

### Execução automática (Windows)

Para rodar sozinho, use o **Agendador de Tarefas** do Windows, executando `main.py` uma ou duas vezes por dia. Configure a pasta do projeto no campo **"Iniciar em"**, para que o `.env` e o `notificados.json` sejam encontrados. Promoções da Steam duram dias, então não é necessário rodar com mais frequência.

## Arquivos do projeto

| Arquivo | Função |
|---|---|
| `main.py` | Programa principal |
| `.env` | Suas chaves e configurações (não vai para o GitHub) |
| `.env.example` | Modelo do `.env`, sem valores secretos |
| `notificados.json` | Gerado pelo programa: jogos já avisados (não vai para o GitHub) |
| `requirements.txt` | Dependências do projeto |

## Segurança

- A chave da Steam e a URL do webhook são segredos. Guarde-as apenas no `.env`.
- Se alguma delas vazar, gere uma nova (chave da Steam em steamcommunity.com/dev/apikey; webhook nas configurações do canal do Discord).

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).