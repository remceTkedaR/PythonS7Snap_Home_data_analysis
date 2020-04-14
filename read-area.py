
import snap7
import struct
import snap7.client
from snap7.snap7types import *
from snap7.util import *


def data_block_item(db_number, inst_number, data):
    item_val = client.read_area(areas['DB'], db_number, inst_number, data)
    item_struct = struct.iter_unpack("!f", item_val[:4])
    for item_pack in item_struct:
        item_unpack = item_pack
    # Convert tuple to float
    # using join() + float() + str() + generator expression
    result = float('.'.join(str(ele) for ele in item_unpack))
    item_str_value = '%-.4f' % result
    return item_str_value


#client = snap7.client.Client()
#client.connect('192.168.1.121', 0, 1)



class DBObject(object):
    pass


offsets = { "Bool":2,"Int": 2,"Real":4,"DInt":6,"String":256}

db=\
"""
Temperature Real 0.0
Cold Bool 4.0
RPis_to_Buy Int 6.0
Db_test_String String 8.0
"""

def DBRead(plc,db_num,length,dbitems):
    data = plc.read_area(areas['DB'], db_num, 0, length)
    obj = DBObject()
    for item in dbitems:
        value = None
        offset = int(item['bytebit'].split('.')[0])

        if item['datatype']=='Real':
            value = get_real(data,offset)

        if item['datatype']=='Bool':
            bit =int(item['bytebit'].split('.')[1])
            value = get_bool(data,offset,bit)

        if item['datatype']=='Int':
            value = get_int(data, offset)

        if item['datatype']=='String':
            value = get_string(data, offset)

        obj.__setattr__(item['name'], value)

    return obj

def get_db_size(array,bytekey,datatypekey):
    seq,length = [x[bytekey] for x in array],[x[datatypekey] for x in array]
    idx = seq.index(max(seq))
    lastByte = int(max(seq).split('.')[0])+(offsets[length[idx]])
    return lastByte



if __name__ == "__main__":
    plc = snap7.client.Client()
    plc.connect('192.168.1.121',0,1)
    itemlist = filter(lambda a: a!='',db.split('\n'))
    deliminator= '\t'
    items = [
        {
            "name": x.split(deliminator)[0],
            "datatype": x.split(deliminator)[1],
            "bytebit": x.split(deliminator)[2]
         } for x in itemlist
    ]
    #get length of datablock
    length = get_db_size(items,'bytebit','datatype')
    meh = DBRead(plc, 4, length, items)
    print(
    Cold,
    Tempeature,
    RPis_to_Buy,
    Db_test_String .format(meh.Cold,meh.Temperature,meh.RPis_to_Buy,meh.Db_test_String))


