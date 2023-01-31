from kafka import KafkaProducer
import jsons

class MessageProducer:
      broker = ""
      topic = ""
      producer = None

      def __init__(self, broker, topic):
          self.broker = broker
          self.topic = topic
          self.producer = KafkaProducer(bootstrap_servers=self.broker, value_serializer=lambda v: jsons.dumps(v).encode('utf-8'), acks='all', retries = 3)

      def send_msg(self,msg):
          print("sending message ...")
          try:
              future = self.producer.send(self.topic,msg)
              self.producer.flush()
              future.get(timeout=60)
              print("message done ...")
              return {'status_code':200, 'error':None}
          except Exception as ex:
              return ex

broker = '165.194.35.81:9092'
topic = 'testing'
message_producer = MessageProducer(broker,topic)

data = {'id':'test1', 'data':'lalalala from cluster2'}
resp = message_producer.send_msg(data)
print(resp)
