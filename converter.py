from cgitb import text
import sys
import os
import glob
import json

# defines =====================

ID_KEY = 'id'
TEXT_KEY = 'text'
USER_KEY = 'user'
PROFILE_KEY = 'profile'
REAL_NAME_KEY = 'real_name'
DISPLAY_NAME_KEY = 'display_name'
FILES_KEY = 'files'
URL_KEY = 'url_private'


USER_FILE_NAME = 'users.json'

# functions =====================

def json_file_to_data(full_path):
        f = open(full_path, 'r')

        converted = json.load(f)

        f.close()

        return converted


def get_users(source_dir):
    users_json = json_file_to_data(source_dir)
    users = {}

    for user in users_json:
        
        name = user[PROFILE_KEY][DISPLAY_NAME_KEY]
        if not name:
            name = user[PROFILE_KEY][REAL_NAME_KEY]
        id = user[ID_KEY]
        users[id] = name

    return users

# core logics =====================

argv = sys.argv

if len(argv) < 2:
    print('Please add argument of work directory')
    exit()

source_dir = argv[1]

print(f'workDir > {source_dir}')

output_dir = f'{source_dir}/../slack_csv_output'

print(f'Create output dir > {output_dir}/')
os.makedirs(output_dir, exist_ok=True)

channels = sorted(os.listdir(path=source_dir))
channels = [x for x in channels if not x.endswith('.json')]

users = get_users(f'{source_dir}/{USER_FILE_NAME}')

for channel in channels:

    print(f'[{channel}]')

    json_files = sorted(glob.glob(f"{source_dir}/{channel}/*.json"))
    lines = "date,name,text,files\n"

    for file_full_path in json_files:
        file_name = os.path.split(file_full_path)[1]
        date = file_name.replace('.json', '')

        json_dic = json_file_to_data(file_full_path)

        for item in json_dic:

            if not (item.keys() >= { TEXT_KEY }):
                continue

            text = f'{item[TEXT_KEY]}'.replace('"', '\"')
            name = ''
            if USER_KEY in item.keys():
                user_id = item[USER_KEY]
                if user_id in users.keys():
                    name = users[user_id]
            urls = ''

            if (item.keys() >= {FILES_KEY}):
                for attachmentFile in item[FILES_KEY]:
                    url = f"{attachmentFile[URL_KEY]}".replace('"', '\"')
                    urls += f'{url}\n'

            lines += f'{date},{name},"{item[TEXT_KEY]}","{urls}"\n'

        print(f'\t{date} ({len(json_dic)})')

    out_file_path = f"{output_dir}/{channel}.csv"
    f = open(out_file_path, 'w')
    f.write(lines)
    f.close()

print(f'{len(channels)} channels fineshed.')