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
from get_code_of_manufacturer import get_code_of_engine_type, get_code_of_manufacturer,get_code_of_owner,get_engine_type_json,get_code_of_seats,get_code_of_gear_box,get_code_of_colors,get_code_of_hand
from methods import check_if_clicked, make_unclicked, edit_filtered_message
from pyrogram.types import Message
from pyrogram.errors import PeerFlood
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
        InlineKeyboardButton('יד', callback_data='hand'),
    ],
    [
        InlineKeyboardButton('קילומטראז', callback_data='kilometers'),
        InlineKeyboardButton('תיבת הילוכים', callback_data='gear_box'),
        InlineKeyboardButton('צבע', callback_data='colors'),
    ],
    [
        InlineKeyboardButton('בעלות', callback_data='ownership'),
        InlineKeyboardButton('סוג מנוע', callback_data='engine_type'),
        InlineKeyboardButton('מקומות', callback_data='seats'),
    ],
    [InlineKeyboardButton('בצע חיפוש 👀', callback_data='scan')],
    [InlineKeyboardButton('אפס סינון 🔄', callback_data='resetfilters'),
     InlineKeyboardButton('תפריט ראשי', callback_data='backtomain')],
]
OWNERS_BUTTONS = [
     [
        InlineKeyboardButton('פרטית', callback_data='פרטית'),
        InlineKeyboardButton('חברה', callback_data='חברה'),
        InlineKeyboardButton('ליסינג', callback_data='ליסינג'),
    ],
     [
        InlineKeyboardButton('השכרה', callback_data='השכרה'),
        InlineKeyboardButton('מונית', callback_data='מונית'),
        InlineKeyboardButton('ייבוא אישי', callback_data='ייבוא אישי'),
    ],
    [
        InlineKeyboardButton(
            'סיימתי לבחור', callback_data='ownership_done'),
    ],

]
ENGINE_TYPE_BUTTONS = [
     [
        InlineKeyboardButton('בנזין', callback_data='בנזין'),
        InlineKeyboardButton('דיזל', callback_data='דיזל'),
        InlineKeyboardButton('חשמלי', callback_data='חשמלי'),
    ],
     [
        InlineKeyboardButton('טורבו דיזל', callback_data='טורבו דיזל'),
        InlineKeyboardButton('היברידי חשמל / בנזין', callback_data='היברידי חשמל / בנזין'),
        InlineKeyboardButton('היברידי חשמל / דיזל', callback_data='היברידי חשמל / דיזל'),
    ],
    [
        InlineKeyboardButton(
            'סיימתי לבחור', callback_data='engine_type_done'),
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
SEATS_BUTTONS = [
    [
        InlineKeyboardButton('1', callback_data='1'),
        InlineKeyboardButton('2', callback_data='2'),
        InlineKeyboardButton('3', callback_data='3'),
    ],
    [
        InlineKeyboardButton('4', callback_data='4'),
        InlineKeyboardButton("5", callback_data="5"),
        InlineKeyboardButton('6', callback_data='6'),
    ],
    [
        InlineKeyboardButton('7', callback_data='7'),
        InlineKeyboardButton('8', callback_data='8'),
        InlineKeyboardButton('9', callback_data='9'),
    ],
    [
        InlineKeyboardButton('10', callback_data='10'),
        InlineKeyboardButton('11', callback_data='11'),
        InlineKeyboardButton('12', callback_data='12'),
    ],
    [
        InlineKeyboardButton(
            'סיימתי לבחור', callback_data='seats_done'),
    ],
]
GEAR_BOX_BUTTONS = [
    [
        InlineKeyboardButton('ידנית', callback_data='ידנית'),
        InlineKeyboardButton('אוטומט', callback_data='אוטומט'),
    ],
    [
        InlineKeyboardButton('רובוטית', callback_data='רובוטית'),
        InlineKeyboardButton('טיפטרוניק', callback_data='טיפטרוניק'),
    ],
    [
        InlineKeyboardButton(
            'סיימתי לבחור', callback_data='gear_box_done'),
    ],
]
COLORS_BUTTONS = [
    [
        InlineKeyboardButton('אדום', callback_data='אדום'),
        InlineKeyboardButton('אפור', callback_data='אפור'),
        InlineKeyboardButton('ורוד', callback_data='ורוד'),
    ],
    [
        InlineKeyboardButton('חום', callback_data='חום'),
        InlineKeyboardButton("ירוק", callback_data="ירוק"),
        InlineKeyboardButton('כחול', callback_data='כחול'),
    ],
    [
        InlineKeyboardButton('כתום', callback_data='כתום'),
        InlineKeyboardButton('לבן', callback_data='לבן'),
        InlineKeyboardButton('סגול', callback_data='סגול'),
    ],
    [
        InlineKeyboardButton('צהוב', callback_data='צהוב'),
        InlineKeyboardButton('שחור', callback_data='שחור'),
    ],
    [
        InlineKeyboardButton(
            'סיימתי לבחור', callback_data='colors_done'),
    ],
]
HAND_BUTTONS = [
    [
        InlineKeyboardButton('מיבואן', callback_data='מיבואן'),
        InlineKeyboardButton('יד ראשונה', callback_data='יד ראשונה'),
        InlineKeyboardButton('יד שניה', callback_data='יד שניה'),
    ],
    [
        InlineKeyboardButton('יד שלישית', callback_data='יום שלישית'),
        InlineKeyboardButton("יד רביעית", callback_data="יד רביעית"),
        InlineKeyboardButton('יד חמישית', callback_data='יד חמישית'),
    ],
    [
        InlineKeyboardButton('יד שישית', callback_data='יד שישית'),
        InlineKeyboardButton('יד שביעית', callback_data='יד שביעית'),
        InlineKeyboardButton('יד שמינית', callback_data='יד שמינית'),
    ],
    [
        InlineKeyboardButton('יד תשיעית', callback_data='יד תשיעית'),
        InlineKeyboardButton('יד עשירית+', callback_data='יד עשירית+'),
    ],
    [
        InlineKeyboardButton(
            'סיימתי לבחור', callback_data='hand_done'),
    ],
]
FAVORITES_BUTTONS = [
        InlineKeyboardButton('תפריט ראשי', callback_data='backtomain'),
    ],
# Running bot
app = Client('Yad2Testbot', api_id=APP_ID,
             api_hash=API_HASH, bot_token=BOT_TOKEN)
user_choices = {
    "manufacturer": [],
    "owners": [],
    "engine_type" : [],
    "seats" : [],
    "gearBox" : [],
    "hand" : [],
    "colors" : []
}

# Start
@app.on_message(filters.command('start') & filters.private)
async def start(client, message):
    await message.reply_text("היי וברוכים הבאים לבוט שיעזור לכם למצוא מציאות בתחום הרכבים ביד 2😊", reply_markup=InlineKeyboardMarkup(START_BUTTONS))


@app.on_callback_query()
async def _callbacks(client, cb: CallbackQuery):
    print(cb.data)
    if cb.data == 'carscanfilters':
        await cb.message.edit_text("כאן תוכל לבחור את המסננים בחיפוש הרכב בו אתה מעוניין ", reply_markup=InlineKeyboardMarkup(CAR_SCAN_FILTERS_BUTTONS))
        
    if cb.data == 'favorites':
        await cb.message.edit_text("כאן יוצגו כל המודעות ששמרת",  reply_markup=InlineKeyboardMarkup(FAVORITES_BUTTONS))
    if cb.data == 'backtomain':
        await cb.message.edit_text("היי וברוכים הבאים לבוט שיעזור לכם למצוא מציאות בתחום הרכבים ביד 2😊", reply_markup=InlineKeyboardMarkup(START_BUTTONS))
    if cb.data == 'manufacturer':
        await cb.message.edit_text("בבקשה בחר את היצרנים בהם אתה מעוניין", reply_markup=InlineKeyboardMarkup(MANUFACTURER_BUTTONS))
    if cb.data == 'engine_type':
        await cb.message.edit_text("בבקשה בחר את סוגי המנועים בהם אתה מעוניין", reply_markup=InlineKeyboardMarkup(ENGINE_TYPE_BUTTONS))
    if cb.data == 'ownership':
        await cb.message.edit_text("בבקשה בחר את הבעלויות בהן אתה מעוניין", reply_markup=InlineKeyboardMarkup(OWNERS_BUTTONS))
    if cb.data == 'seats':
        await cb.message.edit_text("בבקשה בחר את מספר המקומות בהם אתה מעוניין", reply_markup=InlineKeyboardMarkup(SEATS_BUTTONS))
    if cb.data == 'gear_box':
        await cb.message.edit_text("בבקשה בחר את תיבות ההילוכים בהם אתה מעוניין", reply_markup=InlineKeyboardMarkup(GEAR_BOX_BUTTONS))
    if cb.data == 'colors':
        await cb.message.edit_text("בבקשה בחר את הצבעים בהם אתה מעוניין", reply_markup=InlineKeyboardMarkup(COLORS_BUTTONS))
    if cb.data == 'hand':
        await cb.message.edit_text("בבקשה בחר את היד בה אתה מעוניין", reply_markup=InlineKeyboardMarkup(HAND_BUTTONS))
   
    if cb.data == 'hand_done':
        if not len(user_choices["hand"]) == 0:
            CAR_SCAN_FILTERS_BUTTONS[1][2] = check_if_clicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[1][2], 'hand')
        else:
            CAR_SCAN_FILTERS_BUTTONS[1][2] = make_unclicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[1][2], 'hand')
        await cb.message.edit_text(edit_filtered_message(user_choices), reply_markup=InlineKeyboardMarkup(CAR_SCAN_FILTERS_BUTTONS))    
    if not cb.data =='hand_done': 
        for i in range(len(HAND_BUTTONS)):
            for index, s in enumerate(HAND_BUTTONS[i]):
                if cb.data == s.callback_data:

                    if not get_code_of_hand(cb.data) in user_choices["hand"]:
                        if len(user_choices["hand"]) < 4:
                            user_choices["hand"].append(
                                get_code_of_hand(cb.data))
                            HAND_BUTTONS[i][index] = check_if_clicked(
                                s, HAND_BUTTONS[i][index], cb.data)
                            print(user_choices)
                    elif get_code_of_hand(cb.data) in user_choices["hand"]:
                        user_choices["hand"].remove(
                            get_code_of_hand(cb.data))
                        HAND_BUTTONS[i][index] = make_unclicked(
                            s, HAND_BUTTONS[i][index], cb.data)
                        print(user_choices)

                    await cb.message.edit_text("בבקשה בחר את היד בה אתה מעוניין", reply_markup=InlineKeyboardMarkup(HAND_BUTTONS))  
    if cb.data == 'colors_done':
        if not len(user_choices["colors"]) == 0:
            CAR_SCAN_FILTERS_BUTTONS[2][2] = check_if_clicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[2][2], 'colors')
        else:
            CAR_SCAN_FILTERS_BUTTONS[2][2] = make_unclicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[2][2], 'colors')
        await cb.message.edit_text(edit_filtered_message(user_choices), reply_markup=InlineKeyboardMarkup(CAR_SCAN_FILTERS_BUTTONS))    
    if not cb.data =='colors_done': 
        for i in range(len(COLORS_BUTTONS)):
            for index, s in enumerate(COLORS_BUTTONS[i]):
                if cb.data == s.callback_data:

                    if not get_code_of_colors(cb.data) in user_choices["colors"]:
                        if len(user_choices["colors"]) < 4:
                            user_choices["colors"].append(
                                get_code_of_colors(cb.data))
                            COLORS_BUTTONS[i][index] = check_if_clicked(
                                s, COLORS_BUTTONS[i][index], cb.data)
                            print(user_choices)
                    elif get_code_of_colors(cb.data) in user_choices["colors"]:
                        user_choices["colors"].remove(
                            get_code_of_colors(cb.data))
                        COLORS_BUTTONS[i][index] = make_unclicked(
                            s, COLORS_BUTTONS[i][index], cb.data)
                        print(user_choices)

                    await cb.message.edit_text("בבקשה בחר את הצבעים בהם אתה מעוניין", reply_markup=InlineKeyboardMarkup(COLORS_BUTTONS))  
    if cb.data == 'gear_box_done':
        if not len(user_choices["gearBox"]) == 0:
            CAR_SCAN_FILTERS_BUTTONS[2][1] = check_if_clicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[2][1], 'gear_box')
        else:
            CAR_SCAN_FILTERS_BUTTONS[2][1] = make_unclicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[2][1], 'gear_box')
        await cb.message.edit_text(edit_filtered_message(user_choices), reply_markup=InlineKeyboardMarkup(CAR_SCAN_FILTERS_BUTTONS))    
    if not cb.data =='gear_box_done': 
        for i in range(len(GEAR_BOX_BUTTONS)):
            for index, s in enumerate(GEAR_BOX_BUTTONS[i]):
                if cb.data == s.callback_data:

                    if not get_code_of_gear_box(cb.data) in user_choices["gearBox"]:
                        if len(user_choices["gearBox"]) < 4:
                            user_choices["gearBox"].append(
                                get_code_of_gear_box(cb.data))
                            GEAR_BOX_BUTTONS[i][index] = check_if_clicked(
                                s, GEAR_BOX_BUTTONS[i][index], cb.data)
                            print(user_choices)
                    elif get_code_of_gear_box(cb.data) in user_choices["gearBox"]:
                        user_choices["gearBox"].remove(
                            get_code_of_gear_box(cb.data))
                        GEAR_BOX_BUTTONS[i][index] = make_unclicked(
                            s, GEAR_BOX_BUTTONS[i][index], cb.data)
                        print(user_choices)

                    await cb.message.edit_text("בבקשה בחר את תיבות ההילוכים בהם אתה מעוניין", reply_markup=InlineKeyboardMarkup(GEAR_BOX_BUTTONS))  
    if cb.data == 'seats_done':
        if not len(user_choices["seats"]) == 0:
            CAR_SCAN_FILTERS_BUTTONS[3][2] = check_if_clicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[3][2], 'seats')
        else:
            CAR_SCAN_FILTERS_BUTTONS[3][2] = make_unclicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[3][2], 'seats')
        await cb.message.edit_text(edit_filtered_message(user_choices), reply_markup=InlineKeyboardMarkup(CAR_SCAN_FILTERS_BUTTONS))    
    if not cb.data =='seats_done': 
        for i in range(len(SEATS_BUTTONS)):
            for index, s in enumerate(SEATS_BUTTONS[i]):
                if cb.data == s.callback_data:

                    if not get_code_of_seats(cb.data) in user_choices["seats"]:
                        if len(user_choices["seats"]) < 4:
                            user_choices["seats"].append(
                                get_code_of_seats(cb.data))
                            SEATS_BUTTONS[i][index] = check_if_clicked(
                                s, SEATS_BUTTONS[i][index], cb.data)
                            print(user_choices)
                    elif get_code_of_seats(cb.data) in user_choices["seats"]:
                        user_choices["seats"].remove(
                            get_code_of_seats(cb.data))
                        SEATS_BUTTONS[i][index] = make_unclicked(
                            s, SEATS_BUTTONS[i][index], cb.data)
                        print(user_choices)

                    await cb.message.edit_text("בבקשה בחר את סוגי המנועים בהם אתה מעוניין", reply_markup=InlineKeyboardMarkup(SEATS_BUTTONS))  
    if cb.data == 'engine_type_done':
        if not len(user_choices["engine_type"]) == 0:
            CAR_SCAN_FILTERS_BUTTONS[3][1] = check_if_clicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[3][1], 'engine_type')
        else:
            CAR_SCAN_FILTERS_BUTTONS[3][1] = make_unclicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[3][1], 'engine_type')
        await cb.message.edit_text(edit_filtered_message(user_choices), reply_markup=InlineKeyboardMarkup(CAR_SCAN_FILTERS_BUTTONS))    
    if not cb.data =='engine_type_done': 
        for i in range(len(ENGINE_TYPE_BUTTONS)):
            for index, s in enumerate(ENGINE_TYPE_BUTTONS[i]):
                if cb.data == s.callback_data:

                    if not get_code_of_engine_type(cb.data) in user_choices["engine_type"]:
                        if len(user_choices["engine_type"]) < 4:
                            user_choices["engine_type"].append(
                                get_code_of_engine_type(cb.data))
                            ENGINE_TYPE_BUTTONS[i][index] = check_if_clicked(
                                s, ENGINE_TYPE_BUTTONS[i][index], cb.data)
                            print(user_choices)
                    elif get_code_of_engine_type(cb.data) in user_choices["engine_type"]:
                        user_choices["engine_type"].remove(
                            get_code_of_engine_type(cb.data))
                        ENGINE_TYPE_BUTTONS[i][index] = make_unclicked(
                            s, ENGINE_TYPE_BUTTONS[i][index], cb.data)
                        print(user_choices)

                    await cb.message.edit_text("בבקשה בחר את סוגי המנועים בהם אתה מעוניין", reply_markup=InlineKeyboardMarkup(ENGINE_TYPE_BUTTONS))    
    if cb.data == 'ownership_done':
        if not len(user_choices["owners"]) == 0:
            CAR_SCAN_FILTERS_BUTTONS[3][0] = check_if_clicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[3][0], 'ownership')
        else:
            CAR_SCAN_FILTERS_BUTTONS[3][0] = make_unclicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[3][0], 'owners')
        await cb.message.edit_text(edit_filtered_message(user_choices), reply_markup=InlineKeyboardMarkup(CAR_SCAN_FILTERS_BUTTONS))
    if not cb.data =='ownership_done': 
        for i in range(len(OWNERS_BUTTONS)):
            for index, s in enumerate(OWNERS_BUTTONS[i]):
                if cb.data == s.callback_data:

                    if not get_code_of_owner(cb.data) in user_choices["owners"]:
                        if len(user_choices["owners"]) < 4:
                            user_choices["owners"].append(
                                get_code_of_owner(cb.data))
                            OWNERS_BUTTONS[i][index] = check_if_clicked(
                                s, OWNERS_BUTTONS[i][index], cb.data)
                            print(user_choices)
                    elif get_code_of_owner(cb.data) in user_choices["owners"]:
                        user_choices["owners"].remove(
                            get_code_of_owner(cb.data))
                        OWNERS_BUTTONS[i][index] = make_unclicked(
                            s, OWNERS_BUTTONS[i][index], cb.data)
                        print(user_choices)

                    await cb.message.edit_text("בבקשה בחר את הבעלויות בהן אתה מעוניין", reply_markup=InlineKeyboardMarkup(OWNERS_BUTTONS))
    if cb.data == 'manufacturer_done':
        if not len(user_choices["manufacturer"]) == 0:
            CAR_SCAN_FILTERS_BUTTONS[0][0] = check_if_clicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[0][0], 'manufacturer')
        else:
            CAR_SCAN_FILTERS_BUTTONS[0][0] = make_unclicked(
                cb.data, CAR_SCAN_FILTERS_BUTTONS[0][0], 'manufacturer')
        await cb.message.edit_text(edit_filtered_message(user_choices), reply_markup=InlineKeyboardMarkup(CAR_SCAN_FILTERS_BUTTONS))
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