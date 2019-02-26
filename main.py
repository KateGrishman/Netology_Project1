from json import dumps
import time

import requests

# https://oauth.vk.com/authorize?client_id=6865217&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52

token_code = ''
test_user_id = '171691064'


def api_get(method_name, p):
    params = {'access_token': token_code, 'version': 5.92}
    params.update(p)
    resp = requests.get(f'https://api.vk.com/method/{method_name}', params=params).json()
    if 'response' in resp:
        return resp['response']
    elif 'error' in resp and resp['error']['error_code'] == 6:
        print("Too many requests")
        time.sleep(1)
        return api_get(method_name, p)


def load_user_id(id_or_name):
    try:
        int(id_or_name)
        return id_or_name
    except ValueError:
        return api_get('users.get', {'screen_name': id_or_name, 'fields': ''})[0]['uid']


def load_user_groups(user_id):
    return api_get('users.getSubscriptions', {'user_id': user_id})['groups']['items']


def collect_secret_groups(group_ids):
    mystery_groups = []
    for group in group_ids:
        print(f'checking {group}...')
        count = api_get('groups.getMembers', {'group_id': group, 'filter': 'friends'})['count']
        if count == 0:
            mystery_groups.append(str(group))
        time.sleep(.5)
    return mystery_groups


def load_group_info(mystery_groups):
    group_info = api_get('groups.getById', {'group_ids': ','.join(mystery_groups), 'fields': 'name,members_count'})
    filtered_info = []
    for info in group_info:
        filtered_info.append({'name': info['name'], 'gid': info['gid'], 'members_count': info['members_count']})
    return filtered_info


def save_to_file(filtered_info, file_name='groups.json'):
    with open(file_name, 'w') as result_file:
        result_file.write(dumps(filtered_info, indent=2))


save_to_file(load_group_info(collect_secret_groups(load_user_groups(load_user_id(test_user_id)))))
