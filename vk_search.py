import vk_api
from pprint import pprint
from config import token_client
import create_bd

VK_session = vk_api.VkApi(token=token_client)
VK = VK_session.get_api()

def add_datebase():
    create_bd.add_offer(name=None, age=None, male=None, city=None, foto=None, user_id=1)
    pass #вывод будет не возраст правда а день рождения и фото 3 шт



#необходима переменная с информацией пользователя что бы определить пол, возраст, город поиска
def search(age, sex, city):
    users = VK.users.search(age_from=age - 3, age_to=age + 2, sex=sex, fields=['sex', 'bdate', 'city', ], city_id=city, count=5)

    for person in users['items']:
        all_photos = VK.photos.getAll(owner_id=person['id'], extended=1)
        try:
            person['bdate'] and person['city']['id']
        except KeyError:
            continue
        else:
            save_photos = {}
            for photo in all_photos['items']:
                save_photos[photo['likes']['count']] = photo['sizes'][0]['url']
            likes_photo = sorted(list(save_photos.keys()))[-3:]
            #Учесть при загрузке в БД, что фото может и не быть 3 шт
            #Доработать так как при извлечении фото с приватных страниц код падает
            #Позже поправить выгрузку самой большой фото
            photos = []
            for photo in likes_photo:
                photos.append(save_photos[photo])
            print(person['first_name'], person['bdate'], person['sex'], person['city']['id'], photos)
            # add_datebase(person['first_name'], person['bdate'], person['sex'], person['city']['id'], photos)

search(25, 1, 2)



