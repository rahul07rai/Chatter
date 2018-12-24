#!/usr/bin/env python3

import jwt
import psycopg2
from pony.orm import *
from datetime import datetime

key = 'bviwkjsvdvf3wel4t38jvv43tljhsk'

db = Database()
db.bind(provider='postgres', user='postgres', password='postgres', host='localhost', database='mytest')
#db.bind(provider='sqlite', filename=':memory:')

class User(db.Entity):
    name = Required(str, unique=True)
    password = Required(str)
    contact = Required(int, unique=True)
    signature = Required(str, unique=True)
    dt = Required(datetime)
    message1 = Set('Chat', reverse='sender')
    message2 = Set('Chat', reverse='receiver')
    
class Chat(db.Entity):
    text = Required(str)
    dt = Required(datetime)
    receiver = Required(User, reverse='message2')
    sender = Required(User, reverse='message1')

db.generate_mapping(create_tables=True)

@db_session
def add_data(username, password, cont_num, sig, timestamp):
    u = User(name=username, password=password, contact=cont_num, signature=sig, dt=timestamp)
    commit()

@db_session
def add_text(send, recv, text, timestamp): 
    sender = User.get(signature = send)
    receiver = User.get(signature = recv)
    c = Chat(sender=sender.id, receiver=receiver.id, text=text, dt=timestamp)
    commit()

@db_session
def auth(sig, passwd):
    user = User.get(signature=sig)
    if user.password == passwd:
        return 0
    else:
        return 1

@db_session
def get_text(send, recv):
    sender = User.get(signature = send)
    receiver = User.get(signature = recv)
    chat = select(c for c in Chat if c.receiver == User[receiver.id] and c.sender == User[sender.id])
    for t in chat:
        print(t.text)

@db_session
def get_text_api(recv, start, end):
    chat_dict = {}
    receiver = User.get(signature = recv)
    chat = select(c for c in Chat if c.receiver == User[receiver.id])
    for c in chat:
        if start <= c.dt.timestamp() or end >= c.dt.timestamp():
            if c.sender.signature in chat_dict:
                chat_dict[c.sender.signature].append([c.text, c.dt.timestamp()])
            else:
                chat_dict[c.sender.signature] = [[c.text, c.dt.timestamp()]] 
    return jwt.encode(chat_dict, key, algorithm='HS256')

@db_session
def friendList(sig):
    frnd_sig_list = select(u.signature for u in User if u.signature != sig)[:]
    return frnd_sig_list

