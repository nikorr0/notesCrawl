# python-telegram-bot==20.7
import json
import os

from text_normalization import *
from topic_selector import *
from tf_idf_converter import *
from search_texts import *

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

with open('text_data.json', 'r', encoding="utf8") as f:
    text_data = json.load(f)
API_TOKEN = open("API_TOKEN.txt", "r").read()

CHOOSE, ADD, SAVE, SEARCH = range(4)

reply_keyboard = text_data['menu_keyboard']
menu_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_text(
        text_data['hello_message'],
        reply_markup=menu_markup,
    )

    return CHOOSE


async def add_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(text_data['ask_to_add_notes'], reply_markup=ReplyKeyboardRemove())
    return ADD


async def search_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(text_data['ask_to_send_query'], reply_markup=ReplyKeyboardRemove())

    return SEARCH


async def save_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "Добавить заметки в новый список":
        if os.path.isfile(f'users_notes/{update.message.from_user["id"]}.txt'):
            os.remove(f'users_notes/{update.message.from_user["id"]}.txt')
        os.rename(f"users_notes/temp_{update.message.from_user['id']}.txt", f"users_notes/{update.message.from_user['id']}.txt")

    elif update.message.text == "Добавить заметки в существующий список":
        with open(f"users_notes/temp_{update.message.from_user['id']}.txt", 'r', encoding="utf-8") as temp_file:
            new_notes = temp_file.read()
        os.remove(f"users_notes/temp_{update.message.from_user['id']}.txt")
        with open(f"users_notes/{update.message.from_user['id']}.txt", 'a', encoding="utf-8") as file:
            file.write("\n"+new_notes)

    await update.message.reply_text(
        text_data['notes_successfully_added'], 
        reply_markup=menu_markup)

    return CHOOSE

async def search_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        query = update.message.text 

        if not os.path.isfile(f'users_notes/{update.message.from_user["id"]}.txt'):
            await update.message.reply_text(
                text_data['notes_are_already_deleted'], 
                reply_markup=menu_markup)
            return CHOOSE
        
        with open(f"users_notes/{update.message.from_user['id']}.txt", "r", encoding='utf-8') as file:
            raw_notes = file.readlines()

        notes = dict()
        for i, j in enumerate(raw_notes):
            notes[i] = j

        norm_notes = nomalize(notes)
        norm_query = nomalize(query, mode='query')
        grouped_notes = get_texts_group(norm_query, norm_notes, number_of_topics=10)
        tf_idf = getTFIDFWidthFromNotes(norm_query, grouped_notes)
        ids_d = getRelevantNotesByTFIDF(tf_idf)
        ids = list(map(lambda x: x['notes'], ids_d))

        reply_message = ""
        for i, j in enumerate(ids):
            reply_message += f"{i+1}. " + notes[j]
        
        await update.message.reply_text(
            text_data['search_message'] + "\n\n" + reply_message, 
            reply_markup=menu_markup,
        )
    except:
        await update.message.reply_text(
            text_data['error_message'], 
            reply_markup=menu_markup,
        )
    return CHOOSE


async def delete_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if os.path.isfile(f'users_notes/{update.message.from_user["id"]}.txt'):
        os.remove(f'users_notes/{update.message.from_user["id"]}.txt')
        reply_message = text_data["notes_successfully_deleted"]
    
    else:
        reply_message = text_data["notes_are_already_deleted"]

    await update.message.reply_text(
        reply_message,
        reply_markup=menu_markup,
    )

    return CHOOSE

    
async def add_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == None:
        if update.message.document.file_name[-4:] != ".txt":
            await update.message.reply_text(text_data['wrong_file_format'], reply_markup=menu_markup)
            return CHOOSE
        if update.message.document.file_size > 1024*1024*3:
            await update.message.reply_text(text_data['file_is_too_big'], reply_markup=menu_markup)
            return CHOOSE

        notes_file = await context.bot.get_file(update.message.document.file_id)
        await notes_file.download_to_drive(f"users_notes/temp_{update.message.from_user['id']}.txt")
        with open(f"users_notes/temp_{update.message.from_user['id']}.txt", 'r', encoding="utf-8") as temp_file:
            notes = temp_file.read().rstrip()

    else:
        notes = update.message.text.rstrip()

    if len(notes.split("\n")) < 3:
        if os.path.isfile(f'users_notes/temp_{update.message.from_user["id"]}.txt'):
            os.remove(f'users_notes/temp_{update.message.from_user["id"]}.txt')
        await update.message.reply_text(text_data['little_notes'], reply_markup=menu_markup)
        return CHOOSE

    if not os.path.isfile(f'users_notes/{update.message.from_user["id"]}.txt'):
        text_data["add_keyboard_edited"] = [text_data["add_keyboard"][0]]
    else:
        text_data["add_keyboard_edited"] = text_data["add_keyboard"]
    
    with open(f"users_notes/temp_{update.message.from_user['id']}.txt", "w", encoding="utf-8") as file:
        file.write(notes)

    await update.message.reply_text(
        text_data['how_to_save_notes'], 
        reply_markup=ReplyKeyboardMarkup(text_data['add_keyboard_edited'], one_time_keyboard=True),
    )

    return SAVE

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE: [
                MessageHandler(
                    filters.Regex("^Добавить заметки$"), add_message
                ),
                MessageHandler(filters.Regex("^Поиск по заметкам$"), search_message),
                MessageHandler(filters.Regex("^Удалить мои заметки$"), delete_notes),
            ],
            ADD: [
                MessageHandler(
                    (filters.TEXT | filters.ATTACHMENT) & ~(filters.COMMAND), add_notes),
            ],
            SAVE: [
                MessageHandler(filters.Regex("^(Добавить заметки в новый список|Добавить заметки в существующий список)$"), save_notes),
            ],
            SEARCH: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND), search_notes),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)]
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
