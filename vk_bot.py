import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

from config import token_group

vk_session = vk_api.VkApi(token=token_group)
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)


def sender(id, text, keybord=None):
    post = {'user_id': id, 'message': text, 'random_id': 0}
    if keybord != None:
        post['keyboard'] = keybord.get_keyboard()
    vk_session.method('messages.send', post)


def keyboard(first=1):
    keybord = VkKeyboard(one_time=False, inline=False)
    if first == 1:
        keybord.add_button('Подобрать', VkKeyboardColor.PRIMARY)
    else:
        keybord.add_button('Следущий', VkKeyboardColor.PRIMARY)
    keybord.add_button('Показать избранное', VkKeyboardColor.SECONDARY)
    keybord.add_line()
    keybord.add_button('В избранное', VkKeyboardColor.POSITIVE)
    keybord.add_button('В черный список', VkKeyboardColor.NEGATIVE)
    return keybord


def main():
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg == 'привет':
                sender(id, 'Начнем ?', keyboard())

            if msg == 'подобрать' or 'следущий':
                sender(id, 'Пока так не уменю, но скоро научусь', keyboard(2))
            if msg == 'показать избранное':
                sender(id, 'Пока так не уменю, но скоро научусь', keyboard(2))
            if msg == 'в избранное':
                sender(id, 'Пока так не уменю, но скоро научусь добавлять', keyboard(2))
            if msg == 'в черный список':
                sender(id, 'Пока так не уменю, но скоро научусь', keyboard(2))


if __name__ == '__main__':
    main()
