# **Installation and Deployment**

## **1. Experiment System Design**
The experiment works under the system design as the following figure. 4 nodes are built in this experiment: 1 master node, 3 slave nodes. Each node runs Ubuntu. The master node runs Kafka, InfluxDB, Grafana, and LoadBalancing mechanisms. 3 slave nodes run Kafka, Detecting and Correcting Sensor Data (DCSD). 
![experiment_system](https://user-images.githubusercontent.com/18479389/191924862-59f81a56-37ba-44f4-9cb7-c951ccbbf1fd.png "Experiment system design")
This experiment design focuses on topic design at the Kafka. There are three types of topics in this experiment:
- Topics related to sensor data: SensorData0, SensorData1, SensorData2, which transfer the sensor data information of the device0, device1, device3.  
- Topics related to edge node status: Ref, and InfoEdgeNode topic. The first one transfers the edge node status requirement of the Balancer. The second one transfers the edge node status of all edge nodes to the Balancer. 
- Topics related to task assignment: EdgeNodeTask0, EdgeNodeTask1, EdgeNodeTask2. They transfer the information of task assignment from the Balancer. 

Besides, raw sensor data are stored at the InfluxDB, verified sensor data are also stored at the InfluxDB.

Sensor data and edge node status are visualized on Grafana. 

## **2. Installation**
This installation is with Ubuntu22.04.
### **2.1 Create a cluster of virtual machine with VirtualBox** 
- Install VirtualBox with:
           
              sudo apt update
              sudo apt install virtualbox

- Create a cluster with 4 nodes with VirtualBox: First, a NAT network is made:

      Open VirtualBox -> Click on File ->  Preferences -> Network -> Click icon Adds new NAT network

![Screenshot from 2022-09-23 19-14-00](https://user-images.githubusercontent.com/18479389/191939784-25364812-2995-42b0-8417-f25af67bf6ff.png)
Edit the NAT network EdgeComputing-Cluster:
![Screenshot from 2022-09-23 19-15-42](https://user-images.githubusercontent.com/18479389/191939970-760e7ff1-6abb-4a60-a5af-299258984c3b.png)

Then, make 4 virtual machines.
- Create 4 VMs:

a. Download ubuntu.iso from [iso ubuntu]([title](https://www.example.com)). 

b. Create new VMs, named: EC-slave-en1, EC-slave-en2, EC-slave-en3, and EC-master-lb1.

    Click on New -> Name the VM -> Type: Linux -> Linux2.6/3.x/4.x(64-bit) -> Set memory size: 2048MB -> Create a virtual hard disk now -> VDI -> Dynamically allocated -> File location and size: 30GB -> Create. 

Open settings of each VM to config the Network: At Adapter1, click Enable Network Adapter, choose NAT Network, choose the NAT network already created "EdgeComputing-Cluster". At Adapter2, click Enable Network Adapter, choose Bridged Adapter, click OK. 
![Screenshot from 2022-09-23 19-41-25](https://user-images.githubusercontent.com/18479389/191944044-e20dae62-a8a4-4033-866d-17e780bcbcc6.png) 
![Screenshot from 2022-09-23 19-44-20](https://user-images.githubusercontent.com/18479389/191944470-7e0fc314-a7b7-4093-8674-5894d8cb7ac1.png)
At settings of each VM, add ubuntu iso by edit Storage as the figure: Storage -> Empty -> Click CD icon -> add the downloaded iso. Then, start the VM to install ubuntu with safe graphic mode. 
![Screenshot from 2022-09-23 20-06-20](https://user-images.githubusercontent.com/18479389/191947616-d819c71b-a31c-4931-8c6d-4c9079353e32.png)
        
### **2.2 Install and config Kafka** 
kafka should be installed in all nodes (master, slaves).
- Install Docker [Guide docker installation](https://docs.docker.com/engine/install/ubuntu/):
   
        $sudo apt-get update

        $sudo apt-get install \
              ca-certificates \
              curl \
              gnupg \
              lsb-release

        $sudo mkdir -p /etc/apt/keyrings

        $curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

        $echo \
           "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
           $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

        $sudo apt-get update

        $sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin 

        $sudo apt-get install docker-compose 

        $docker-compose --version #check the installation 

- Install Kafka via Docker-compose:

       - Create a new folder, such as "run_cluster" -> add a yaml file named "docker-compose.yml" with these contents:
     
        version: '3'

        services:
           zookeeper:
             image: wurstmeister/zookeeper
             container_name: zookeeper
             ports:
               - "2181:2181"
          kafka:
             image: wurstmeister/kafka
             container_name: kafka
             ports:
               - "9092:9092"
             environment:
               KAFKA_ADVERTISED_HOST_NAME: localhost
               KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181 

        - Execute the following command to create containers of Kafka and Zookeeper: 
         
        sudo docker-compose -f docker-compose.yml up -d
Move to the folder containing the docker-compose.yml file for executing the command. After executing the command:
![Screenshot from 2022-09-23 20-21-46](https://user-images.githubusercontent.com/18479389/191949974-3fe98765-d870-48df-95ea-0676857ab488.png) 

- Connect to Kafka shell with:

         sudo docker exec -it kafka /bin/sh 

- Create a topic with: 

         kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic [name_of_topic]

- List topics in Kafka with:

         kafka-topics.sh --list --zookeeper zookeeper:2181 

![Screenshot from 2022-09-23 20-29-11](https://user-images.githubusercontent.com/18479389/191951023-f3c2cf80-3109-4c79-aecd-b0e5f42a6410.png) 

### **2.3 Install and config InfluxDB**
- Install InfluxDB: 

          $sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -

          $sudo apt update

          $sudo apt install influxdb 

          $sudo systemctl start influxdb #start InfluxDB 

          $sudo systemctl status influxdb  #check status of InfluxDB
After installing, the checking should be:
![Screenshot from 2022-09-23 20-33-44](https://user-images.githubusercontent.com/18479389/191951700-ae07c32f-dc49-4fe3-b498-0f7fcdcc0f0a.png) 
- execute: $influx to enter the InfluxDB shell 
- Show databases with: show databases
- Create databases with: create database [name_data_base]
![308179149_460817562733930_1694019029923324411_n](https://user-images.githubusercontent.com/18479389/191953968-6c9230bb-d9cd-4523-8b84-df1568d7e28c.jpg)
- Install 2 databases: edge_node_status and sensor_data

### **2.4 Install and config Grafana** 
- Grafana is used for visualizing data. We use it to visualize sensor data and status of edge nodes. 
- Install Grafana [Guide Grafana installation](https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/): 

          $sudo apt-get install -y apt-transport-https
          $sudo apt-get install -y software-properties-common wget 
          $sudo wget -q -O /usr/share/keyrings/grafana.key https://packages.grafana.com/gpg.key 
          $echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list

          $sudo apt-get update
          $sudo apt-get install grafana

- Start Grafana server with:

          $sudo systemctl daemon-reload
          $sudo systemctl start grafana-server
          $sudo systemctl status grafana-server
![Screenshot from 2022-09-23 21-04-03](https://user-images.githubusercontent.com/18479389/191956288-e0539d30-cda6-4259-9310-89424a8be702.png)

- From browser: localhost://3000, to enter the webpage of Grafana. Use user: admin, password: admin for the first time of login. Config the new password: sys5583. The interface after creating dashboards:
![Screenshot from 2022-09-23 21-10-25](https://user-images.githubusercontent.com/18479389/191957283-29f42c84-2335-4418-b753-e2d0999064fe.png)
![Screenshot from 2022-09-23 21-08-34](https://user-images.githubusercontent.com/18479389/191956960-b7470f8e-3f36-4b15-b974-3e97c77bca31.png)
Each dashboard can vizualize contents of one database with a few of panels. Go to Configuration > Data sources to add data sources as the following figure. 
![Screenshot from 2022-09-23 21-15-41](https://user-images.githubusercontent.com/18479389/191958100-97a25509-3463-44d0-9677-8429fc6f3854.png)



## **3. Deployment**
In progress 