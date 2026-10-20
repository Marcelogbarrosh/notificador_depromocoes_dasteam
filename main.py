import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")
DESCONTO_MINIMO = int(os.getenv("DESCONTO_MINIMO", "50"))

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
    print(dados_preco[str(appid_atual)]["data"]["name"])
    print(preco["final_formatted"])
    print(f"desconto :{preco['discount_percent']} %")


