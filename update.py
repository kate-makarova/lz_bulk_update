import re

from moder_bot import ModerBot


def update_text(text):
    pattern = 'https://wildcross.rusff.me'
    text = text.replace(pattern, "")

    pattern = 'http://wildcross.rusff.me'
    text = text.replace(pattern, "")
    return text

bot = ModerBot()
user_list = bot.parse_user_list()

for user in user_list:
    bot.profile_field_update(user[1], 2, update_text)