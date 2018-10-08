import urllib3
import requests


class User:

    def __init__(self, token, source_uid):
        self.token = token
        self.source_uid = source_uid

    def get_friends(self):
        params = {'access_token': self.token,
                  'user_ids': self.source_uid,
                  'fields': 'nickname',
                  'v': '5.85'}
        response = requests.get('https://api.vk.com/method/friends.get', params, verify=False)
        return response.json()['response']

    def get_groups(self, user_id=None):
        if user_id is None:
            user_id = self.source_uid
        print(user_id)
        params = {'access_token': self.token,
                  'user_ids': user_id,
                  'extended': 1,
                  'fields': 'members_count',
                  'v': '5.85'}
        response = requests.get('https://api.vk.com/method/groups.get', params, verify=False)
        return response.json()['response']

    def get_exclusive_groups(self):
        groups_response = self.get_groups(self.source_uid)
        groups = groups_response['items']
        print(groups)
        friends_response = self.get_friends()
        friends = friends_response['items']
        groups_list = [i['id'] for i in groups]
        group_friends_count = dict.fromkeys(groups_list, 0)
        friend = friends[0]
        friend_groups_response = self.get_groups(friend['id'])
        friend_groups = friend_groups_response['items']
        print(friend_groups)

        # for friend in friends:
        #     friend_groups_response = self.get_groups(friend['id'])
        #     friend_groups = friend_groups_response['items']
        #     print(friend_groups)
        #     for group in friend_groups:
        #         if group['id'] in group_friends_count.keys():
        #             group_friends_count[group['id']] += 1


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    TOKEN = "ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae"
    source_uid = 7613322
    # int(input('Введите идентификатор пользователя: '))
    usr = User(TOKEN, source_uid)
    usr.get_exclusive_groups()



    # Внимание: и
    # имя
    # пользователя(eshmargunov)
    # и
    # id(171691064)