import time
from json import dumps

import requests

# https://oauth.vk.com/authorize?client_id=6865217&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52

token_code = ''
user_id = '171691064'

user_groups = requests.get('https://api.vk.com/method/users.getSubscriptions',
                           params={'user_id': user_id, 'access_token': token_code, 'version': 5.92}).json()
group_ids = user_groups['response']['groups']['items']
# print(dumps(group_ids, indent=4))

get_friends_response = requests.get('https://api.vk.com/method/friends.get',
                                    params={'user_id': user_id, 'access_token': token_code, 'version': 5.92})
friend_ids = get_friends_response.json()['response']
# print(friend_ids)

mystery_groups = []
for group in group_ids:
    print(f'checking {group}...')
    count = requests.get('https://api.vk.com/method/groups.getMembers',
                         params={'group_id': group, 'filter': 'friends', 'access_token': token_code, 'version': 5.92}) \
        .json()['response']['count']
    if count == 0:
        mystery_groups.append(str(group))
    time.sleep(.5)

group_info = requests.get('https://api.vk.com/method/groups.getById',
                          params={'group_ids': ','.join(mystery_groups), 'fields': 'name,members_count',
                                  'access_token': token_code, 'version': 5.92}) \
    .json()['response']

filtered_info = []
for info in group_info:
    filtered_info.append({'name': info['name'], 'gid': info['gid'], 'members_count': info['members_count']})

with open('result.json', 'w') as result_file:
    result_file.write(dumps(filtered_info))
