import json



def change_time(time_):
    with open('./configs/config.json', 'r', encoding='utf-8') as f:
        admins = json.load(f)
    admins['bot']['while_true'].remove(admins['bot']['while_true'][0])
    admins['bot']['while_true'].append( (time_ * 60) )
    result = True
    with open('./configs/config.json', 'w', encoding='utf-8') as f:
        json.dump(admins, f,ensure_ascii=False, indent=4)
    return result

def get_time():
    with open('./configs/config.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['bot']['while_true'][0]


async def add_admin(user_id, nickname):
    with open('./configs/config.json', 'r', encoding='utf-8') as f:
        admins = json.load(f)
        id_users = []
        for i in admins['bot']['admin_list']:
            id_users.append(i['user_id'])
    if user_id not in id_users:
        admins['bot']['admin_list'].append({"user_id":user_id, "nickname":nickname})
    with open('./configs/config.json', 'w', encoding='utf-8') as f:
        json.dump(admins,  f,ensure_ascii=False, indent=4)


async def remove_admin(user_id):
    with open('./configs/config.json', 'r', encoding='utf-8') as f:
        admins = json.load(f)
    try:
        remove = []
        for i in admins['bot']['admin_list']:
            if int(user_id) == i['user_id']:
                id_user = i['user_id']
                nickname = i['nickname']
                admin = True
            else:
                admin = False
        admins['bot']['admin_list'].remove({"user_id":id_user, "nickname":nickname})
    except Exception as i:
        admin = False
    with open('./configs/config.json', 'w', encoding='utf-8') as f:
        json.dump(admins,  f,ensure_ascii=False, indent=4)
    return admin


async def see_admins():
    with open('./configs/config.json', 'r', encoding='utf-8') as f:
        list_admins = []
        admins = json.load(f)
        current_position = 1
        for i in admins['bot']['admin_list']:
            character = dict()
            character['user_id'] = i['user_id']
            character['nickname'] = i['nickname']
            character['position'] = current_position
            list_admins.append(character)
            current_position += 1
        return list_admins

async def get_admins():
    with open('./configs/config.json', 'r', encoding='utf-8') as f:
        admins = json.load(f)
        id_users = []
        for i in admins['bot']['admin_list']:
            id_users.append(i['user_id'])
    return id_users