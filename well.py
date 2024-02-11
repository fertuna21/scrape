import asyncio
import aiohttp
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.error import TelegramError


TELEGRAM_BOT_TOKEN = '6705992658:AAEy6Mjj5GlWkF4vWdRFCpU0PUv2c6C3o-4'
TELEGRAM_CHAT_ID = '-1002114092452'


async def fetch_website_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def main():
    try:
        url = 'https://www.ethiopia-insight.com/'

        website_content = await fetch_website_content(url)
        soup = BeautifulSoup(website_content, 'html.parser')
        text_content = soup.get_text()

        # Extract image URLs
        image_urls = [img['src'] for img in soup.find_all('img')]

        bot = Bot(token=TELEGRAM_BOT_TOKEN)

        message = f"Found link: {url}\n{text_content}"

        # Send text content
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

        # Send images
        for image_url in image_urls:
            try:
                await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=image_url)
            except TelegramError as e:
                print(f"Error sending photo: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")


if asyncio.get_event_loop().is_running():
    asyncio.create_task(main())
else:
    asyncio.run(main())
