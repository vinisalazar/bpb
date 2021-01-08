import locale
import logging
import os
from datetime import timedelta

from telegram import ext

from utils import parse_date

please_schedule = " Por favor marque um horário com o comando /setmeeting."

# Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

# Handlers
def start(update, context):

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Olá, sou o BPB!\n O bot de Boas práticas do Código Bonito.",
    )


def get_meeting(update, context):

    try:
        datetime_obj = getattr(context.bot, "next_meeting")
        parsed_date, _ = parse_date(datetime_obj)
        message = f"A próxima reunião está marcada para:\n {parsed_date}.\n".lower().capitalize()

        try:

            next_meetings = getattr(context.bot, "next_meetings")
            message += "Esse horário irá se repetir pelas próximas 4 semanas:\n"
            message += " \n".join(i[0] for i in next_meetings)

        except AttributeError:

            pass

    except Exception as _:

        message = "Nenhuma reunião marcada." + please_schedule

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def set_meeting(update, context):

    try:

        # Get message meeting and following ones
        parsed_date, datetime_obj = parse_date(context.args)
        next_meetings, interval = [
            (parsed_date, datetime_obj),
        ], 7
        for _ in range(3):
            next_meetings.append(parse_date(datetime_obj + timedelta(days=interval)))
            interval += interval

        # Add attributes to bot
        context.bot.next_meeting = datetime_obj
        context.bot.next_meetings = next_meetings

        message = f"Reunião marcada para:\n {parsed_date}.\n".lower().capitalize()
        message += "Esse horário irá se repetir pelas próximas 4 semanas:\n"
        message += " \n".join(i[0] for i in context.bot.next_meetings)

    except Exception as e:

        message = (
            "Não consegui marcar a reunião. Por favor verifique a mensagem submetida:\n"
        )
        message += (
            f"'{' '.join(context.args)}'"
            if len(context.args) > 1
            else "Ué, você não enviou nada!"
        )
        logger.error(e)

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def clear_meetings(update, context):

    try:

        delattr(context.bot, "next_meeting")
        delattr(context.bot, "next_meetings")
        message = "Limpei a agenda de reuniões." + please_schedule

    except AttributeError:

        message = "Nenhuma reunião agendada."

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def links(update, context):

    with open("bpb/links_importantes.html", "r") as link_file:
        links_importantes = link_file.read()

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=links_importantes, parse_mode="HTML"
    )


def welcome(update, context):

    new_member = update.message.new_chat_members[0]

    user_text = f"[{new_member.full_name}](tg://user?id={new_member.id})"

    welcome_message = (
        f"Olá, {user_text}! Esse é o grupo do Código Bonito, "
        "um grupo de discussões sobre programação, "
        "bioinformática e ciência aberta. "
        "Se apresente e conte como encontrou o grupo!"
    )

    update.message.reply_text(welcome_message, parse_mode="Markdown")


handlers = [
    ext.MessageHandler(ext.Filters.status_update.new_chat_members, welcome),
    ext.CommandHandler("start", start),
    ext.CommandHandler("setmeeting", set_meeting),
    ext.CommandHandler("getmeeting", get_meeting),
    ext.CommandHandler("clear", clear_meetings),
    ext.CommandHandler("links", links),
]


def main():

    # Defining bot
    updater = ext.Updater(token=os.environ.get("TEL_TOKEN"))
    dispatcher = updater.dispatcher

    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
