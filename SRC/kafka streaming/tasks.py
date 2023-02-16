# from cgi import test
# from pyexpat import model
from confluent_kafka import Consumer
from influxdb import InfluxDBClient
import numpy as np 
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from matplotlib import pyplot as plt


#config information of the Broker
conf = {'bootstrap.servers': '165.194.35.81:9092',
         'group.id': "sensornode",
         'auto.offset.reset': 'smallest'}
#read data from file 
file_dir = './light1.txt'
id_node = 1
id_data = 1
input_file = open(file_dir, 'r')
lines = input_file.readlines()
lines.pop(0)
sensorData = []
for item in lines:
    line_i = item.split(',')
    line_i.pop(0)
    line_i.pop(0)
    line_i.pop(0)
    line_i.pop(0)
    line_i_array = np.array(line_i)
    line_i_array = [float(item) for item in line_i_array]
    line_i_array = [id_node,id_data] + line_i_array
    sensorData = sensorData + [line_i_array]

lightData = sensorData[0:500][:] #take first 500 rows as training data
lightData = np.array(lightData)
lightData = lightData[:,2]
print(len(lightData))
testData = sensorData[501:550][:] #take next 50 lines as testing data
testData = np.array(testData)
testData = testData[:,2]



#DCSD in python 
#fit model to train 
fitted_model = ExponentialSmoothing(lightData).fit()
pred_values = fitted_model.forecast(1)
print(pred_values)

# plt.xlabel('timestamp')
# plt.ylabel('light values')
# plt.title('HWS forecasting')
# plt.show()
