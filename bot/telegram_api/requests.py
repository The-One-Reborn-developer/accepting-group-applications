import logging
import aiohttp
import os


async def send_notification(application_data) -> bool:
    BASE_URL = f'https://api.telegram.org/bot{
        os.getenv("TELEGRAM_BOT_TOKEN")}/sendMessage'
    logging.info("Trying to send notification...")
    try:
        async with aiohttp.ClientSession() as session:
            username = application_data['username'].replace(
                'https://t.me/', '@')
            link = application_data['link'].replace(
                'https://t.me/', '@'
            )
            description = application_data['description']
            category = application_data['category']
            logging.info(f"{username}, {link}, {description}, {category}")
            await session.post(
                BASE_URL,
                data={
                    'chat_id': os.getenv('ADMIN_GROUP_CHAT_ID'),
                    'text': f'{username}:\n'
                    f'Ссылка: {link}\n'
                    f'Описание: <code>{description}</code>\n'
                    f'Категория: {category}',
                    'parse_mode': 'HTML'
                }
            )

        return True
    except Exception as e:
        logging.exception(f'Exception in send_notification: {e}')
        return False
