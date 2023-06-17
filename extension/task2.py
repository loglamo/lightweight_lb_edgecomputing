# machine learning training task                                                                                                                                                                           
from numpy import loadtxt                                                                                                                                                                                  
from tensorflow.keras.models import Sequential                                                                                                                                                             
from tensorflow.keras.layers import Dense                                                                                                                                                                  
                                                                                                                                                                                                           
# load dataset                                                                                                                                                                                             
dataset = loadtxt('/home/syslab/workspace_la/edge_nodes/tasks/training_data.csv', delimiter=',')                                                                                                           
# split input, output                                                                                                                                                                                      
x = dataset[:,0:8]                                                                                                                                                                                         
y = dataset[:,8]                                                                                                                                                                                           
print("Read data done")                                                                                                                                                                                    
# define keras model                                                                                                                                                                                       
model = Sequential()                                                                                                                                                                                       
model.add(Dense(12, input_shape=(8,), activation='relu'))                                                                                                                                                  
model.add(Dense(8, activation='relu'))                                                                                                                                                                     
model.add(Dense(1, activation='sigmoid'))                                                                                                                                                                  
                                                                                                                                                                                                           
# compile keras                                                                                                                                                                                            
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])                                                                                                                          
                                                                                                                                                                                                           
# fit the keras model on the dataset                                                                                                                                                                       
model.fit(x, y, epochs =500, batch_size = 10)                                                                                                                                                              
# evaluate                                                                                                                                                                                                 
_, accuracy = model.evaluate(x,y)                                                                                                                                                                          
print('Accuracy: %.2f' % (accuracy*100)) 
