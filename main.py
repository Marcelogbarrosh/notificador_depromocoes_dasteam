import os
from dotenv import load_dotenv
import requests

load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

urlwish = "https://api.steampowered.com/IWishlistService/GetWishlist/v1/"
urlpreco = "https://store.steampowered.com/api/appdetails"

#parâmetros usados
user = {
    "key" : STEAM_API_KEY,
    "steamid" : STEAM_ID,
}

resposta = requests.get(urlwish, params=user, timeout=10)

print(resposta.status_code) #200 = ok; 404 = perfil não encontrado; 429 = rate limit exceded
#""try except""" pra ver se funcionou
resposta.raise_for_status() 

dados = resposta.json() #recebe convertendo pra dicionario

lista_appid = []
tamanho = len(dados['response']['items'])
for i in range(tamanho):
    appid_atual = dados['response']['items'][i]['appid']
    lista_appid.append(appid_atual)

for i in range(len(lista_appid)):
    print(f"{i+1} = {lista_appid[i]}")