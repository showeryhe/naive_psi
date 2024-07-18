import os
import hash
import pickle

def gen():
    pk = b'hello, world'
    return(pk)

def enc_msg(pk: bytes, msg: bytes):
    ct = hash.encrypt(pk, msg)
    return(ct)

def enc_msg_list(pk: bytes, msg_list):
    ct_list=list()
    for msg in msg_list:
        ct_list.append(enc_msg(pk, msg))
    return(ct_list)

def compare_list(pk: bytes, my_msg_list, received_ct_list):
    my_ct_list = enc_msg_list(pk, my_msg_list)
    shared_list = list()
    for x in range(len(my_ct_list)):
        if my_ct_list[x] in received_ct_list:
            shared_list.append(my_msg_list[x])
    return(shared_list)

def read_data(file_name: str):
    msg_list = list()
    f = open(file_name, 'r')
    try: 
        for line in f.readlines():
            tmp = line.rstrip('\n') #line带"\n"
            msg_list.append(tmp.encode('utf-8'))
    finally:
        f.close()
    return(msg_list)

def sender(pk: bytes):
    msg_list = read_data('sender_data.txt')
    ct_list=enc_msg_list(pk, msg_list)
    # 将 bytes 列表写入文件
    with open("sender_ct.pkl", "wb") as file:
        pickle.dump(ct_list, file)
    return()

def get_ct_list():
    ct_list = list()
    with open("sender_ct.pkl", "rb") as file:
        ct_list = pickle.load(file)
    return(ct_list)

def receiver(pk: bytes):
    my_msg_list = read_data('my_data.txt')
    received_ct_list = get_ct_list()
    return(compare_list(pk, my_msg_list, received_ct_list))

def main():
    pk = gen()
    print(receiver(pk))
    return

if __name__ == "__main__":
    main()
