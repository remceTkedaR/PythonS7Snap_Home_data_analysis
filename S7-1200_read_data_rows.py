#  Test program for communication of Snap7 python with S7 1200
# Reading data from one variable in a data block
# by Radosław Tecmer
# radek69tecmer@gmail.com
# ------------------------

"""
Home Co
DB4.X6.0 - furnace valve
DB4.X6.1 - Living room valve
DB4.X6.2 - Hall room valve
DB4.X6.3 - Bedroom 1 valve
DB4.X6.4 - Bedroom 2 valve
DB4.X6.5 - TV room valve
DB4.X6.6 - Bathroom valve
DB4.X6.7 - WC valve

"""

import snap7
import snap7.snap7exceptions
from snap7.util import *
import struct
import csv
import time
from datetime import datetime
from datetime import date
import fnmatch
import os
import locale

# Find existing file mame file_data csv


def max_number_file():
    file_list = []
    # Find existing file mame file_data csv
    f_names = ([file_find for root, dirs, files in os.walk(".", topdown=False)
                for file_find in files
                if file_find.endswith('.csv')  #or file.endswith('.png') or file.endswith('.pdf')
                ])
    for f_name in f_names:
        f_name_new = f_name.replace('file_data', '')  # cutoff file_data
        f_new = f_name_new.replace('.csv', '')  # cutoff .csv
        file_list.append(f_new)  # digit received
    try:
        max_number_str = max(file_list)
        number_int = (int(max_number_str) + 1)
    except ValueError:  # if there are no files, enter zero
        number_int = 0
    return number_int


# time start to  delay
last_time_ms = int(round(time.time() * 10000))

# Function read data from instance db


def data_block_item(db_number, inst_number, data):
    item_val = plc.read_area(db_number, inst_number, data)
    item_struct = struct.iter_unpack("!f", item_val[:4])
    for item_pack in item_struct:
        item_unpack = item_pack
    # Convert tuple to float
    # using join() + float() + str() + generator expression
    result = float('.'.join(str(ele) for ele in item_unpack))
    item_str_value = '%-.4f' % result
    return item_str_value


# Function read data from instance db


def data_block_read(db_number, inst_number, data):
    db_val = plc.db_read(db_number, inst_number, data)
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
    byte_bit = plc.ab_read(byte_out, byte_size)
    byte_bit_array = (byte_bit[0])
    byte_coils = bin(byte_bit_array).replace("0b", "")
    result = (byte_coils[out_bit])
    return result


# Function get the boolean value from location in bytes from DB instance
def db_read_byte(plc, db_number, inst_number, size, byte_index, bit_index):
    db_area = plc.db_read(db_number, inst_number, size)
    db_byte = get_bool(db_area, byte_index, bit_index)
    return db_byte

# Find number new file


b = max_number_file()

while True:

    # Opened file to writing
    file = open('file_data.csv', 'w+')
    file_data_csv = csv.writer(file)

    # file headers to saving
    file_data_csv.writerow(
        ['Date', 'Time', 'Outside', 'Living room', 'Hall', 'Bedroom 1', 'Bedroom 2', 'Bathroom', 'Room'
         , 'furnace valve', 'Living room valve', 'Hall room valve', 'Bedroom 1 valve', 'Bedroom 2 valve',
         'TV room valve', 'Bathroom valve', 'WC valve'])

    # index measurement loop
    a = 0
    # generating new name file
    filename = str('file_data' + str(b) + '.csv')
    # index for new file name
    b += 1

    # measurement loop, set number of lines in the file
    while a < 12:
        # execution condition delay time
        diff_time_ms = int(round(time.time() * 10000)) - last_time_ms
        # This is delay 3000000ms = 5min
        if diff_time_ms >= 3000000:
            last_time_ms = int(round(time.time() * 10000))

            # Stamp to time & date
            now = datetime.now()
            today = date.today()
            time_today = now.strftime("%H:%M:%S")

            #  connect to S7 1200
            try:
                plc = snap7.client.Client()
                plc.connect('192.168.1.121', 0, 1)
                error_connect = plc.get_connected()
            except snap7.snap7exceptions.Snap7Exception:
                time.sleep(0.2)
                plc = snap7.client.Client()
                plc.connect('192.168.1.121', 0, 1)

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

            # Status Valves Home
            furnace_valve = db_read_byte(plc, 4, 6, 1, 0, 0)
            living_room_valve = db_read_byte(plc, 4, 6, 1, 0, 1)
            hall_room_valve = db_read_byte(plc, 4, 6, 1, 0, 2)
            bedroom1_valve = db_read_byte(plc, 4, 6, 1, 0, 3)
            bedroom2_valve = db_read_byte(plc, 4, 6, 1, 0, 4)
            bathroom_valve = db_read_byte(plc, 4, 6, 1, 0, 5)
            room_tv_valve = db_read_byte(plc, 4, 6, 1, 0, 6)

            plc.disconnect()

            # save to file

            file_data_csv.writerow([today, time_today, outside, living_room, hall, bedroom_1, bedroom_2,
                                    bathroom, room_tv, furnace_valve, living_room_valve, hall_room_valve,
                                    bedroom1_valve, bedroom2_valve, bathroom_valve, room_tv_valve])

            a += 1
            print(a)
            if a == 3:
                file.close()
                os.rename('file_data.csv', str(filename))  # rename file

                print('close file')
                break


