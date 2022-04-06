from discord.ext import commands
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

driver.get(f'https://web.whatsapp.com')
time.sleep(5)
for i in range(20):
	driver.save_screenshot("static/qr.png")
	im = Image.open("static/qr.png")
	left = 965;top = 225;right = 1368;bottom = 628
	im.crop((left,top,right,bottom)).save('static/qr.png')
	time.sleep(1)


client = commands.Bot(command_prefix='#')

@client.event 
async def on_ready():
	print('Now Looking!')

webhooks = [938792403479973918,938791542586503228,938792290732871711,938791641693687889]

@client.event
async def on_message(message):
	try:
		if message.author.id in webhooks and message.guild.id == 864766766932426772:
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
					shiny = True if ':shiny:' in title else False
					gender = 'male' if ':male:' in title else 'female' if ':female:' in title else 'undefined'
					image = embedInfo['thumbnail']['url']
					fields = embedInfo['fields']
					for i in fields:
						name_ = i['name']
						value_ = i['value']
						print(name_)
						print(value_)

					print(image)
					print(channelName ,  coordinates , name , ' | Shiny = ' , shiny  , ' | Gender : ' , gender)

	except Exception as e:
		print(e)

client.run('NzkwOTIxMjQ0NjUxNTUyNzY5.YhG0ww.vyKF1x-fKIqc68We5malAtigtNo',bot=False)
