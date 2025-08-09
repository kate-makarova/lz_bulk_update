import re

from moder_bot import ModerBot


def update_text(text):
    pattern = 'https://wildcross.rusff.me'
    text = text.replace(pattern, "")

    pattern = 'http://wildcross.rusff.me'
    text = text.replace(pattern, "")
    return text

def put_dummy_text(text):
    return '<li class="pa-fld2"><a href="https://wildcross.rusff.me/viewtopic.php?id=1746#p118853" class="lz1">питер де врис</a>  Death doesn’t discriminate<br> Between <a href="http://wildcross.rusff.me/profile.php?id=594" class="lz2">the sinners and the saints</a><br> It takes and it takes and it takes<br> And we <a href="https://wildcross.rusff.me/profile.php?id=567" class="lz2">keep living anyway</a><br> We rise and we fall and we break<br> And we <a href="http://wildcross.rusff.me/profile.php?id=574" class="lz2">make our mistakes</a></li>'


bot = ModerBot()
bot.set_cookie()
user_list = bot.parse_user_list()

not_updated = []

for user in user_list:
    print('Updating ' + user[0] + '(user id: ' + str(user[1]) + ')')
    result = bot.profile_field_update(user[1], 2, update_text)
    if result == False:
        print ("Could not update profile")
        not_updated.append(user)

bot.quit()
print('')
print('Could not update:')
for user in not_updated:
    print(user[0] + '(user id: ' + str(user[1]) + ')')