#-*-coding:utf8;-*-
#qpy:3
#qpy:console

import config
import telebot 
import searchClass
from telebot import types
import time

#0 - главное меню
#1 - автор
#2 - название
#3 - тэг
#4 - год
#5 - AddDB


#diSendBook для запоминания того, что еще надо выслать. По факту это будет, библиотека key-value, а value будет массив с массивами массивов.... бля...
diSendBook = {}
#di для отслеживания текущего меню
di = {}
#diDosProtect библиотека для отслеживания сообщений (защита от дос)
diDosProtect = {}

onButtonClick = 0

bot = telebot.TeleBot(config._TOKEN, skip_pending=True)



@bot.message_handler(commands=['start'])
def start(message):
	
	if diDosProtect.get(message.chat.id) == None:
		diDosProtect[message.chat.id] = True
	if diDosProtect[message.chat.id] == True:
		diDosProtect[message.chat.id] = False
		bot.send_message(message.chat.id, "Тебя приветствует поисковый бот 'Бздынь-библиотеки', это первый бот который специализируется только на книгах из мира Программирование! А вот тут наш канал @bzd_channel и чат @book_it :-)")
		di[message.chat.id] = 0
		if sendMainMenu(message.chat.id):
			diDosProtect[message.chat.id] = True
			return
	else:
		return
	
####Markup-ы менюшек, дабы не пересоздавать каждый раз
#Главное меню
markupMainMenu = types.ReplyKeyboardMarkup()
markupMainMenu.resize_keyboard = True
itemAuthorMainMenu = types.KeyboardButton("Автор")
itemNameMainMenu = types.KeyboardButton("Название")
itemTagsMainMenu = types.KeyboardButton("Тэг")
itemAgeMainMenu = types.KeyboardButton("Год")
markupMainMenu.row(itemAuthorMainMenu, itemNameMainMenu)
markupMainMenu.row(itemTagsMainMenu, itemAgeMainMenu)
#Кнопка выхода в главное меню
markupReplyMenu = types.ReplyKeyboardMarkup()
markupReplyMenu.resize_keyboard = True
itemReplyMenu = types.KeyboardButton("🏠 Главное меню 🏠")
markupReplyMenu.row(itemReplyMenu)

##########
	

@bot.message_handler(content_types=['text'])
def MainFunction(message):
	
	
	#Admin commands
	global onButtonClick
	messageText = message.text
	messageChatId = message.chat.id
	
	if diDosProtect.get(messageChatId) != None:
		if diDosProtect[messageChatId] == False:
			return
		
	
	if messageChatId == config._FATHERid:
		#Отображение Dictionary
		if messageText == "Dict":
			bot.send_message(config._FATHERid,str(di))
			return
		#Отображение счетчика кликов
		if messageText == "Click":
			bot.send_message(config._FATHERid, str(onButtonClick))
			return
		#Режим добавления в базу данных
		if messageText == "AddDB":
			di[config._FATHERid] = 5
			bot.send_message(config._FATHERid, "ok, можно добавлять")
			return
		#Создать таблицу book (используется 1 раз, при самом первом старте бота)
		if messageText == "CreateTable":
			ret = searchClass.createTable()
			bot.send_message(config._FATHERid, ret)
		#Режим возвращения информации
		if messageText == "ReturnInform": 
			di[config._FATHERid] = 6
			bot.send_message(config._FATHERid, "ok, отправьте файл для получение информации")
		#Отобразить все значения из базы данных
		if messageText == "SelectAll":
			ret_text = telebot.util.split_string(str(searchClass.selectAll()), 4000)
			for i in ret_text:
				bot.send_message(config._FATHERid, str(i))
		#Подсчет строк
		if messageText == "CountRows":
			bot.send_message(config._FATHERid, str(searchClass.countRows()))
		#Остановить бота
		if messageText == "StopBotNow":
			bot.send_message(config._FATHERid, "Бот остановлен")
			print ("Bot stoped")
			exit()
				
				
	# User and menu
	try:
		#Если сообщение отправлено из главного меню, ищем команду перехода к поиску
		if di[messageChatId] == 0 or di[messageChatId] > 4:
			changeMenu(messageText,messageChatId)
			return
		#Если мы в подменю и пришло сообщение с командой перейти в главное меню - переходим
		if di[messageChatId] != 0:
			if messageText == "🏠 Главное меню 🏠":
				di[messageChatId] = 0
				sendMainMenu(messageChatId)
				onButtonClick += 1
				return
				
			if diDosProtect.get(messageChatId) == None:
				diDosProtect[messageChatId] = True
				
			if diDosProtect[messageChatId] == True:
				diDosProtect[messageChatId] = False
				if len(messageText) <= 30:
					if di[messageChatId] == 1: #автор
						if firstSend(searchClass.search(message, "author"), messageChatId):
							diDosProtect[messageChatId] = True
							return
					if di[messageChatId] == 2: #Название
						if firstSend(searchClass.search(message, "name"), messageChatId):
							diDosProtect[messageChatId] = True
							return
					if di[messageChatId] == 3: #Тэг
						if firstSend(searchClass.search(message, "tag"), messageChatId):
							diDosProtect[messageChatId] = True
							return
					if di[messageChatId] == 4: #Год
						if firstSend(searchClass.search(message, "age"), messageChatId):
							diDosProtect[messageChatId] = True
							return
				else:
					bot.send_message(messageChatId, "В твоём запросе больше 30 символов")
					diDosProtect[messageChatId] = True
					return
		
			
	except KeyError:
		changeMenu(messageText, messageChatId)
		if di.get(messageChatId) == None:
			di[messageChatId] = 0 
			sendMainMenu(messageChatId)
	

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if diDosProtect.get(call.message.chat.id) == None:
		diDosProtect[call.message.chat.id] = True
	if diDosProtect[call.message.chat.id] == True:
		diDosProtect[call.message.chat.id] = False
		if call.message:
			if call.data == "again":
				bot.delete_message(call.message.chat.id, call.message.message_id)
				if collectAgain(call.message.chat.id):
					diDosProtect[call.message.chat.id] = True
			return
	
@bot.message_handler(content_types=['document'])
def documMessage(message):
	if message.chat.id == config._FATHERid:
		try:
			#Добавление в базу данных
			if di[config._FATHERid] == 5:
				messReturn = searchClass.addDB(message)
				bot.send_message(config._FATHERid, messReturn)
				
			#Информационное сообщение
			if di[config._FATHERid] == 6:
				bot.send_message(config._FATHERid, str(message))
				
		except KeyError:
			bot.send_message(config._FATHERid, "KeyError, вас не было в базе")
			return
		

def sendReplyMenu(messageChatId, NameMenu):
	bot.send_message(messageChatId, "Введите данные для поиска в выбранной категории ({name}) ".format(name=NameMenu), reply_markup=markupReplyMenu)
	return

def sendMainMenu(messageChatId):
	bot.send_message(messageChatId, "🏠 Главное меню 🏠", reply_markup=markupMainMenu)
	return True

#Первая отправка сообщения с книгами, складывает книги в diSendBook и отправляет три
def firstSend(message, chatId):
	if message[0] == "error":
		bot.send_message(chatId, message[1])
		return True
	if len(message) <= 3:
		sendBook(message, chatId, False, 0)
		return True
	else:
		diSendBook[chatId] = message
		print (str(diSendBook[chatId]))
		i = 0
		retList=[]
		while i<3:
			retList.append(diSendBook[chatId].pop())
			i += 1
		sendBook(retList,chatId,True,len(diSendBook[chatId]))
		return True
		
#Все последующие отправки книг из того же комплекта, режет по три книги и дает на отправку функции sendBook
def collectAgain(chatId):
	if diSendBook.get(chatId) == None:
		#bot.send_message(chatId, "Отправлять нечего")
		return True
	if len(diSendBook[chatId]) <= 3:
		sendBook(diSendBook[chatId], chatId, False, 0)
		diSendBook[chatId].clear()
		return True
	i = 0
	retList = []
	while i<3:
		retList.append(diSendBook[chatId].pop())
		i += 1
	sendBook(retList,chatId,True,len(diSendBook[chatId]))
	return True
		
	
#Занимается отправкой книг
def sendBook(message,chatId,sendButton,residue):
	p = 0
	for i in message:
		p += 1
		markup = types.InlineKeyboardMarkup()
		item = types.InlineKeyboardButton(text="Перейти к книге", url=i[5].strip())
		itemAgain = types.InlineKeyboardButton(text="Далее, осталось книг: " + str(residue), callback_data="again")
		markup.row(item)
		bot.send_message(chatId, "ID: {id}\nТэги: {tag}\nЯзык: {language}\nАвтор: {author}\nНазвание: {name}\nГод: {age}\nСсылка: {link}\n".format(id=i[0],tag=i[3],author=i[1],name=i[2],age=i[4],link=i[5],language=i[6]), reply_markup=markup)
		if sendButton == True:
			if p == len( message):
				keyboard = types.InlineKeyboardMarkup()
				item = types.InlineKeyboardButton(text = "Далее", callback_data="again")
				keyboard.add(item)
				bot.send_message(chatId, "Осталось книг: " + str(residue), reply_markup= keyboard)
	return
	
#Выбор Меню
def  changeMenu(messageText, messageChatId):
		global onButtonClick
		if di.get(messageChatId) != None:
			if di[messageChatId] != 0:
				if messageText == "🏠 Главное меню 🏠":
					di[messageChatId] = 0
					sendMainMenu(messageChatId)
					onButtonClick += 1
					return 
		if messageText == "Автор":
				di[messageChatId] = 1
				sendReplyMenu(messageChatId,"Автор")
				onButtonClick += 1
				return 
		if messageText == "Название":
				di[messageChatId] = 2
				sendReplyMenu(messageChatId,"Название")
				onButtonClick += 1
				return 
		if messageText == "Тэг":
				di[messageChatId] = 3
				sendReplyMenu(messageChatId,"Тэг")
				onButtonClick += 1
				return 
		if messageText == "Год":
				di[messageChatId] = 4
				sendReplyMenu(messageChatId,"Год")
				onButtonClick += 1
				return
		return
			
	
while True:
	try:
		bot.polling(none_stop=True)
	except Exception as e:
		print ("\nЯ УПАЛ! Ошибка: ")
		print (str(e))
		print ("-----------------")
		time.sleep(5)
		continue
    
    
    
    
    
    
    
