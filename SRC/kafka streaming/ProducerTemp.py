from email import message
from pykafka import KafkaClient
import json
from datetime import datetime
import time
import numpy as np

#generating data from file 
file_dir = './datasets/intel/interpolated/injected_mixed_experiment/temp1.txt'
id_data = [1,2] #1: temp, 2: light 
id_node = [1, 2, 3] #1: sensor node 1, 2: sensor node 2, 3: sensor node 3
id_data_now = id_data[0]  #data set is temperature data
id_node_now = id_node[1]  #node 2
def generate_data(file_dir, id_node_now, id_data_now):
    id_node = id_node_now
    id_data = id_data_now 
    input_file = open(file_dir, 'r')      #open file to read
    lines = input_file.readlines()        #read all lines in file
    lines.pop(0)                          #remove the first line of properties name
    sensorData = []
    for item in lines:
        line_i = item.split(',')          #read one by line with removing the comma 
        line_i.pop(0)                     #remove time
        line_i.pop(0)                     #remove mode id 
        line_i.pop(0)                     #remove fault type
        line_i.pop()                     #remove light
        line_i_array = np.array(line_i)   #convert list into array
        line_i_array = [float(item) for item in line_i_array]    #str into float 
        line_i_array = [id_node,id_data] + line_i_array 
        sensorData = sensorData + [line_i_array]
    return sensorData

#kafka producer on sensor node
client = KafkaClient(hosts="192.168.10.10:9092")     #connect to the broker at IP and port
topic = client.topics['sensordata2']              #connect to the topic of sensordata1
producer = topic.get_sync_producer() #create a producer with syn = true
#send data to broker 

sensorData = generate_data(file_dir, id_node_now, id_data_now)
for item in sensorData:
    data_item = {}
    data_item['time'] = str(datetime.utcnow())   #add timestamp
    data_item['idnode'] = item[0]
    data_item['iddata'] = item[1]
    data_item['value'] = item[2]
    message = json.dumps(data_item)              #make massage as json format
    print('message now is \n')
    print(message)
    producer.produce(message.encode('utf-8'))
    time.sleep(3)                                #send each 3 seconds
