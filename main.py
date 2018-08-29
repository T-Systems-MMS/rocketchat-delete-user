import json
import requests
import os
import sys
import urllib3

rocketchat_url = os.environ['CHAT_HOST']

confirmation_to_delete = False

if os.environ['CHAT_SECURE'] == 'False':
    secure = False
else:
    secure = True

if secure == False:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if os.environ['CHAT_CONFIRM_DELETE'] == 'False':
    confirmation_to_delete = True

def get_auth_params():

    data = { "username": os.environ['CHAT_ADMIN_USERNAME'], "password":  os.environ['CHAT_ADMIN_PASSWORD'] }

    r = requests.post(url = rocketchat_url + '/api/v1/login', data = json.dumps(data), verify = secure)

    user_json = json.loads(r.text)

    user_id = user_json['data']['userId']
    auth_token = user_json['data']['authToken']

    return [user_id, auth_token]

def get_user_id(auth_headers, username):

    r = requests.get(url=rocketchat_url + '/api/v1/users.list?query={"username":"' + username + '"}&count=0', headers = auth_headers, verify = secure)

    user_list = json.loads(r.text)

    try:
        user_id = user_list['users'][0]['_id']
    except (ValueError,IndexError):
        print("User not found")
        exit(0)

    return user_id

def delete_user(auth_headers, user_id):

    data = {"userId": user_id}

    r = requests.post(url=rocketchat_url + '/api/v1/users.delete', data=json.dumps(data), verify = secure, headers = auth_headers)

def query_yes_no(question, default="no"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

auth_params = get_auth_params()

user_id = auth_params[0]
auth_token = auth_params[1]

headers = {'X-User-Id': user_id,
           'X-Auth-Token': auth_token,
           'Content-type': 'application/json',
           }

user_id_to_delete = get_user_id(headers, sys.argv[1])

print("User " + sys.argv[1] + " with ID " + user_id_to_delete + " will be deleted now ...")

if confirmation_to_delete != True:
    confirmation_to_delete = query_yes_no("Confirm?")

if confirmation_to_delete == True:
    delete_user(headers, user_id_to_delete)
else:
    print("Aborting now...")


