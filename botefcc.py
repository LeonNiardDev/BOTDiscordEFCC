import discord
from discord.ext import tasks
import requests

# Ton token Discord (à ne pas partager)
TOKEN = 'MTI5NjQwOTc1MDY4MjA3NTEzNg.G8hfbq.54JSBacow9gm_ZCIITnr13F20rpPMtOMSx6KdA'

# ID du serveur et du channel à mettre à jour
SERVER_ID = 1268019169337671721
CHANNEL_ID = 1296411871573970997

# App ID du jeu
APP_ID = '3168470'

# Crée une instance du bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Fonction pour récupérer le nombre de joueurs
def get_player_count(app_id):
    game_players_url = f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}'
    response = requests.get(game_players_url)
    
    if response.status_code == 200:
        return response.json()['response']['player_count']
    else:
        return None

# Tâche répétitive qui met à jour le nom du channel
@tasks.loop(minutes=10)  # Met à jour toutes les 10 minutes
async def update_channel():
    guild = client.get_guild(SERVER_ID)
    channel = guild.get_channel(CHANNEL_ID)

    if channel:
        player_count = get_player_count(APP_ID)
        if player_count is not None:
            new_channel_name = f'Live players : {player_count}'
            await channel.edit(name=new_channel_name)
            print(f'Channel updated: {new_channel_name}')
        else:
            print("Erreur lors de la récupération des joueurs")

# Événement quand le bot est prêt
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    update_channel.start()  # Démarre la tâche répétitive

# Lancer le bot
client.run(TOKEN)
