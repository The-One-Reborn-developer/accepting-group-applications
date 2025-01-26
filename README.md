# Telegram bot for a supergroup

A [TG bot](https://t.me/it_chats_bot) for receiving and processing applications for adding groups to a supergroup.

## Features

* Handle user's username, group link, description and category and store them to a database.
* Send a notification to the admin group about new applications.
* Send notifications to users about the status of their applications. *in progress*

## Dependencies

* [aiogram](https://github.com/aiogram/aiogram)
* [python-dotenv](https://github.com/theskumar/python-dotenv)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Docker](https://www.docker.com/)
* [docker-compose](https://docs.docker.com/compose/)

## Setup

Create `.env` file and populate it with environment variables according to `.env.sample`.

## Running

```bash
bash launch.sh
```
