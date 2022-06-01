# Configs
import json
import requests
import os
import shlex
import asyncio
import uuid
import shutil
from typing import Tuple
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from yad2_get_details import get_yad2_content,  getFilteredUrl
from get_code_of_manufacturer import get_code_of_manufacturer
from methods import check_if_clicked, make_unclicked, edit_filtered_message
# Configs
API_HASH = os.getenv('API_HASH')
APP_ID = os.getenv('APP_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')
# Buttons
START_BUTTONS = [
    [
        InlineKeyboardButton('חפש לי מציאה 🚙', callback_data='carscanfilters'),
    ],
    [
        InlineKeyboardButton('מודעות שסימנתי ב-⭐️', callback_data='favorites'),
    ],
    [
        InlineKeyboardButton('תמיכה טכנית 👨‍💻', url='https://t.me/xgorn')
    ],
]
ADS_BUTTONS = [
    [
        InlineKeyboardButton('למודעה הקודמת ⬅️', callback_data='previousad'),
    ],
    [
        InlineKeyboardButton('למודעה הבאה ➡️', callback_data='nextad'),
    ],
    [
        InlineKeyboardButton('הצג את המודעה המקורית ',
                             url='https://t.me/xgorn')
    ],

]
CAR_SCAN_FILTERS_BUTTONS = [
    [
        InlineKeyboardButton('יצרן', callback_data='manufacturer'),
        InlineKeyboardButton('דגם', callback_data='model'),
        InlineKeyboardButton('שנה', callback_data='yera'),
    ],
    [
        InlineKeyboardButton('מחיר', callback_data='price'),
        InlineKeyboardButton('אזור', callback_data='location'),
        InlineKeyboardButton('יד', callback_data='owners'),
    ],
    [
        InlineKeyboardButton('קילומטראז', callback_data='kilometers'),
        InlineKeyboardButton('תיבת הילוכים', callback_data='gearbox'),
        InlineKeyboardButton('צבע', callback_data='color'),
    ],
    [
        InlineKeyboardButton('בעלות', callback_data='ownership'),
        InlineKeyboardButton('סוג מנוע', callback_data='enginetype'),
        InlineKeyboardButton('מספר מקומות', callback_data='numofseats'),
    ],
    [InlineKeyboardButton('בצע חיפוש 👀', callback_data='scan')],
    [InlineKeyboardButton('אפס סינון 🔄', callback_data='resetfilters'),
     InlineKeyboardButton('תפריט ראשי', callback_data='backtomain')],
]
FAVORITES_BUTTONS = [
    [
        InlineKeyboardButton('תפריט ראשי', callback_data='backtomain'),
    ],
]
MANUFACTURER_BUTTONS = [
    [
        InlineKeyboardButton('מאזדה', callback_data='מאזדה'),
        InlineKeyboardButton('שברולט', callback_data='שברולט'),
        InlineKeyboardButton('קיה', callback_data='קיה'),
    ],
    [
        InlineKeyboardButton('טויוטה', callback_data='טויוטה'),
        InlineKeyboardButton("פיג'ו", callback_data="פיג'ו"),
        InlineKeyboardButton('סובארו', callback_data='סובארו'),
    ],
    [
        InlineKeyboardButton('סיטרואן', callback_data='סיטרואן'),
        InlineKeyboardButton('אופל', callback_data='אופל'),
        InlineKeyboardButton('מרצדס', callback_data='מרצדס'),
    ],
    [
        InlineKeyboardButton(
            'סיימתי לבחור', callback_data='manufacturer_done'),
    ],
]

# Running bot
app = Client('Yad2Testbot', api_id=APP_ID,
             api_hash=API_HASH, bot_token=BOT_TOKEN)
xbot = ""
user_choices = {
    "manufacturer": [],
    "owners": []
}


# Start
@app.on_message(filters.command('start') & filters.private)
async def start(client, message):
    await message.reply_text("היי וברוכים הבאים לבוט שיעזור לכם למצוא מציאות בתחום הרכבים ביד 2😊", reply_markup=InlineKeyboardMarkup(START_BUTTONS))


@app.on_callback_query()
async def _callbacks(client, cb: CallbackQuery):
    if cb.data == 'carscanfilters':
        await cb.message.edit_text("כאן תוכל לבחור את המסננים בחיפוש הרכב בו אתה מעוניין ", reply_markup=InlineKeyboardMarkup(CAR_SCAN_FILTERS_BUTTONS))
    if cb.data == 'favorites':
        await cb.message.edit_text("כאן יוצגו כל המודעות ששמרת",  reply_markup=InlineKeyboardMarkup(FAVORITES_BUTTONS))
    if cb.data == 'backtomain':
        await cb.message.edit_text("היי וברוכים הבאים לבוט שיעזור לכם למצוא מציאות בתחום הרכבים ביד 2😊", reply_markup=InlineKeyboardMarkup(START_BUTTONS))
    if cb.data == 'manufacturer':
        await cb.message.edit_text("בבקשה בחר את היצרנים בהם אתה מעוניין", reply_markup=InlineKeyboardMarkup(MANUFACTURER_BUTTONS))
    if cb.data == 'manufacturer_done':
        if not len(user_choices["manufacturer"]) == 0:
            CAR_SCAN_FILTERS_BUTTONS[0][0] = check_if_clicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[0][0], 'manufacturer')
        else:
            CAR_SCAN_FILTERS_BUTTONS[0][0] = make_unclicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[0][0], 'manufacturer')

        # await cb.message.edit_text("בחר מסננים נוספים, עד כה בחרת \n"+CAR_SCAN_FILTERS_BUTTONS[0][0].text.removesuffix("✅"), reply_markup=InlineKeyboardMarkup(CAR_SCAN_FILTERS_BUTTONS))
        await cb.message.edit_text(edit_filtered_message(user_choices), reply_markup=InlineKeyboardMarkup(CAR_SCAN_FILTERS_BUTTONS))

    # check if user has chosen manufacturers and append them to user_choices
    if not cb.data == 'manufacturer_done':
        for i in range(len(MANUFACTURER_BUTTONS)):
            for index, s in enumerate(MANUFACTURER_BUTTONS[i]):
                if cb.data == s.callback_data:

                    if not get_code_of_manufacturer(cb.data) in user_choices["manufacturer"]:
                        if len(user_choices["manufacturer"]) < 4:
                            user_choices["manufacturer"].append(
                                get_code_of_manufacturer(cb.data))
                            MANUFACTURER_BUTTONS[i][index] = check_if_clicked(
                                s, MANUFACTURER_BUTTONS[i][index], cb.data)
                            print(user_choices)
                    elif get_code_of_manufacturer(cb.data) in user_choices["manufacturer"]:
                        user_choices["manufacturer"].remove(
                            get_code_of_manufacturer(cb.data))
                        MANUFACTURER_BUTTONS[i][index] = make_unclicked(
                            s, MANUFACTURER_BUTTONS[i][index], cb.data)
                        print(user_choices)

                    await cb.message.edit_text("בבקשה בחר את היצרנים בהם אתה מעוניין", reply_markup=InlineKeyboardMarkup(MANUFACTURER_BUTTONS))

    if cb.data == 'scan':
        await cb.message.edit_text("מצאת את הרכב שלך בחיפוש הרכבים ביד 2😊", reply_markup=InlineKeyboardMarkup(START_BUTTONS))
        await cb.message.reply_text(getFilteredUrl(user_choices))


app.run()
