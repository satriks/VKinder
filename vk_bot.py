from datetime import datetime
from time import sleep

import vk_api, requests, os
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

from config import token_group
from VK import vk_sercher
from database import ORM
import  asyncio



vk_session = vk_api.VkApi(token=token_group)
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)


def sender(id, text, keybord=None, attachments=None):
    post = {'user_id': id, 'message': text, 'random_id': 0 }
    if keybord != None:
        post['keyboard'] = keybord.get_keyboard()
    if attachments:
        post['attachment'] = attachments
    vk_session.method('messages.send', post)

def like_keyboard():
    like_keybord = VkKeyboard(one_time=False, inline=True)
    like_keybord.add_button('Фото1', VkKeyboardColor.POSITIVE)
    like_keybord.add_button('Фото2', VkKeyboardColor.POSITIVE)
    like_keybord.add_button('Фото3', VkKeyboardColor.POSITIVE)

    return like_keybord

def keyboard(first=1):
    keybord = VkKeyboard(one_time=False, inline=False)
    if first == 1:
        keybord.add_button('Подобрать', VkKeyboardColor.PRIMARY)
    else:
        keybord.add_button('Следущий', VkKeyboardColor.PRIMARY)
    keybord.add_button('Показать избранное', VkKeyboardColor.SECONDARY)
    keybord.add_line()
    keybord.add_button('В избранное', VkKeyboardColor.POSITIVE)
    keybord.add_button('Больше не показывать', VkKeyboardColor.NEGATIVE)
    return keybord

def attach(data, peer_id):

    attachments = []
    for foto in [data.foto1, data.foto2, data.foto3]:
        try:
            p = requests.get(foto)
            out = open("img.jpg", "wb")
            out.write(p.content)
            out.close()
            upload = VkUpload(vk_session)
            photo = upload.photo_messages("img.jpg", peer_id=peer_id)
            attachments.append(f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}_{photo[0]["access_key"]}')
            os.remove("img.jpg")
        except requests.exceptions.MissingSchema:
            print('Для отладки requests.exceptions.MissingSchema')
            continue
        except vk_api.exceptions.ApiError:
            print('Для отладки vk_api.exceptions.ApiError')
            continue
    return ','.join(attachments)

def fill_bd(id, offset=0):
    vk_serch = vk_sercher.VKsercher()
    vk_serch.search(*ORM.get_serch_data(id), offset=offset)
    vk_serch.get_photo()
    for cand_id, data in (vk_serch.data_dict.items()):
        ORM.add_candidat(cand_id, data, id)

def check( user_vk_id, n):
    if abs(n - ORM.last_id()) < 10:
        fill_bd(user_vk_id, n+50)
        sleep(3)
        print('fill отладка')


def get_offer(user_vk_id, n=1):

    offer = ORM.get_condidat(n)

    if offer is None:
        sender(user_vk_id, 'Идет обработка, подождите ....')
        fill_bd(user_vk_id, n +30)
        return get_offer(user_vk_id, n + 1)
    else:
        if offer.condidate_id in ORM.get_block(ORM.get_user_id_bd(user_vk_id)):
            return get_offer(user_vk_id, n + 1)
        else:
            check(user_vk_id, n)
            return (offer, n)


def main():
    vk_serch = vk_sercher.VKsercher()
    n = 1
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            id = event.user_id
            user_data = vk_serch.get_user_info(id)
            count_age = datetime.now().year - int(user_data['bdate'].split('.')[-1])
            ORM.add_user(vk_id=user_data['id'], age=count_age, city=user_data['city']['title'], sex=user_data['sex'])
            if msg == 'привет':
                sender(id, 'Начнем ?', keyboard())

            if msg == 'подобрать':
                sender(id, 'Идет обработка, подождите ....')

                fill_bd(id)

                res = get_offer(id, n)
                offer = res[0]
                n = res[1]
                sender(id, f'{offer.name}\nhttps://vk.com/id{offer.condidate_vk_id}', keyboard(2), attachments=offer.foto1 + ',' + offer.foto2 + ',' + offer.foto3 )
                sender(id, f'поставить лайк?', like_keyboard())

            if msg == 'следущий':
                res = get_offer(id, n + 1)
                offer = res[0]
                n = res[1]

                # sender(id, f'{offer.name}\nhttps://vk.com/id{offer.condidate_vk_id}', keyboard(2),
                #        attachments=attach(offer, id))
                sender(id, f'{offer.name}\nhttps://vk.com/id{offer.condidate_vk_id}', keyboard(2),
                       attachments=offer.foto1 + ',' + offer.foto2 + ',' + offer.foto3)
                sender(id, f'поставить лайк?', like_keyboard())




            if msg == 'в избранное':
                ORM.add_favorit(offer.condidate_vk_id)
                sender(id, f'Пользователь {offer.name} добавлен в избранное {"*" * 35}', keyboard(2))
                res = get_offer(id, n + 1)
                offer = res[0]
                n = res[1]

                sender(id, f'{offer.name}\nhttps://vk.com/id{offer.condidate_vk_id}', keyboard(2),
                       attachments=offer.foto1 + ',' + offer.foto2 + ',' + offer.foto3)
                sender(id, f'поставить лайк?', like_keyboard())
                # n += 1

            if msg == 'больше не показывать':
                ORM.add_block(offer.condidate_vk_id)
                sender(id, f'Пользователь {offer.name} добавлен в черный список \n{("*" * 35)}', keyboard(2))
                res = get_offer(id, n + 1)
                offer = res[0]
                n = res[1]

                sender(id, f'{offer.name}\nhttps://vk.com/id{offer.condidate_vk_id}', keyboard(2),
                       attachments=offer.foto1 + ',' + offer.foto2 + ',' + offer.foto3)
                sender(id, f'поставить лайк?', like_keyboard())
                # n += 1

            if msg == 'показать избранное':
                text = '\n'.join(list(map(str,(ORM.get_favorit(ORM.get_user_id_bd(id)))))).replace('Link', 'Профиль')
                sender(id, text, keyboard(2))

            if msg == 'фото1':
                data_foto = offer.foto1.split('_')
                if vk_serch.add_like(data_foto[0].replace('photo',''), data_foto[1]):
                    sender(id, f'Лайк для фото1 отправлен')
            if msg == 'фото2':
                data_foto = offer.foto2.split('_')
                if vk_serch.add_like(data_foto[0].replace('photo',''), data_foto[1]):
                    sender(id, f'Лайк для фото2 отправлен')
            if msg == 'фото3':
                data_foto = offer.foto3.split('_')
                if vk_serch.add_like(data_foto[0].replace('photo',''), data_foto[1]):
                    sender(id, f'Лайк для фото3 отправлен')

            print(n)
if __name__ == '__main__':
    # ORM.create_bd()
    main()
    # ORM.get_favorit(1)