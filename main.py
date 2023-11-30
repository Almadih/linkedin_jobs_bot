#!/usr/bin/env python

import asyncio
import logging
from bot_commands import CustomContext,start,number_of_queries,number_of_users,add_query,get_queries,cancel_query
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from constants import TOKEN, URL
from scraper import start_scrape



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def main(request) -> None:
    """Set up PTB application and a web application for handling the incoming requests."""
    context_types = ContextTypes(context=CustomContext)
    # Here we set updater to None because we want our custom webhook server to handle the updates
    # and hence we don't need an Updater instance
    application = (
        Application.builder().token(TOKEN).updater(None).context_types(context_types).build()
    )

    # register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler('add_query',add_query))
    application.add_handler(CommandHandler('queries',get_queries))
    application.add_handler(CommandHandler('cancel_query',cancel_query))
    application.add_handler(CommandHandler('num_users',number_of_users))
    application.add_handler(CommandHandler('num_queries',number_of_queries))

    # Pass webhook settings to telegram
    await application.bot.set_webhook(url=f"{URL}/telegram", allowed_updates=Update.ALL_TYPES)

    path = request.path.split('/')[-1]

    if path == '/telegram':
        await telegram(application,request.body)
    elif path == '/health-check':
        return await health()
    elif path == '/scrape':
         await start_scrape(logger,application)
    
    async with application:
             await application.start()
             await application.stop()
    return {"msg":"done"}


async def telegram(application,request) -> None:
        """Handle incoming Telegram updates by putting them into the `update_queue`"""
        await application.update_queue.put(Update.de_json(data=request.get_json(), bot=application.bot))


async def health() -> dict:
        """For the health endpoint, reply with a simple plain text message."""
        response = {"msg":"The bot is still running fine :)"}
        return response


def hello_http(event, context):
    return asyncio.run(main(event))
