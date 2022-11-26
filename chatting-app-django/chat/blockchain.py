# -*- coding: utf-8 -*-

import json
import os
import hashlib
from chat.models import Message


def get_hash(filename):
    # file = open(bch_dir + filename, 'rb').read()
    return hashlib.md5(filename.encode('utf-8')).hexdigest()


def get_integrity(id_sender, id_receiver):
    # a = (i.sender_id == int(id_sender) and i.receiver_id == int(id_receiver)) or (
    #         i.sender_id == int(id_receiver) and i.receiver_id == int(id_sender))
    list_msg = Message.objects.all()
    if len(list_msg) == 1:
        return {'text_msg': 'pisja-popa', 'change_bool': False}
    list_new = []
    for i in list_msg:
        if ((i.sender_id == int(id_sender) and i.receiver_id == int(id_receiver)) or (
                i.sender_id == int(id_receiver) and i.receiver_id == int(id_sender))) or i.sender_id is None:
            list_new.append(i)
    list1 = list()
    for i in range(1, len(list_new)):
        actual_hash = get_hash(list_new[i - 1].message)
        if list_new[i].hash_bloks == actual_hash:
            res = False
        else:
            res = True
        # elif list_msg[i].hash_bloks != actual_hash and (
        #         (list_msg[i].sender_id == int(id_sender) and list_msg[i].receiver_id == int(id_receiver)) or (
        #         list_msg[i].sender_id == int(id_receiver) and list_msg[i].receiver_id == int(id_sender))):
        #     res = True
        # elif ((list_msg[i].sender_id == int(id_sender) and list_msg[i].receiver_id == int(id_receiver)) or (
        #         list_msg[i].sender_id == int(id_receiver) and list_msg[i].receiver_id == int(id_sender))):
        #     print('не нашеееееееееееееееееееееееееееееееееее')
        list1.append({'text_msg': list_new[i - 1], 'change_bool': res})
    return list1


def write_blok(id_sender, msg_text, id_receiver, hash='', name_two_person=(None, None)):
    get_last_msg1 = str(Message.objects.all().last().message)
    get_last_msg = Message.objects.all()
    flag_dialog_exist = False
    for i in get_last_msg:
        if (i.sender_id == id_sender and i.receiver_id == id_receiver) or (
                i.sender_id == id_receiver and i.receiver_id == id_sender):
            flag_dialog_exist = True
    if flag_dialog_exist:
        for i in reversed(get_last_msg):
            if (i.sender_id == id_sender and i.receiver_id == id_receiver) or (
                    i.sender_id == id_receiver and i.receiver_id == id_sender):
                return {'sender': name_two_person[-1].username, 'receiver': name_two_person[0].username, 'message': msg_text,
                        'hash_bloks': get_hash(i.message)}
    else:
        for i in reversed(get_last_msg):
            if (i.sender_id == None and i.receiver_id == None) or (
                    i.sender_id == None and i.receiver_id == None):
                return {'sender': name_two_person[-1].username, 'receiver': name_two_person[0].username, 'message': msg_text,
                        'hash_bloks': get_hash(i.message)}

