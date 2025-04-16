from aiogram import Bot

from logger import logger

import requests
from lxml import html

from database import save_to_db

import pandas as pd



async def download_file(document, bot: Bot):
    file_info = await bot.get_file(document.file_id)
    file_path = file_info.file_path
    file = await bot.download_file(file_path)
    
    return file
    

async def get_content(file):
    content = {}
    raw_data = pd.read_excel(file)
    
    for index, row in raw_data.iterrows():
        content[row['title']] = {
            'title': row['title'],
            'url': row['url'],
            'xpath': row['xpath']
        }
    
    return content


async def get_item_price(item, user_id):
    url = item['url']
    xpath = item['xpath']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        tree = html.fromstring(response.content)
        
        elements = tree.xpath(xpath)
        if not elements:
            logger.warning(f"Элемент не найден по XPath: {xpath}")
            return "Цена не найдена (неверный XPath)"
            
        price = elements[0].text.strip()
        save_to_db(user_id, item['title'], url, xpath, price)
        return price
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к {url}: {e}")
        return "Ошибка загрузки страницы"
    except Exception as e:
        logger.error(f"Неизвестная ошибка при обработке {url}: {e}")
        return "Ошибка при получении цены"


