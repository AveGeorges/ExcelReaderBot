from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import CommandStart
from dotenv import load_dotenv

from operations import download_file, get_content, get_item_price
from database import init_db

from logger import logger

import asyncio

import os

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="Загрузить файл")]
    ], resize_keyboard=True)
    await bot.send_message(message.chat.id, """Добро пожаловать в наш бот!\n
Нажмите на кнопку Загрузить файл, чтобы загрузить файл Excel в бот и увидеть его содержимое.
    """, reply_markup=keyboard)
    
    
@dp.message(F.text == "Загрузить файл")
async def upload_file(message: types.Message):
    await bot.send_message(message.chat.id, """Пожалуйста, отправьте файл Excel.\nУбедитесь, что в файле есть столбцы
с названием 'title', 'url', 'xpath'.
    """)
    

@dp.message(F.content_type == types.ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    
    logger.info(f"Document received from user {message.from_user.id}")
    
    document = message.document
    if document.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        await bot.send_message(message.chat.id, "Файл Excel успешно загружен!")
        
        logger.info(f"Document {document.file_name} successfully uploaded")
        
        file = await download_file(document, bot)
        logger.info(f"File {document.file_name} successfully downloaded")
        
        content = await get_content(file)
        logger.info(f"Content successfully read")
        
        for item in content:
            price = await get_item_price(content[item], message.from_user.id)
            content[item]['price'] = price
            
        logger.info(f"Prices successfully read")

        text = "Содержимое файла:\n\n"
        for count, item in enumerate(content):
            text += f"Товар №{count + 1}:\n"
            text += f"1. Title: {content[item]['title']}\n2. URL: {content[item]['url']}\n3. XPath: {content[item]['xpath']}\n4. Price: {content[item]['price']}\n\n"

        await bot.send_message(message.chat.id, f"{text}")
        
    else:
        await bot.send_message(message.chat.id, "Пожалуйста, отправьте файл Excel")
        
        logger.error(f"Document {document.file_name} is not an Excel file")
    

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logger.info("Bot started")
    asyncio.run(main())
