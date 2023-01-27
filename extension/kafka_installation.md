# About Kafka
- Apache Kafka is a distributed message broker designed to handle large volumes of real-time data. A Kafka cluster is a highly scalable and fault-tolerant, and higher throughput compared to other message brokers like ActiveMQ and RabbitMQ. 
- A publish/subscribe messaging system allows 1/n producers to publish messages without considering the number of consumers or how they will process messages. Subscribed clients are notified automatically about updates and the creation of new messages. This system is more efficient and scalable than systems where clients poll periodically to determine if new messages are available [Kafka-DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-20-04). 

## 1. Download and Extract the Kafka binaries 

      $mkdir Kafka     //create folder named Kafka
      $sudo apt-get install openjdk-8-jre 
      $wget https://archive.apache.org/dist/kafka/3.3.0/kafka_2.13-3.3.0.tgz      //download binaries 
      $tar -xzf [name_folder_kafka_downloaded]     //uncompress 

Versions of Kafka can be found at (https://archive.apache.org/dist/kafka/). 


