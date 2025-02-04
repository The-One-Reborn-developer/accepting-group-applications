import asyncio
import os
import logging

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher

from bot.routes.start import start_router
from bot.database.orm import Application, DatabaseManager
from bot.scripts.spreadsheet import (
    initialize_spreadsheet,
    scrape_ru_group_links,
    scrape_en_group_links,
    scrape_channels_links
)


async def main() -> None:
    load_dotenv(find_dotenv())

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )
    logging.info('Initializing database...')
    DATABASE = DatabaseManager()
    logging.info('Creating tables...')
    DATABASE.create_tables()
    logging.info('Tables created.')

    logging.info('Initializing spreadsheet...')
    spreadsheet = initialize_spreadsheet()
    logging.info('Spreadsheet initialized.')

    logging.info('Scraping russian groups worksheet...')
    ru_groups_links = scrape_ru_group_links(spreadsheet)
    logging.info('Scraping english groups worksheet...')
    en_groups_links = scrape_en_group_links(spreadsheet)
    logging.info('Scraping channels worksheet...')
    channels_links = scrape_channels_links(spreadsheet)
    logging.info('Spreadsheet links scraped.')

    logging.info('Getting links from database...')
    links_in_database = Application.get_applications()
    readable_links_list = [link.to_dict() for link in links_in_database]

    database_links = [link_data['link']
                      for link_data in readable_links_list]
    logging.info('Populating database with the links from spreadsheet...')
    for link in ru_groups_links:
        if link not in database_links and link != '' and link != 'Ссылка':
            logging.info(f'Adding {link} to database...')
            Application.insert_application(link=link)
    for link in en_groups_links:
        if link not in database_links and link != '' and link != 'Ссылка':
            logging.info(f'Adding {link} to database...')
            Application.insert_application(link=link)
    for link in channels_links:
        if link not in database_links and link != '' and link != 'Ссылка':
            logging.info(f'Adding {link} to database...')
            Application.insert_application(link=link)
    logging.info('Database populated.')

    logging.info('Starting bot.')
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher()
    logging.info('Dispatcher created.')

    dp.include_router(start_router)
    logging.info('Routes added.')

    await bot.delete_webhook(drop_pending_updates=True)
    logging.info('Webhook deleted.')
    logging.info('Starting polling...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
