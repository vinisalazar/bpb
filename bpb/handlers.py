import locale
import logging

from telegram.ext import CommandHandler, Filters, MessageHandler

from .messages import (
    CLEAR,
    ERRO_AO_MARCAR,
    MARCADA_PARA,
    PLEASE_SCHEDULE,
    REPETIRA,
    SEM_REUNIAO,
    SEM_VALOR,
    START,
    WELCOME,
    LINKS_IMPORTANTES,
)
from .utils import get_meeting_range, parse_date

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


def start(update, context):

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=START,
    )


def get_meeting(update, context):

    try:
        datetime_obj = getattr(context.bot, "next_meeting")

        parsed_date, _ = parse_date(datetime_obj)
        message = MARCADA_PARA.format(parsed_date=parsed_date).lower().capitalize()

        try:

            next_meetings = getattr(context.bot, "next_meetings")
            message += REPETIRA + " \n".join(i[0] for i in next_meetings)

        except AttributeError as e:

            logger.error(e)
            pass

    except Exception as _:

        message = SEM_REUNIAO + PLEASE_SCHEDULE

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def set_meeting(update, context):

    try:

        parsed_date, datetime_obj, next_meetings = get_meeting_range(context.args)

        # Add attributes to bot
        context.bot.next_meeting = datetime_obj
        context.bot.next_meetings = next_meetings

        message = (
            MARCADA_PARA.format(parsed_date=parsed_date).lower().capitalize() + REPETIRA
        )
        message += " \n".join(i[0] for i in context.bot.next_meetings)

    except Exception as e:

        message = ERRO_AO_MARCAR
        message += f"'{' '.join(context.args)}'" if len(context.args) > 1 else SEM_VALOR

        logger.error(e)

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def clear_meetings(update, context):

    try:

        delattr(context.bot, "next_meeting")
        delattr(context.bot, "next_meetings")
        message = CLEAR + PLEASE_SCHEDULE

    except AttributeError:

        message = SEM_REUNIAO

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def links(update, context):

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=LINKS_IMPORTANTES, parse_mode="Markdown"
    )


def welcome(update, context):

    new_member = update.message.new_chat_members[0]

    user_text = f"[{new_member.full_name}](tg://user?id={new_member.id})"

    welcome_message = WELCOME.format(user_text=user_text)

    update.message.reply_text(welcome_message, parse_mode="Markdown")


def get_handlers():

    handlers = [
        MessageHandler(Filters.status_update.new_chat_members, welcome),
        CommandHandler("start", start),
        CommandHandler("setmeeting", set_meeting),
        CommandHandler("getmeeting", get_meeting),
        CommandHandler("clear", clear_meetings),
        CommandHandler("links", links),
    ]

    return handlers
