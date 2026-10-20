import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")
DESCONTO_MINIMO = int(os.getenv("DESCONTO_MINIMO", "50"))
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
urlwish = "https://api.steampowered.com/IWishlistService/GetWishlist/v1/"
urlpreco = "https://store.steampowered.com/api/appdetails"

#parâmetros usados
params_user = {"key" : STEAM_API_KEY, "steamid" : STEAM_ID,}

try:
    resposta_user = requests.get(urlwish, params=params_user, timeout=10)
    resposta_user.raise_for_status() 
    dados = resposta_user.json() #recebe convertendo pra dicionario
except requests.RequestException:
    print(f"Falha ao consultar wishlist.")
    
    raise SystemExit(1)

lista_appid = []
promocoes = []
tamanho = len(dados['response']['items'])

for i in range(tamanho):
    appid_atual = dados['response']['items'][i]['appid']
    lista_appid.append(appid_atual)

for appid_atual in lista_appid:

    time.sleep(1.5) #pra não estourar o rate limite
    params_jogo = {"appids": appid_atual, "cc": "br"}
    try:
        resposta_jogo = requests.get(urlpreco, params= params_jogo, timeout=10)   
        resposta_jogo.raise_for_status()
        dados_preco = resposta_jogo.json()
    except requests.RequestException:
        print(f"Falha ao consultar o jogo com id ({appid_atual})")
        continue
    try:
        preco = dados_preco[str(appid_atual)]["data"]["price_overview"]
    except KeyError:
        print(f"Jogo com id :{appid_atual} sem preço, gratuito, não lançado ou indisponível")
        continue
    if preco["discount_percent"] >= DESCONTO_MINIMO:
        promocoes.append({
            "nome" : dados_preco[str(appid_atual)]['data']['name'],
            "preco" : preco['final_formatted'],
            "desconto": preco['discount_percent'],
            "appid": appid_atual,
        })
if promocoes:
    linhas = [
        f"**{jogo['nome']}**: {jogo['preco']} (-{jogo['desconto']}%)\n"
        f"<https://store.steampowered.com/app/{jogo['appid']}>"
        for jogo in promocoes
    ]

    # blocos de 10 jogos por mensagem, por causa do limite de 2000 caracteres
    for i in range(0, len(linhas), 10):
        texto = "\n\n".join(linhas[i:i + 10])
        try:
            resposta = requests.post(
                DISCORD_WEBHOOK_URL, json={"content": texto}, timeout=10
            )
            resposta.raise_for_status()
        except requests.RequestException:
            print("Falha ao enviar para o Discord.")
        time.sleep(1)
else:
    print("Nenhum jogo em promoção.")