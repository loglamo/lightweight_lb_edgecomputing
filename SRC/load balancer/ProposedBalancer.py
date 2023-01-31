from operator import index
from confluent_kafka import Consumer
from more_itertools import consume
import psutil 
from scipy import optimize 
import math
import numpy as np

#config broker servers
conf = {'bootstrap.servers': 'localhost:9092',
            'group.id': 'sensornode',
            'auto.offset.reset': 'smallest'}
#create a consumer
consumer = Consumer(conf)
#consumer subs topics 
consumer.subscribe(['sensordata1','sensordata2','sensordata3'])

def balancer_proposal(sensordata, idleCPU):
    # iddata_sensornode1 = sensordata[0]
    # iddata_sensornode2 = sensordata[1]
    # iddata_sensornode3 = sensordata[2]
    # weight_value = 0.7
    # priority_value_sensornode1 = 0.0  #priority value of data type
    # priority_value_sensornode2 = 0.0  #priority value of data type
    # priority_value_sensornode3 = 0.0  #priority value of data type
    # #specify priority value
    # if (iddata_sensornode1 == 1):
    #     priority_value_sensornode1 = weight_value
    # else:
    #     priority_value_sensornode1 = 1 - weight_value 
    # if (iddata_sensornode2 == 1):
    #     priority_value_sensornode2 = weight_value
    # else:
    #     priority_value_sensornode2 = 1 - weight_value 
    # if (iddata_sensornode3 == 1):
    #     priority_value_sensornode3 = weight_value
    # else:
    #     priority_value_sensornode3 = 1 - weight_value 
    # priority_value_array = [priority_value_sensornode1, priority_value_sensornode2, priority_value_sensornode3] 
    index_priority_sort_list = np.argsort(sensordata)
    #call CPU context of edge nodes 
    # cpu_test_masternode = psutil.cpu_percent()   #cpu utilization of master node for testing 
    # idle_cpu_test_masternode = 100 - cpu_test_masternode   #idle cpu of testing nodes
    # idle_cpu_test_node2 = 50 #idle cpu of testing nodes 
    # idle_cpu_test_node3 = 40 #idle cpu of testing nodes
    # idle_value_array = [idle_cpu_test_masternode, idle_cpu_test_node2, idle_cpu_test_node3]
    index_idle_sort_list = np.argsort(idleCPU)
    bestPairs = [index_priority_sort_list, index_idle_sort_list]
    bestPairs = np.array(bestPairs)
    return bestPairs
    

    
    



# def main():
#     while True:
#         msg = consumer.poll(1.0)
#         if msg is None:
#             continue
#         if msg.error():
#             print('error: {}'.format(msg.error()))
#             continue
#         data = msg.value().decode('utf-8')
#         print(data)
#     consumer.close()

# if __name__ == '__main__':
#     main()
