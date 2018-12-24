#!/usr/bin/env python3

import jwt
from db import get_text_api

class decrypt(object):
    def __init__(self):
        self.__key = 'bviwkjsvdvf3wel4t38jvv43tljhsk'
        self.__get_encoded_data()

    def __get_encoded_data(self):
        self.__user = input("Enter signature : ")
        print("Enter timestamp range")
        self.__start = float(input("Start : "))
        self.__end = float(input("End : "))
        self.__encoded = get_text_api(self.__user, self.__start, self.__end)

    def decode_data(self):
        return jwt.decode(self.__encoded, self.__key, algorith=['HS256'])

if __name__ == '__main__':
    d = decrypt()
    data = d.decode_data()
    print(data)

