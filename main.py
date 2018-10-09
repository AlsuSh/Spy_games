import urllib3
import requests
import time
import json
from pprint import pprint


class User:

    def __init__(self, token, source_uid):
        self.token = token
        self.source_uid = source_uid

    def get_friends(self):
        params = {'access_token': self.token,
                  'user_id': self.source_uid,
                  'fields': 'nickname',
                  'v': '5.85'}
        response = requests.get('https://api.vk.com/method/friends.get', params, verify=False)
        return response.json()['response']

    def get_groups(self, user_id=None):
        if user_id is None:
            user_id = self.source_uid
        try:
            params = {'access_token': self.token,
                      'user_id': user_id,
                      'extended': 1,
                      'fields': 'members_count',
                      'v': '5.85'}
            response = requests.get('https://api.vk.com/method/groups.get', params, verify=False, timeout=30)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        else:
            result = response.json()
            if 'error' in result:
                if result['error']['error_code'] == 6:  # Too many requests per second
                    time.sleep(0.5)
                    return self.get_groups(user_id)
                else:
                    return {'items': []}
            else:
                return result['response']

    def get_exclusive_groups(self):
        groups_response = self.get_groups(self.source_uid)
        groups = groups_response['items']
        friends_response = self.get_friends()
        friends = friends_response['items']

        groups_list = [i['id'] for i in groups]
        group_friends_count = dict.fromkeys(groups_list, 0)
        result = []
        for friend in friends:
            print(friend)
            friend_groups_response = self.get_groups(friend['id'])
            friend_groups = friend_groups_response['items']
            for group in friend_groups:
                if group['id'] in group_friends_count.keys():
                    group_friends_count[group['id']] += 1
        for group in groups:
            if group_friends_count[group['id']] == 0:
                result.append(group)
        return result


def groups_format(groups):
    result = []
    for group in groups:
        result.append({'name': group['name'],
                       'gid': group['id'],
                       'members_count': group['members_count']})
    return result


def save_to_file(data, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    TOKEN = "ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae"
    # source_uid = 171691064
    int(input('Введите идентификатор пользователя: '))
    usr = User(TOKEN, source_uid)
    groups = usr.get_exclusive_groups()
    groups_result = groups_format(groups)
    save_to_file(groups_result, 'groups.json')
    pprint(groups_result)
