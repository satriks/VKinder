import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from config import token_group
from pprint import pprint

vk = vk_api.VkApi(token=token_group)

longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})


def info_user(id_user):
    user_info = vk.method('users.get', {'user_ids': id_user, 'fields': ['sex', 'bdate', 'city',]})
    pprint(user_info)
    # тут есть подводные камни, у пользователя может быть скрыт город или не указан, а также день рождения скрыт
    # могу предложить что бы можно было попросить пользователя написать город,
    # а так же если нет дня рождения то попросить указать возраст
    return user_info


if __name__ == '__main__':

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                user = info_user(event.user_id)
                #тут думаю надо сначало проверить на наличие пользователя в базе
                #далее если пользователя нет, то занести, вызвать vk_search, и предложить варианты штуки 3
                #если есть в базе то сразу из базы выдернуть и предлагать
                request = event.text
                if request == "пока":
                    write_msg(event.user_id, "Пока((")
                elif request == "привет":
                    write_msg(event.user_id, "Привет")
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")
