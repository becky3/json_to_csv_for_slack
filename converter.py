from cgitb import text
import sys
import os
import glob
import json

class UserInfo:
    display_name = ""
    real_name = ""

argv = sys.argv

TEXT_KEY = 'text'
PROFILE_KEY = 'user_profile'
FIRST_NAME_KEY = 'first_name'
REAL_NAME_KEY = 'real_name'
DISPLAY_NAME_KEY = 'display_name'
FILES_KEY = 'files'
URL_KEY = 'url_private'

USER_FILE_NAME = 'users.json'

def json_file_to_data(full_path):
        f = open(full_path, 'r')

        converted = json.load(f)

        f.close()

        return converted


# def get_user_list(source_dir):


if len(argv) < 2:
    print('Please add argument of work directory')
    exit()

source_dir = argv[1]

print(f'workDir > {source_dir}')

output_dir = f'{source_dir}/../slack_csv_output'

print(f'Create output dir > {output_dir}/')
os.makedirs(output_dir, exist_ok=True)

channels = sorted(os.listdir(path=source_dir))

for channel in channels:
    print(channel)

    json_files = sorted(glob.glob(f"{source_dir}/{channel}/*.json"))
    lines = "date,first_name,real_name,display_name,text,files\n"

    for file_full_path in json_files:
        file_name = os.path.split(file_full_path)[1]
        date = file_name.replace('.json', '')

        print(f'\t{date}')

        json_dic = json_file_to_data(file_full_path)

        for item in json_dic:

            if not (item.keys() >= { TEXT_KEY }):
                continue

            text = f'{item[TEXT_KEY]}'.replace('"', '\"')
            first_name = ""
            real_name = ""
            display_name = ""

            if (item.keys() >= { PROFILE_KEY }):
                first_name = item[PROFILE_KEY][FIRST_NAME_KEY]
                real_name = item[PROFILE_KEY][REAL_NAME_KEY]
                display_name = item[PROFILE_KEY][DISPLAY_NAME_KEY]

            urls = ""

            if (item.keys() >= {FILES_KEY}):
                for attachmentFile in item[FILES_KEY]:
                    url = f"{attachmentFile[URL_KEY]}".replace('"', '\"')
                    urls += f'{url}\n'

            lines += f'{date},{first_name},{real_name},{display_name},"{item[TEXT_KEY]}","{urls}"\n'

    print(lines)

    out_file_path = f"{output_dir}/{channel}.csv"
    f = open(out_file_path, 'w')
    f.write(lines)
    f.close()
