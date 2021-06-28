import requests
from datetime import datetime
import telebot
from telebot import types
from auth_data import token


def telegram_bot(token) :
	bot = telebot.TeleBot(token) # get your token from auth_data

	@bot.message_handler(commands=["start"])
	def start_message(message) :
		# Main menu of bot where you choose action
		bot.send_message(message.chat.id , "📈Состояние популярной криптовалюты\n👉Введи : price .\n\n💵Курс валют\n👉Введи : money .\n\n🔎Полная версия биржи.\n👉Введи : /site ")
	
	@bot.message_handler(commands = ['site'])
	def url(message):
		#Buttons for hrefs of the full version of sites
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
			bot.send_message(message.chat.id, "🤦‍♂️🚬Там что-то не ясно написано? Price, Money, /site... Попробуй еще, мы верим в тебя... ")

								

	bot.polling()		

if __name__ == '__main__' :
	telegram_bot(token)	