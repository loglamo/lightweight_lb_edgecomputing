# About Kafka Service on Cluster1
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

The unit file for zookeeper can be edit as the above figure. The [Unit] section specifies that Zookeeper requires networking and filesystem to be ready before it can start. The [Service] section specifies systemd should use the zookeeper-server-start.sh and zookeeper-server-stop.sh shell files for starting and stopping the service. Restarting, if it exists abnormally. 

Secondly, create an unit file for kafka:

        $sudo nano /etc/systemd/system/kafka.service

![kafkaunitfile](https://user-images.githubusercontent.com/18479389/215034811-42220ccb-f5fc-4699-909c-719352a000fd.png)

Start kafka with:

        $sudo systemctl start kafka    //start kafka
        $sudo systemctl status kafka   //check status kafka

![startkafka](https://user-images.githubusercontent.com/18479389/215035547-e47d11eb-bd31-460f-af35-9d848e12a898.png)

## 3. Test the Kafka Installation
- Create a new topic:

        $./kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic testing     //create a topic named "testing"

- Send a message to the created topic:

         $echo "Hello, World" | ./kafka-console-producer.sh --broker-list localhost:9092 --topic testing > /dev/null


- Read message from the topic:

         $./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic testing --from-beginning


![pubsubmeaasage](https://user-images.githubusercontent.com/18479389/215042324-938db059-75e7-4cd0-b083-477f3e33e904.png)

Note that using the following command for creating topics with older versions 2.2 of Kafka:

         $./kafka-topics.sh --create --zookeeper localhost:2181 --replication 1 --partitions 1 --topic [name_topic]    //this command does not work with latest versions with the error "no option with --zookeeper"

Kafka server (Kafka service) now well runs on the machine. We can send, receive messages with command lines or using code files with various programming languages (Python, Java, Go, .etc).

__Note: We have to config kafka server with advertising address listeners so that remote machines can send them messages to the topics it holds. Eventhough remote machines can ping kafka server, firewall of kafka server does not work, it does not sure that the kafka server can receive messages.__

We can config with "advertised.listeners" in /config/server.properties like:
![configserver](https://user-images.githubusercontent.com/18479389/215106541-19dd0cc2-b4d1-4ce3-8548-ac0432b4297a.png)

## Appendix
![overviewkafka](https://user-images.githubusercontent.com/18479389/215045309-afb1af74-7b24-4669-88f2-9086c4b9b0cb.png) 

Generally, Kafka ecosystem goes with three players: Producers, topics(run by brokers) and consumers as shown in above figure. It is a distributed pub-sub messaging system that maintains feeds of messages in partitioned and replicated topics (https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1). 

- __Producers__ produce messages according to their choices. It may attach a key to each message, in which case the producer guarantees that all messages with the same key will arrive to the same partition
- __Topics__ are logs that receive data from producers and store them across their partitions. Producers always write new messages at the end of the log
- __Consumers__ read the messages of a set of partitions of a topic
