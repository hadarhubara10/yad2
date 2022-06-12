from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
# Craete buttons
test = []
test2 = []
for i in range(10):
    if len(test2) == 3:
        test.append(test2)
        test2 = []
    test2.append(InlineKeyboardButton(i, callback_data=i)),
print(test)
