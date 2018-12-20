import settings
import pymysql
import requests
import time
import logs

access_token = settings.user['access_token']
session = requests.session()

def check_valid():
    response = session.get(
        'https://api.vk.com/method/account.getInfo',
        params={
            'access_token': access_token,
            'v': '5.92',
        }
    ).json()

    try:
        tmp = response['response']
        return True

    except:
        return False

def groupsGetMembers(group_id, offset):
    time.sleep(0.3)
    try:
        response = session.get(
            'https://api.vk.com/method/groups.getMembers',
            params={
                'v': '5.92',
                'access_token': access_token,
                'group_id': group_id,
                'sort': 'id_asc',
                'offset': offset,
                'count': 1000
            }
        ).json()

        return response['response']

    except:
        logs.echoWarning('Error, check if the group is private')
        exit(0)


def usersGetInfo(user_ids):
    time.sleep(0.3)
    user_ids = str(user_ids).replace('[', '').replace(']', '').replace("'", '')

    fields = 'contacts, sex, bdate, city, country, domain'

    response = session.get(
        'https://api.vk.com/method/users.get',
        params={
            'v': '5.92',
            'access_token': access_token,
            'user_ids': user_ids,
            'fields': fields
        }
    ).json()

    return response['response']

def stats(
    start_time,
    wrote,
    analyzed,
    members_count,
    did_not_indicate
):
    took_seconds = str(int(time.time() - start_time))
    took_minutes = str(int(took_seconds) / 60)
    print('-' * 59)

    print('Short stats:')
    print('Scanned users: ' + str(analyzed) + '/' + str(members_count))
    print('Took ' + took_seconds + ' seconds (' + took_minutes + ' minutes)')
    print('Added ' + str(wrote) + ' lines in db')
    print('Users did not indicate their mobile phone: ' + str(did_not_indicate))

    print('-' * 59)
    print('You can find dump in the table "' + settings.db['table_name'] + '"')
