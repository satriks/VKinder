from datetime import datetime

import vk_api

from settings.vk_config import vk_token_client


class VKsercher:
    def __init__(self):
        self.data_dict = {}
        self.vk_session = vk_api.VkApi(token=vk_token_client)
        self.vk = self.vk_session.get_api()

    def search(self, age, sex, city, offset=0):
        ''' Ищет пользователей, с открытым аком, по указанным параметрам
             Словарь id : Имя, примерный возраст '''

        offers = self.vk.users.search(
            sort=0,
            sex=sex,
            status=1,
            age_from=age - 5,
            age_to=age + 5,
            has_photo=1,
            count=50,
            online=0,
            hometown=city,
            is_closed=False,
            offset=offset,
            fields=('photo_max_orig', 'bdate')
        )

        for data in offers['items']:
            if data['is_closed'] == False:
                try:
                    age_format = list(map(int, data['bdate'].split('.')))
                    bday = datetime(age_format[2], age_format[1], age_format[0])
                    age = (datetime.now() - bday).days
                    self.data_dict[data['id']] = [data['first_name'] + ' ' + data['last_name']] + [age // 366]
                except:
                    continue

    def get_photo(self):
        ''' Добавляет в к найденным акайнтам 3 самы популярные их фото'''
        for id in self.data_dict:
            if len(self.data_dict.get(id)) > 2:
                continue
            else:
                photo = self.vk.photos.getAll(owner_id=id, photo_sizes=1, extended=1)
                self.data_dict[id] = self.data_dict.get(id) + (list(map(lambda x: x[1], (sorted(
                    [(x['likes']['count'], f'photo{x["owner_id"]}_{x["id"]}_{vk_token_client}') for x in
                     photo['items']])[-1:-4:-1]))))

    def get_user_info(self, id):
        '''Выводит данне о user др, город, пол '''
        user = self.vk.users.get(user_ids=id, fields=('bdate', 'city', 'sex'))
        return user[0]

    def add_like(self, owner_id, item_id):
        res = self.vk.likes.add(type='photo',
                                owner_id=owner_id,
                                item_id=item_id,
                                access_token=vk_token_client)
        if res['likes']:
            return 1
        else:
            return 0

    def check_like(self, owner_id, item_id):
        res = self.vk.likes.isLiked(type='photo',
                                    owner_id=owner_id,
                                    item_id=item_id,
                                    access_token=vk_token_client)
        return res['liked']

    def delete_like(self, owner_id, item_id):
        res = self.vk.likes.delete(type='photo',
                                   owner_id=owner_id,
                                   item_id=item_id,
                                   access_token=vk_token_client)
        if res['likes']:
            return 1
        else:
            return 0
