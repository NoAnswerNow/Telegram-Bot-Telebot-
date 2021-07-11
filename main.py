import requests
from datetime import datetime
import sqlite3
import telebot
from telebot import types
from auth_data import token




def telegram_bot(token) :
	bot = telebot.TeleBot(token) # get your token from auth_data

	@bot.message_handler(commands=["start"])
	def start_message(message) :
		# Main menu of bot where you choose action
		bot.send_message(message.chat.id , "📈Состояние популярной криптовалюты\n👉Введи : price .\n\n💵Курс валют\n👉Введи : money .\n\
			                                \n🔎Полная версия биржи.\n👉Введи : /site\n\
			                                \n💱Конвертер валют\nПеревести доллары в гривны.\n👉Введи : /ua\n\
			                                 \nПеревести гривны в доллары.\n👉Введи : /us")

		# First of all Create your Database, I used SQLITE3
		# Connenct to database
		connect = sqlite3.connect ('C:\\Users\\Maxim\\Desktop\\telegram.db', check_same_thread= False) # path to database
		cursor = connect.cursor()
		# Create table users
		cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY ,user_id INTEGER, first_name TEXT, last_name TEXT, user_name TEXT)""")
		connect.commit()
		#connect.close()
		# select only uniqueness users
		check_id = message.chat.id
		cursor.execute(f"SELECT user_id FROM users WHERE user_id = {check_id}")
		data = cursor.fetchone()
		# if there is no match than add user to the table
		if data is None :
			# add values to the table
			user_id = message.chat.id
			first_name = message.chat.first_name
			last_name = message.chat.last_name
			user_name = message.chat.username
			cursor.execute('INSERT INTO users (user_id, first_name, last_name, user_name) VALUES(?,?,?,?);', (user_id, first_name, last_name, user_name))
			connect.commit()
		else :
			pass

	# Currency converter		
	# Сonvert dollars(USD) to hryvnia(UAH)		
	@bot.message_handler(commands=['ua'])
	def echo_usd_ua(message):
		msg_usd = bot.reply_to(message, "Введите сумму в долларах (USD) :")
		bot.register_next_step_handler(msg_usd, convert_usd_ua) #remember user input

	def convert_usd_ua(message):	
		try :
			user_cash_usd = message.text
			# check that the user has entered a number
			if not user_cash_usd.isdigit():
				msg_usd = bot.reply_to(message, "Введите число. Например, 100, 150, 200 , 253 ...")
				bot.register_next_step_handler(msg_usd, convert_usd_ua)
				return
			req = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
			response = req.json()
			price = response[0]
			rate_usd = float(price['buy']) # convert value of rate from str to float
			user_cash_usd = float(message.text) # convert message from str to float
			result_usd = rate_usd * user_cash_usd # get the result
			bot.send_message(message.chat.id , f" ➡️ {result_usd} грв (UAH)\n ( Курс ПриватБанка)\n{datetime.now().strftime('%Y-%m-%d %H:%M')}✅")
		except Exception as e :
			bot.reply_to(message, "Что-то не так")

     # Сonvert hryvnia(UAH) to dollars(USD)
	@bot.message_handler(commands=['us'])
	def echo_ua_usd(message):
		msg_ua = bot.reply_to(message, "Введите сумму в гривнах (UAH) :")
		bot.register_next_step_handler(msg_ua, convert_ua_usd)

	def convert_ua_usd(message):	
		try :
			user_cash_ua = message.text
			if not user_cash_ua.isdigit():
				msg_ua = bot.reply_to(message, "Введите число. Например, 100, 150, 200 , 253 ...")
				bot.register_next_step_handler(msg_ua, convert_ua_usd)
				return
			req = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
			response = req.json()
			price = response[0]
			rate_usd = float(price['sale']) # convert value of rate from str to float
			user_cash_ua = float(message.text) # convert message from str to float
			result_ua = user_cash_ua/rate_usd
			bot.send_message(message.chat.id , f" ➡️ {result_ua} у.е (USD)\n ( Курс ПриватБанка)\n{datetime.now().strftime('%Y-%m-%d %H:%M')}✅")
		except Exception as e :
			bot.reply_to(message, "Что-то не так")		
	
			

	
	@bot.message_handler(commands = ['site'])
	def url(message):
		# Buttons for hrefs of the full version of sites
		markup = types.InlineKeyboardMarkup()
		btn_site= types.InlineKeyboardButton(text='Yobit.net', url='http://yobit.net/ru/')
		markup.add(btn_site)
		bot.send_message(message.chat.id, "🔎Переход на полную версию", reply_markup = markup)	

		markup = types.InlineKeyboardMarkup()
		btn_site= types.InlineKeyboardButton(text='coinmarketcap.com', url='http://coinmarketcap.com/')
		markup.add(btn_site)
		bot.send_message(message.chat.id, "🔎Переход на полную версию", reply_markup = markup)

		markup = types.InlineKeyboardMarkup()
		btn_site= types.InlineKeyboardButton(text='investing.com', url='https://ru.investing.com/crypto/')
		markup.add(btn_site)
		bot.send_message(message.chat.id, "🔎Переход на полную версию", reply_markup = markup)

	@bot.message_handler(content_types=["text"])
	def send_text(message):
		if message.text.lower() == "price" :
			try:
				# get the exchange rate from yobit.net
				req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
				response = req.json()
				sell_price = response["btc_usd"]["sell"]
				buy_price = response["btc_usd"]["buy"]
				# output to the user
				bot.send_message(
					message.chat.id,
					f"💸 Продажа BTC : {sell_price}\n💰Покупка BTC : {buy_price}\n⌛️{datetime.now().strftime('%Y-%m-%d %H:%M')}"
				)

				req = requests.get("https://yobit.net/api/3/ticker/ltc_usd")
				response = req.json()
				sell_price = response["ltc_usd"]["sell"]
				buy_price = response["ltc_usd"]["buy"]
				bot.send_message(
					message.chat.id,
					f"💸Продажа LTC : {sell_price}\n💰Покупка LTC : {buy_price}\n⌛️{datetime.now().strftime('%Y-%m-%d %H:%M')}"
				)

				req = requests.get("https://yobit.net/api/3/ticker/eth_usd")
				response = req.json()
				sell_price = response["eth_usd"]["sell"]
				buy_price = response["eth_usd"]["buy"]
				bot.send_message(
					message.chat.id,
					f"💸Продажа ETH : {sell_price}\n💰Покупка ETH : {buy_price}\n⌛️{datetime.now().strftime('%Y-%m-%d %H:%M')}"
				)

				req = requests.get("https://yobit.net/api/3/ticker/doge_usd")
				response = req.json()
				sell_price = response["doge_usd"]["sell"]
				buy_price = response["doge_usd"]["buy"]
				bot.send_message(
					message.chat.id,
					f"💸Продажа DOGE : {sell_price}\n💰Покупка DOGE : {buy_price}\n⌛️{datetime.now().strftime('%Y-%m-%d %H:%M')}\n✅"
				)
			
			except Exception as e:
				print(e)
				bot.send_message(
					message.chat.id,
					"☠️☠️☠️Не твой день, с курсом что-то не то, минфин взломан, пакуй чемоданы☠️☠️☠️"
				)


		elif message.text.lower() == "money" :
			try:				
				#get the exchange rate from PrivatAPI
				req = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
				response = req.json()
				price = response[0]
				bot.send_message(
					message.chat.id,
					price['ccy'] +' ➡️ '+ price['base_ccy'] + '\n'+'Покупка' +'  : '+ price['buy'] + '\n'+ 'Продажа' + \
      							' : ' + price['sale'] #rewrite output!
				)

				req = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
				response = req.json()
				price_second = response[1]
				bot.send_message(
					message.chat.id,
					price_second['ccy'] +' ➡️ '+ price_second['base_ccy'] + '\n'+'Покупка' +'  : '+ price_second['buy'] + '\n'+ 'Продажа' + \
      							' : ' + price_second['sale'] + '\n' + '✅') #rewrite output!

			except Exception as e:
				print(e)
				bot.send_message(
					message.chat.id,
					"☠️☠️☠️Не твой день, с курсом что-то не то, минфин взломан, пакуй чемоданы☠️☠️☠️"
				)
		else :
			bot.send_message(message.chat.id, "🤦‍♂️🚬Там что-то не ясно написано? Price, Money, /site, /ua, /us... Попробуй еще, мы верим в тебя... ")

	



	bot.polling()		

if __name__ == '__main__' :
	telegram_bot(token)	