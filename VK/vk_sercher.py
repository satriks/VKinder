import vk_api, requests
from config import token_group, vk_token_client, id_group
from datetime import datetime, timedelta



# vk_session = vk_api.VkApi(token=token_client)
# vk = vk_session.get_api()

# def get_access_key():
#     driver = webdriver.Firefox()
#     driver.get(f'https://oauth.vk.com/authorize?client_id={id_group}&display=page&redirect_uri=https://oauth.vk.com/blank.html&response_type=token&v=5.131&v=5.131')
#     sleep(2000)

class VKsercher:
    def __init__(self):
        self.data_dict = {}
        self.vk_session = vk_api.VkApi(token=vk_token_client)
        self.vk = self.vk_session.get_api()

    def search(self, age, sex, city, offset=0):
        ''' Ищет пользователей, с открытым аком, по указанным параметрам
             Словарь id : Имя, примерный возраст '''
        offers = self.vk.users.search(
                                sort=0 ,
                                sex= sex,
                                status= 1,
                                age_from= age - 2,
                                age_to= age + 5 ,
                                has_photo= 1,
                                count= 50,
                                online= 0,
                                hometown= city,
                                is_closed= False,
                                offset = offset ,
                                fields=('photo_max_orig', 'bdate')
                               )

        for data in offers['items']:
            if data['is_closed'] == False:

                age_format =  list(map(int, data['bdate'].split('.')))
                bday = datetime(age_format[2], age_format[1], age_format[0])
                age = (datetime.now() -bday).days
                self.data_dict[data['id']] = [data['first_name'] + ' ' + data['last_name']] + [age // 366]

    def get_photo(self):
        ''' Добавляет в к найденным акайнтам 3 самы популярные их фото'''
        for id in self.data_dict:
            if len(self.data_dict.get(id)) > 2 :
                continue
            else:
                photo = self.vk.photos.getAll(owner_id=id, photo_sizes =1 , extended= 1)   # TODO подумать может переделать на photos.getById что бы на этом этапе получать id фото для атача
                self.data_dict[id] = self.data_dict.get(id) + (list(map(lambda x : x[1],(sorted([(x['likes']['count'], x['sizes'][-1]['url']  ) for x in photo['items']])[-1:-4:-1]))))

    # TODO Требует личный токен пользователя что бы показать где он отмечен
    # def get_photo_notice(self):
    #     ''' Добавляет в к найденным акайнтам 3 самы популярные их фото'''
    #     for id in self.data_dict:
    #         if len(self.data_dict.get(id)) > 5 :
    #             continue
    #         else:
    #             photo = self.vk.photos.getUserPhotos(user_id=id,  extended= 1 , sort = 0, count= 3)
    #             print(photo)
    #             break
                # self.data_dict[id] = self.data_dict.get(id) + (list(map(lambda x : x[1],(sorted([(x['likes']['count'], x['sizes'][-1]['url']  ) for x in photo['items']])[-1:-4:-1]))))

    def get_user_info(self, id):
        '''Выводит данне о user др, город, пол '''
        user = self.vk.users.get(user_ids=id, fields = ('bdate', 'city','sex') )
        return user[0]

    def access_token(self):
        pass

    def add_like(self):
        pass
        # TODO создать функцию для лайков

if __name__ == '__main__':
    serch = VKsercher()

    serch.search(30, 1, 'Москва', offset=70)
    # serch.get_user_info(1153507)
    serch.get_photo_notice()

    # serch.get_photo()
    # print(serch.data_dict)





# на потом

# def send_photo(vk, peer_id, owner_id, photo_id, access_key):
#     attachment = f'photo{owner_id}_{photo_id}_{access_key}'
#     vk.messages.send(
#         random_id=get_random_id(),
#         peer_id=peer_id,
#         attachment=attachment)
