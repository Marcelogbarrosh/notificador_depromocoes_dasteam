import os
from dotenv import load_dotenv
import requests
import time
import json

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_NOTIFICADOS = os.path.join(PASTA, "notificados.json")

load_dotenv(os.path.join(PASTA, ".env"))
#verifica se ja existe um json
if os.path.exists(ARQUIVO_NOTIFICADOS):
    with open(ARQUIVO_NOTIFICADOS, "r", encoding="utf-8") as f:
        notificados = json.load(f)
else:
    notificados = {}

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
        if str(appid_atual) not in notificados or preco['final'] < notificados[str(appid_atual)]:
            promocoes.append({
                "nome" : dados_preco[str(appid_atual)]['data']['name'],
                "preco" : preco['final_formatted'],
                "desconto": preco['discount_percent'],
                "appid": appid_atual,
                "precocomparavel": preco['final'],
            })
    else:
         notificados.pop(str(appid_atual), None)
if promocoes:
    
    linhas = [
        f"**{jogo['nome']}**: {jogo['preco']} (-{jogo['desconto']}%)\n"
        f"<https://store.steampowered.com/app/{jogo['appid']}>"
        for jogo in promocoes
    ]

    for i in range(0, len(linhas), 5):
        
        texto = "\n\n".join(linhas[i:i + 5])
        bloco = promocoes[i:i + 5]
        try:
            resposta = requests.post(DISCORD_WEBHOOK_URL, json={"content": texto}, timeout=10)
            resposta.raise_for_status()
        except requests.RequestException:
            print("Falha ao enviar para o Discord.")
        else:##se nao der except ele sobrescreve ou adiciona um novo
           
            for jogo in bloco:
                notificados[str(jogo['appid'])] = jogo['precocomparavel']

        time.sleep(1)

with open(ARQUIVO_NOTIFICADOS, "w", encoding="utf-8") as f:
    json.dump(notificados, f)