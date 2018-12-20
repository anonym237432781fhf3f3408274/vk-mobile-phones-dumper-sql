import functions as f
import logs
import settings
import time
from sys import argv
import sql

def main():
    vv = False

    if '--help' in argv or '-h' in argv:
        print\
("""
=== VK mobile phones dumper MySQL ==

-h  --help      :      show this help and exit
-v  --view      :      show logs while programm running
""")
        print('Usage: ' + argv[0] + '[group_id] [params]')
        print()
        print('Examples:')
        print()
        print(argv[0] + ' 123 -v')
        print(argv[0] + ' 456')

        exit(0)

    if len(argv) < 2:
        logs.echoInfo('Usage: [group_id] [params]')
        logs.echoInfo('Example: ' + argv[0] + ' 1234567 -v')
        exit(0)

    if '-v' in argv or '--view' in argv or '-vv' in argv:
        vv = True

    try:
        group_id = int(argv[1])

        if group_id < 1:
            logs.echoWarning('Group id must be positive')
            exit(0)

    except:
        logs.echoWarning('Invalid group_id')
        logs.echoInfo('Group id must be an integer')

    if not settings.user['access_token']:
        logs.echoWarning('Missing access_token. Put it in settings.py file')
        exit(0)

    if vv: logs.echoInfo('Checking access_token...')

    if not f.check_valid():
        logs.echoMinus('access_token is invalid! Put correct access_token in settings.py')
        exit(0)

    if vv: logs.echoPlus('access_token is valid')

    sql.create_table()

    if vv: logs.echoPlus('Created table ' + settings.db['table_name'])

    logs.echoInfo('Starting...')

    start_time = time.time()

    members_count = f.groupsGetMembers(group_id, 0)['count']

    offset = 0
    analyzed = 0
    wrote = 0
    logs.echoPlus('Started')

    try:
        while offset < members_count:
            user_ids = f.groupsGetMembers(group_id, offset)['items']

            us_offset_1 = -200
            us_offset_2 = 0

            while us_offset_2 != len(user_ids):
                us_offset_1 += 200

                if (len(user_ids) - 200) > us_offset_2:
                    us_offset_2 += 200

                else:
                    us_offset_2 = len(user_ids)

                response = f.usersGetInfo(user_ids[us_offset_1:us_offset_2])

                for i in range(len(response)):
                    try:
                        flag = True

                        info = response[i]

                        link = 'https://vk.com/' + info['domain']

                        first_name = info['first_name']
                        last_name = info['last_name']
                        mobile_phone = info['mobile_phone'].replace('(', '').replace(')', '').replace(' ', '').replace('-', '')

                        try:
                            city = info['city']['title']

                        except:
                            city = 'Не указан'

                        try:
                            country = info['country']['title']

                        except:
                            country = 'Не указана'

                        try:
                            bdate = info['bdate']

                        except:
                            bdate = 'Не указана'

                        try:
                            sex = info['sex']

                            if sex == 1:
                                sex = 'Женский'

                            elif sex == 2:
                                sex = 'Мужской'

                            else:
                                sex = 'Другое'

                        except:
                            sex = 'Не указан'

                        try:
                            for symbol in settings.filtr['phone_blacklisted_symbols']:
                                if not flag:
                                    break

                                if symbol in mobile_phone.lower() or len(mobile_phone) < 8 or mobile_phone in settings.filtr['phone_blacklisted_phones']:
                                    flag = False

                        except Exception:
                            pass

                        if sex.lower() in settings.filtr['sex_blacklisted_sex']:
                            flag = False

                        if city.lower() in settings.filtr['city_blacklisted_city']:
                            flag = False

                        if country.lower() in settings.filtr['country_blacklisted_country']:
                            flag = False

                        if bdate in settings.filtr['bdate_blacklisted_bdate']:
                            flag = False


                        if flag:
                            sql.add_line(
                                first_name=first_name,
                                last_name=last_name,
                                sex=sex,
                                bdate=bdate,
                                mobile_phone=mobile_phone,
                                city=city,
                                country=country,
                                link=link
                            )

                            wrote += 1

                    except:
                        pass

                analyzed += len(response)

                if vv: logs.echoInfo('Analyzed users: (' + str(analyzed) + '/' + str(members_count) + ')')
                if vv: logs.echoInfo('Wrote info about ' + str(wrote) + ' users')

            offset += 1000

        print()
        logs.echoPlus('Finished')

        f.stats(
            start_time=start_time,
            members_count=members_count,
            analyzed=analyzed,
            wrote=wrote,
            did_not_indicate=members_count - wrote
                )

    except KeyboardInterrupt:
        print()
        logs.echoInfo('Interrupted')

        f.stats(
            start_time=start_time,
            members_count=members_count,
            analyzed=analyzed,
            wrote=wrote,
            did_not_indicate=members_count - wrote
        )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        logs.echoInfo('Interrupted')
        exit(0)
