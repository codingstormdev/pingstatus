# telegram status bot v1 by telegram @codingstorm (@yfimsky)
import time  # i dunno why i put it here
import pythonping  # really need to make bot working
import sqlite3 # for banned ppl
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from datetime import datetime  # useless shit but i have it l0l

TOKEN = ''  # put ur telegram bot token here

admin = []  # put ur id here

channel = "" # put ur telegram channel here but before add the bot there and make him admin

host = '' # type any host u want

bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher()
now = datetime.now()
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
logger.error("Starting bot")

with sqlite3.connect("config.db") as cfgdb:
    cfgbd = cfgdb.cursor()

    cfgbd.execute("""CREATE TABLE IF NOT EXISTS list(
        userid INTEGER
    )""")

@dp.message(commands=['start'])
async def status(message: Message) -> None:
    try:
        bandb = sqlite3.connect("config.db")
        bancur = bandb.cursor() 
        if bancur.execute("SELECT userid FROM list WHERE userid = ?", (message.from_user.id,)).fetchone() == None:
            if message.from_user.id in admin:
                await message.reply('Started.')  # bot says what hes started important thing
                while True:
                    ping = pythonping.ping(host).rtt_avg_ms  # ping thing
                    now = datetime.now()  # u can delete this if u want
                    current_time = now.strftime("%H:%M:%S")  # this too
                    await bot.send_message(channel, f'Telegram ping is: {ping}\nLocal time is: {current_time}')
                    time.sleep(60)  # bed time!
            else:
                await message.reply('You can not use that bot.\n' + 'Bot was not made chatting.')
                await bot.send_message(message.chat.id, f"{message.from_user.id} was banned.")
                bancur.execute("INSERT INTO list (userid) VALUES(?)", (message.from_user.id,))
        else:
            if bancur.execute("SELECT userid FROM list WHERE userid = ?", (message.from_user.id,)).fetchone() != None:  # lil shit to do not cloning the same user id
                pass
            else:
                bancur.execute("INSERT INTO list (userid) VALUES(?)", (message.from_user.id,))
    except sqlite3.Error as e:
            await message.answer(e)
    finally:
            bandb.commit()
            bandb.close()
        
   


@dp.message(commands=['stop'])
async def stop(message: Message) -> None:
    if message.from_user.id in admin:
        await message.reply("Shutting down, please be patient")
        sys.exit()

def main() -> None:
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
