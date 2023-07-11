from kafka import KafkaConsumer, KafkaProducer
import sys
import jsons
from json import loads

bootstrapServer = ['165.194.35.87:9092']
topicCollection = ['reports-2','reports-3','reports-4','reports-5','reports-6']
consumerCollection = KafkaConsumer(client_id='collection', bootstrap_servers = bootstrapServer, auto_offset_reset = 'latest', value_deserializer=lambda x: loads(x.decode('utf-8')))
consumerCollection.subscribe(topics=topicCollection)

def WriteReport2File(fileD,report):
    fileDir = fileD
    print("Received msg is ",report)
    fileWriting = open(fileDir, 'a')
    report = str(report) + "\n"
    fileWriting.write(report)
    fileWriting.close()
    print("msg was written to file...")

def ReadMessage():
    while True:
        print('Polling...')
        records = consumerCollection.poll(timeout_ms=10000)
        for topicPartition, messages in records.items():
            if topicPartition.topic == 'reports-2':
                for record in messages:
                    WriteReport2File('./cpu_utilization_rr/cpu_utilization_2_p50.csv', record.value) 
                continue
            elif topicPartition.topic == 'reports-3':
                for record in messages:
                    WriteReport2File('./cpu_utilization_rr/cpu_utilization_3_p50.csv', record.value) 
                continue
            elif topicPartition.topic == 'reports-4':
                for record in messages:
                    WriteReport2File('./cpu_utilization_rr/cpu_utilization_4_p50.csv', record.value) 
                continue
            elif topicPartition.topic == 'reports-5':
                for record in messages:
                    WriteReport2File('./cpu_utilization_rr/cpu_utilization_5_p50.csv', record.value)
                continue
            elif topicPartition.topic == 'reports-6':
                for record in messages:
                    WriteReport2File('./cpu_utilization_rr/cpu_utilization_6_p50.csv', record.value)
                continue
            

ReadMessage()

