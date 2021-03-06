import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import CommandNotFound
from discord.utils import get
import youtube_dl
import os
import webbrowser
import asyncio
from random import choice
import io 
from os import name 
import ffmpeg 



webbrowser.register('Chrome', None, webbrowser.BackgroundBrowser('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'))
URL = 'https://news.google.com/topics/CAAqBwgKMIXDmAswuMmwAw?hl=ru&gl=RU&ceid=RU%3Aru'
HEADERS={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'accept': '*/*'} 
TOKEN= ''
client = commands.Bot(command_prefix= 'F ')
client.remove_command('help')


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('h3', class_='ipQwMb ekueJc gEATFF RD0gLb')
    x=0
    last_news=[]
    for item in items:
        x+=1
        if x<=4:
            last_news.append({
            'news': item.find('a', class_='DY5T1d').get_text()
                      })
        else:
           break
    return last_news
    
        
  
@client.event
async def on_ready():
    print("Флэки активна")
    await client.change_presence( status = discord.Status.online, activity = discord.Game('Happy Tree Frends'))

@client.command(pass_context=True)  
async def help(ctx):
    
    print('F help comand')
    emb = discord.Embed( title = 'Навигация по командам')

    emb.add_field( name = '{}game'.format('F '), value='Пингует пользователей которые смогут пойти с вами играть в выбранные игры. Игры выбираются подкомандами (сокращенное название игр r6 или R6 означает Rainbow Six: Siege, и т.д.')
    emb.add_field( name = '{}info'.format('F '), value='Последние новости, обновляются при вызове команды')
    emb.add_field( name = '{}music'.format('F '), value='Информация для работы с музыкой')
    emb.add_field( name = '{}game'.format('F '), value='Пингует пользователей которые смогут пойти с вами играть в выбранные игры. Игры выбираются подкомандами (сокращенное название игр r6 или R6 означает Rainbow Six: Siege, и т.д.')
    emb.add_field( name = '{}TC'.format('F '), value='Техподдержка если чето не робит')
    await ctx.send( embed = emb )
   



@client.command(pass_context=True)  
async def hello(ctx):
   
    await ctx.send(f"System activated <@here>")
    

@client.command(pass_context=True)  
async def game(ctx, arg=None):
    await ctx.send(format(ctx.message.author))
    if arg=='r6' or arg=='R6':  
        await ctx.send("Зовёт играть в Rainbow Six: Siege <@411072243565592576> <@360698875574616065> <@286827348983283712> <@419195935676170240> <@360003712300613632>")
    elif arg=='apex' or arg=='арех' or arg=='Apex' or arg=='Арех':
        await ctx.send("Зовёт играть в Apex Legends <@411072243565592576> <@286827348983283712> <@419195935676170240> <@360003712300613632>")
    elif arg=='cs' or arg=='кс' or arg=='Cs' or arg=='Кс' or arg=='CS' or arg=='КС':
        await ctx.send("Зовёт играть в Counter-Strike: Global Offensive, малоли сколько у нас отчаянных <@here>")
    elif arg=='циву' or arg=="цивку" or arg=='Циву' or arg=="Цивку":
        await ctx.send("Зовёт играть в Sid Meier’s Civilization VI или Sid Meier’s Civilization V <@411072243565592576> <@286827348983283712> <@419195935676170240> <@360698875574616065>")
    elif arg=='wow' or arg=='вов':
        await ctx.send("Зовёт играть в World of Warcraft <@411072243565592576> <@360698875574616065> <@360003712300613632>")
    elif arg=='si' or arg=='SI' or arg=='свояк':
        await ctx.send("Зовёт играть в SI Game <@here>")
    elif arg==None:
        await ctx.send("Зовёт почилить <@here>")

@client.command(pass_context=True)
async def info(ctx):
    print('F info comand')
    html = requests.get(URL)
    if html.status_code==200:
        print(html)
        mes=get_content(html.text)
        await ctx.send(mes)
    


@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def clear( ctx, amount = 10 ):
    await ctx.channel.purge( limit = amount )




@client.command(pass_context=True)
async def join(ctx):
    global voice
    channel=ctx.message.author.voice.channel
    voice=get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice=await channel.connect()
        await ctx.send(f'Флэки присоеденилась к каналу: {channel}')
        
        

@client.command(pass_context=True)
async def leave(ctx):
    channel=ctx.message.author.voice.channel
    voice=get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice=await channel.connect()
        await ctx.send(f'Флэки отсоеденилась от канала: {channel}')


@client.command(pass_context=True)
async def play(ctx, arg):
    song_there = os.path.isfile('song.mp3')
    rs=requests.get('https://yandex.ru/search/?clid=2367648-307&text=youtubemusic'+arg)
    if rs.status_code==200:
                url=get_url_music(rs.text)
    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удалён')
    except PermissionError:
        print('[log] Не удалось удалить файл')

    await ctx.send('Пожалуйста ожидайте')

    voice = get(client.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{ 
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
            }],
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загружаю музыку...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name=file
            print('[log] Переименнованный файл: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила своё проигрывание'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    name_song = name.rsplit('-', 2)
    await ctx.send(f'Играет трек: {name_song[0]}')






@client.command(pass_context=True)
async def pause(ctx):
       voice.pause()

@client.command(pass_context=True)
async def resume(ctx):
       voice.resume()

@client.command(pass_context=True)
async def stop(ctx):
       voice.stop()
       
@client.command(pass_context=True)
async def TC(ctx):
    embed = discord.Embed(
        title="***Тык*** для перехода",
        description="Мой ВК, типа техподдержка",
        url='https://vk.com/flaky1',
    )
    await ctx.send(embed=embed)
       







@client.command(pass_comtext=True)
async def music(ctx):
    emb=discord.Embed(title = 'Music', colour = discord.Color.dark_gold())
    emb.add_field(name = 'F play + str', value='Флэки запустит трек, надо лишь название трека одним словом')
    emb.add_field(name = 'F pause', value='Флэки поставит трек на паузу')
    emb.add_field(name = 'F resume', value='Флэки запустит трек вновь')
    emb.add_field(name = 'F stop', value='Флэки остановит трек и очистит поток')
    await ctx.send(embed=emb)


def get_url_music(html):
    soup = BeautifulSoup(html, 'html.parser')
    x=0
    for item in soup.find_all('a', class_='link link_theme_outer path__item i-bem'):
        x+=1
        
        link = item['href']
        if x==2:
            any=link
    
    print(any)
    return any
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Мне не доступна эта функция')

        
        
token = os.environ.get('BOT_TOKEN')

client.run(str(token))
