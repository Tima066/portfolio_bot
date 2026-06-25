import sys

#мой токен от бота
DEFAULT_TOKEN = "8704395916:AAGZESNSQl24vPFGo6lTHR6Em90v20f4FbE"

#если в терминали вместе с командой запуска вводится токен то берем его как основной 
#если в терминале запустили без токена то берем мой
if len(sys.argv) >= 2 and ":" in sys.argv[1]:
    BOT_TOKEN = sys.argv[1]
else:
    BOT_TOKEN = DEFAULT_TOKEN

#включение режима отладки
DEBUG_MODE = "--debug" in sys.argv
