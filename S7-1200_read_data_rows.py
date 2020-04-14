#  Test program for communication of Snap7 python with S7 1200
# Reading data from one variable in a data block
# by Radosław Tecmer
# radek69tecmer@gmail.com
# ------------------------

import snap7
import struct
import csv
import time
from datetime import datetime
from datetime import date
import fnmatch
import os
import locale

# time start to  delay
last_time_ms = int(round(time.time() * 10000))

# Path to save file path:/root/Dokumenty/PythonS7Snap/file_data.csv
path_input = input("please enter where to save the files: ")
path_save = str(path_input)


# Function read data from instance db


def data_block_read(db_number, inst_number, data):
    db_val = client.db_read(db_number, inst_number, data)
    value_struct = struct.iter_unpack("!f", db_val[:4])
    for value_pack in value_struct:
        value_unpack = value_pack
    # Convert tuple to float
    # using join() + float() + str() + generator expression
    result = float('.'.join(str(ele) for ele in value_unpack))
    my_str_value = '%-.4f' % result
    return my_str_value

# function reading coils (byte_out - PLC) (byte-size - PLC coils size) (out_bit - PLC coil)


def read_coils_s7(byte_out, byte_size, out_bit):
    byte_bit = client.ab_read(byte_out, byte_size)
    byte_bit_array = (byte_bit[0])
    byte_coils = bin(byte_bit_array).replace("0b", "")
    result = (byte_coils[out_bit])
    return result


b = 0

while True:

    # Opened file to writing
    file = open(path_save + 'file_data.csv', 'w+')
    file_data_csv = csv.writer(file)

    # file headers to saving
    file_data_csv.writerow(
        ['Date', 'Time', 'Outside', 'Living room', 'Hall', 'Bedroom 1', 'Bedroom 2', 'Bathroom', 'Room'])

    # index measurement loop
    a = 0
    # generating new name file
    filename = str('file_data' + str(b) + '.csv')
    # index for new file name
    b += 1

    # measurement loop
    while a < 3:
        # execution condition delay time
        diff_time_ms = int(round(time.time() * 10000)) - last_time_ms
        # This is delay 80000ms = 8s
        if diff_time_ms >= 3000000:
            last_time_ms = int(round(time.time() * 10000))

            # Stamp to time & date
            now = datetime.now()
            today = date.today()
            time_today = now.strftime("%H:%M:%S")

            #  connect to S7 1200
            try:
                client = snap7.client.Client()
                client.connect('192.168.1.121', 0, 1)
            except snap7.snap7exceptions.Snap7Exception:
                time.sleep(0.2)
                client = snap7.client.Client()
                client.connect('192.168.1.121', 0, 1)

            # Read temperature Outside (db 3, instance 24, data =" real" )
            outside = data_block_read(3, 24, 4)

            # Read temperature Living room (db 3, instance 20, data =" real" )
            living_room = data_block_read(3, 20, 4)

            # Read temperature Hall (db 2, instance 20, data =" real" )
            hall = data_block_read(2, 20, 4)

            # Read temperature Bedroom 1 (db 2, instance 24, data =" real" )
            bedroom_1 = data_block_read(2, 24, 4)

            # Read temperature Bedroom 2 (db 2, instance 28, data =" real" )
            bedroom_2 = data_block_read(2, 28, 4)

            # Read temperature Bathroom (db 2, instance 32, data =" real" )
            bathroom = data_block_read(2, 32, 4)

            # Read temperature Room TV (db 2, instance 36, data =" real" )
            room_tv = data_block_read(2, 36, 4)

            client.disconnect()

            # save to file

            file_data_csv.writerow([today, time_today, outside, living_room, hall, bedroom_1, bedroom_2,
                                    bathroom, room_tv])

            a += 1
            print(a)
            if a == 3:
                file.close()
                os.rename(path_save + 'file_data.csv', path_save + str(filename))

                print('close file')
                break


