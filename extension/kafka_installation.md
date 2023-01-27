# About Kafka
- Apache Kafka is a distributed message broker designed to handle large volumes of real-time data. A Kafka cluster is a highly scalable and fault-tolerant, and higher throughput compared to other message brokers like ActiveMQ and RabbitMQ. 
- A publish/subscribe messaging system allows 1/n producers to publish messages without considering the number of consumers or how they will process messages. Subscribed clients are notified automatically about updates and the creation of new messages. This system is more efficient and scalable than systems where clients poll periodically to determine if new messages are available [Kafka-DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-20-04). 

## 1. Download and Extract the Kafka binaries 

      $mkdir Kafka     //create folder named Kafka
      $sudo apt-get install openjdk-8-jre 
      $wget https://archive.apache.org/dist/kafka/3.3.0/kafka_2.13-3.3.0.tgz      //download binaries 
      $tar -xzf [name_folder_kafka_downloaded]     //uncompress 

Versions of Kafka can be found at (https://archive.apache.org/dist/kafka/). 

## 2. Config Kafka and Zookeeper 
![kafkafolder](https://user-images.githubusercontent.com/18479389/215024990-7d8a4490-c37e-41c6-aa87-1f02a6f89e07.png)

There are two main directories in kafka folder: bin and config directory. 

- Bin: Holds all executables such as Kafka and Zookeeper tools 
- Config: Holds configuration files 

![mainfolders](https://user-images.githubusercontent.com/18479389/215026148-056a7ef4-379b-420a-8887-49fc9ca03978.png)

Kafka's default behaviour will not allow to delete a Topic. A Kafka topic is the category of message to which messages can be published into. To edit the default of Kafka, you must edit the configuration file "server.properties" in config folder. 

       $nano server.properties   //open config file of kafka
       delete.topic.enable = true    //add this line into the bottom of config file

![configkafkadeletetopics](https://user-images.githubusercontent.com/18479389/215028174-09a67a30-17e4-4aab-a3ba-1860a93bbfe5.png)

Creating systemd unit files for the Kafka service helps to perform common service actions such as staring, stopping, restarting Kafka in a consistent manner with other Linux services. Firstly, create an unit file for zookeeper. Zookeeper is a service that Kafka uses to manage its cluster states and configurations. 

       $sudo nano /etc/systemd/system/zookeeper.service   //make empty unit file for zookeeper

![unitfilezoo](https://user-images.githubusercontent.com/18479389/215031103-74fe5dd9-e411-41e9-91b6-235632d2c9d2.png)

The unit file for zookeeper can be edit as the above figure. 
