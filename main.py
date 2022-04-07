from discord.ext import commands
from selenium import webdriver 
import discord
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
from threading import Thread 
import asyncio
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

number = '+919039997961'
prefix = '#'
look = False

driver.get(f'https://web.whatsapp.com/send?phone={number}')


def checkLogin():
	try:
		button = driver.find_element(by=By.CLASS_NAME, value='_2znac')
		button.click()
		return True
	except:
		try:
			if 'To use WhatsApp on your computer:' in driver.page_source:
				return True
			else:
				print('from else')
				return False
		except:
			print('from except')
			return False

def checkDM():
	try:
		page = driver.find_element(by=By.CLASS_NAME , value='_23P3O')
		return False
	except:
		return True

def Login():
	global look
	while checkLogin():
		driver.save_screenshot("static/qr.png")
		im = Image.open("static/qr.png")
		left = 965;top = 225;right = 1368;bottom = 628
		im.crop((left,top,right,bottom)).save('static/qr.png')
		time.sleep(1)
	print('Logged In!')
	driver.get(f'https://web.whatsapp.com/send?phone={number}')
	while checkDM():
		driver.get(f'https://web.whatsapp.com/send?phone={number}')
		time.sleep(30)
	look = True
	print('Interface Loaded!')



client = commands.Bot(command_prefix=prefix)



@client.event 
async def on_ready():
	thr = Thread(target=Login)
	thr.daemon = True
	thr.start()
	print('I\'m Kinda Alive!')

webhooks = [938792403479973918,938791542586503228,938792290732871711,938791641693687889]

@client.event
async def on_message(message):
	
		if message.author.id == client.user.id:
			if message.content == f'{prefix}qr':
				with open('static/qr.png', "rb") as fh:
					f = discord.File(fh, filename='static/qr.png')
				await message.channel.send(file=f)

		if look and message.author.id in webhooks and message.guild.id == 864766766932426772:
			async for msg in message.channel.history(limit=10):
				if msg.id == message.id:
					for embed in msg.embeds:
						embedInfo = (embed.to_dict())
					channelName = msg.channel.name
					coordinates = msg.content
					if '<'and'>' in coordinates:
						coordinates = coordinates.split()[-1]
					title = embedInfo['title']
					name = title.split()[1]+' '+title.split()[2]
					if '<' in name:
						name = name.split('<')[0]
					shiny = True if ':shiny:' in title else False
					gender = 'male' if ':male:' in title else 'female' if ':female:' in title else 'undefined'
					image = embedInfo['thumbnail']['url']
					fields = embedInfo['fields']

					type = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')


					channelName = channelName[2:]
					type.send_keys(f'Channel Name - #{channelName} || Coordinates - {coordinates} || Pokémon - {name} || Shiny - {shiny} || Gender - {gender} || Image - {image} ')
					
					types = []
					generation = ''
					gps = []
					attacks = []
					details = []

					for i in fields:
						name_ = i['name']
						values = i['value'].split('\n')
						for i in values:
							if str(i).startswith('Type:'):
								generation = i.split('|')[-1].split(':')[-1].strip()
								types = []
								type_ = i.split('|')[0].split('<')
								for j in type_:
								    types.append(j.split(':')[1])
								types = list(filter(lambda x:  x != ' ' , types))
							elif ':iv:' in i:
								details = []
								test=i.split('<')
								for j in test:
								    details.append((j.split('>')[-1].strip()))
								details = list(filter(lambda x:  x != ' ' and x != '' , details))
								details = list(map(lambda x: '100% (15/15/15)' if x.startswith('💯%') else x , details ) )
							elif 'FakeGPS' in i:
								gps = []
								for j in i.split('|'):
								    gps.append((j.split('<')[-1].split('>')[0].strip()))
								gps = list(filter(lambda x:  x != ' ' and x != '' , gps))
				
							else:
								attacks = []
								for j in i.split('/'):
								    attacks.append((j.split('>')[-1].strip()))
								attacks = list(filter(lambda x:  x != ' ' and x != '' , attacks))
						if types != []:
							type.send_keys(f'|| Type - {types} ')
						if generation != '':
							type.send_keys(f'|| Generation - {generation} ')
						if details != []:
							type.send_keys(f'|| IV - {details[0]} || CP - {details[1]} || LV - {details[2]} ')
						if gps != []:
							type.send_keys(f'|| FakeGPS - {gps[0]} || iPogo - {gps[1]} || Velocity - {gps[2]} ')
						if attacks != []:
							type.send_keys(f'|| Attacks - {attacks} ')
					driver.find_element(By.CLASS_NAME , value='_4sWnG').click()
					await asyncio.sleep(0.1)

	

client.run('NzkwOTIxMjQ0NjUxNTUyNzY5.YhG0ww.vyKF1x-fKIqc68We5malAtigtNo',bot=False)
