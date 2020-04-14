#
#


import snap7
from snap7.util import *
import struct
import csv
import time
from datetime import datetime
from datetime import date
import fnmatch
import os
from snap7.snap7types import *


def data_block_read_byte(db_number, inst_number, size):
    db_area = plc.db_read(db_number, inst_number, size)
    db4_byte = bin(db_area[0]).replace('0b', '')
    data_list = []
    for x in db4_byte:
        data_list.append(x)
    return data_list


def db_read_byte(plc, db_number, inst_number, size, byte_index, bit_index):
    db_area = plc.db_read(db_number, inst_number, size)
    db_byte = get_bool(db_area, byte_index, bit_index)
    return db_byte


plc = snap7.client.Client()
plc.connect('192.168.1.121', 0, 1)

plc_db4_bb0 = db_read_byte(plc, 4, 0, 1, 0, 5)

db4_0 = data_block_read_byte(4, 0, 2)
furnace_valve = db4_0[0]
living_room_valve = db4_0[1]
hall_room_valve = db4_0[2]
bedroom1_valve = db4_0[3]
bedroom2_valve = db4_0[4]
tv_room_valve = db4_0[5]
bathroom_valve = db4_0[6]
#wc_valve = db4_0[7]



#result = plc.read_area(S7AreaDB, 4, 6, 1)
#bytes_my = ''.join([chr(x) for x in result])
#real_num = struct.unpack('>f', bytes_my)

print(furnace_valve)
print(bathroom_valve)
print(db4_0)
print(plc_db4_bb0)


