from datetime import datetime


import vk_api, requests, os
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

from config import token_group
from VK import vk_sercher
from database import ORM



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

def attach(data, peer_id):

    attachments = []
    for foto in [data.foto1, data.foto2, data.foto3]:
        p = requests.get(foto)
        out = open("img.jpg", "wb")
        out.write(p.content)
        out.close()
        upload = VkUpload(vk_session)
        photo = upload.photo_messages("img.jpg", peer_id=peer_id)
        attachments.append(f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}_{photo[0]["access_key"]}')
        os.remove("img.jpg")
    return ','.join(attachments)

def get_offer(user_vk_id, n=1):
    vk_serch = vk_sercher.VKsercher()
    offer = ORM.get_condidat(n)
    if offer is None:
        sender(user_vk_id, 'Идет обработка, подождите ....')
        vk_serch.search(*ORM.get_serch_data(user_vk_id), offset=n)
        vk_serch.get_photo()
        for cand_id, data in (vk_serch.data_dict.items()):
            ORM.add_candidat(cand_id, data, user_vk_id)
            return get_offer(user_vk_id, n - 2)
        # TODO check logic
    if offer.condidate_id in ORM.get_block(ORM.get_user_id_bd(user_vk_id)):
        return get_offer(user_vk_id, n + 1)
    else:
        return (offer, n )


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

                vk_serch.search(*ORM.get_serch_data(id))
                vk_serch.get_photo()
                for cand_id, data in (vk_serch.data_dict.items()):
                    ORM.add_candidat(cand_id, data, id)
                ret = get_offer(id, n)
                offer = ret[0]
                n = ret[1]
                sender(id, f'{offer.name}\nhttps://vk.com/id{offer.condidate_vk_id}', keyboard(2), attachments=attach(offer,id) )

            if msg == 'следущий':
                ret = get_offer(id, n + 1)
                offer = ret[0]
                n = ret[1]

                sender(id, f'{offer.name}\nhttps://vk.com/id{offer.condidate_vk_id}', keyboard(2),
                       attachments=attach(offer, id))


            if msg == 'в избранное':
                ORM.add_favorit(offer.condidate_vk_id)
                sender(id, f'Пользователь {offer.name} добавлен в избранное', keyboard(2))
                ret = get_offer(id, n + 1)
                offer = ret[0]
                n = ret[1]

                sender(id, f'{offer.name}\nhttps://vk.com/id{offer.condidate_vk_id}', keyboard(2),
                       attachments=attach(offer, id))
                # n += 1

            if msg == 'в черный список':
                ORM.add_block(offer.condidate_vk_id)
                sender(id, f'Пользователь {offer.name} добавлен в черный список', keyboard(2))
                ret = get_offer(id, n + 1)
                offer = ret[0]
                n = ret[1]

                sender(id, f'{offer.name}\nhttps://vk.com/id{offer.condidate_vk_id}', keyboard(2),
                       attachments=attach(offer, id))
                # n += 1

            if msg == 'показать избранное':
                sender(id, 'Пока так не уменю2, но скоро научусь', keyboard(2))

if __name__ == '__main__':
    # ORM.create_bd()
    main()
