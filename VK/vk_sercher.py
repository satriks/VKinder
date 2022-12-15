import vk_api
from config import token_group, token_client
from datetime import datetime, timedelta

# vk_session = vk_api.VkApi(token=token_client)
# vk = vk_session.get_api()

class VKsercher:
    def __init__(self):
        self.data_dict = {}
        self.vk_session = vk_api.VkApi(token=token_client)
        self.vk = self.vk_session.get_api()

    def search(self, age, sex, city, offset=0):
        ''' Ищет пользователей, с открытым аком, по указанным параметрам
        return Словарь id : Имя, примерный возраст '''
        offers = self.vk.users.search(
                                sort=0 ,
                                sex= sex,
                                status= 1,
                                age_from= age - 3,
                                age_to= age + 3,
                                has_photo= 1,
                                count= 100,
                                online= 1,
                                hometown= city,
                                is_closed= False,
                                offset = offset,
                                fields=('photo_max_orig', 'bdate')
                               )

        for data in offers['items']:
            if data['is_closed'] == False:

                age_format =  list(map(int, data['bdate'].split('.')))
                bday = datetime(age_format[2], age_format[1], age_format[0])
                age = (datetime.now() -bday).days
                self.data_dict[data['id']] = [data['first_name'] + ' ' + data['last_name']] + [age // 366]

    def get_photo(self):
        for id in self.data_dict:
            photo = self.vk.photos.getAll(owner_id=id, photo_sizes =1 , extended= 1)
            [print(photo['likes'] ) for _ in photo['items']]
            break

if __name__ == '__main__':
    serch = VKsercher()
    serch.search(30,1,'Москва',offset=10)
    # print(serch.data_dict)
    serch.get_photo()





# на потом

# def send_photo(vk, peer_id, owner_id, photo_id, access_key):
#     attachment = f'photo{owner_id}_{photo_id}_{access_key}'
#     vk.messages.send(
#         random_id=get_random_id(),
#         peer_id=peer_id,
#         attachment=attachment)
