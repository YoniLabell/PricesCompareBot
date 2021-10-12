import json

def add_store(uid,store):
    uid=str(uid)
    store=str(store)

    try:
        f= open('users.json','r')
        users=json.load(f)
        f.close()
        users=dict(users)
    except:
        users={}


    if uid in users.keys():

        if store not in users[uid]:
            if len(users[uid])>2:
                rt='ניתן להוסיף עד שלושה סניפים, לא הוספתי!'
                return rt
            else:
                users[uid].append(store)
                rt='הוספתי!'
        else:
            rt='כבר קיים!'


    else:
        users[uid]=[store]
        rt='הוספתי!'

    f = open('users.json', 'w')
    json.dump(users,f)
    f.close()
    return rt

def del_store(uid,store):
    uid=str(uid)
    store=str(store)
    f= open('users.json','r')
    users=json.load(f)
    f.close()

    users=dict(users)
    if uid in users.keys() and store in users[uid]:
        users[uid].remove(store)
        rt='מחקתי!'
    else:
       rt= 'לא קיים!'
       return rt

    f = open('users.json', 'w')
    json.dump(users,f)
    f.close()
    return rt


def get_stores(uid):
    uid=str(uid)
    f= open('users.json','r')
    users=json.load(f)
    f.close()

    if uid in users:
        return users[uid]
    else:
        return []

