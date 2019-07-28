---
title: 'A Simple Network of Docker Containers'
date: 2019-07-08
permalink: /posts/2019/07/docker-network/
tags:
  - docker
  - virtual-network
---
The goal of this article is to illustrate a basic Docker configuration
that simulates a network of virtual devices.
For sake of simplicity, each Docker container runs the same application,
however, it is possible to run containers with different applications.
Having a large network helps studying the behavior of distributed algorithms
without handling physical or virtual machines.
In addition, I also discuss a simple way to logging in a scalable manner.

I faced this problem in a recent research project where I needed to simulate a large
number of IoT devices.
The application developed, basically, implemented a [Distributed Hash Table][3].
This configuration enabled me to measure large scale properties,
such as logarithmic research and network traffic.
All of these without running out of grants :)

In this article, I will use a dummy network application.
I however plan to release the full open source code, along with the research
paper, after acceptance.

**NOTE**  
You can save all the following scripts and configuration files
in the same folder and run all the commands in the that folder.

**TL;TR;**  
To make the work easier for the laziest, I made a small repository with all the following examples at this [link](https://github.com/tregua87/DockerNetwork).

**To sum up, what you will find in this article is:**
- Basic Docker container configuration.
- Practical tips for handling networks of Docker containers.
- Defining and managing a network of Docker containers, in particular:
  - How to start/stop the network in a controlled way.
  - Collect logs in a scalable fashion.

The rest of the post is organized as follows:
- [Overview](#overview)
- [Preliminaries](#preliminaries)
- [Entry Point](#entry-point)
- [Docker Image](#docker-image)
- [Network Configuration](#network-configuration)
- [Start-stop and network control](#start-stop-and-network-control)
- [Log Collection](#log-collection)

## Overview ##

First thing first, let me describe what we are going to do.  
Our network is composed by a number X of devices, called **peers**.
The peers communicate with a central node, called **entry point**.
Technically speaking, the entry point is implemented by our PC.
The peers are, instead, implemented by docker containers.  
The network can be depicted as follows.
![A Network!](https://docs.google.com/drawings/d/e/2PACX-1vTftn7rqcM65FiUHK_ldUlmpH1XNu-Y7_1-X9rUsG9TjGOg8PUKqvHiylXwj-MyZkc2xFpSuWtZL3y7/pub?w=702&h=451)

The purpose of this network is simple but still important.
The entry point listens to communications from the peers.
Meanwhile, the peers contact the entry point.
During the execution, both peers and entry point write a local log file
(i.e., in the respective container). Then, I will collect their log after
an experiment session.

## Preliminaries ##

Before going to the meat, we need some preliminary installation.
If you have already installed these tings, then, go ahead!  
Docker is a quite flexible technology that allows installing so-called
containers.
In a nutshell, a container is an object that provides all the needs for the
application, while it relies on the host OS kernel.
In my experiments, I used a classic Ubuntu 18.04.
The application is written in Python and requires Flask, while
the network is handled by *Docker compose*.

To install the requirements, just open a terminal and let's start with Docker.
I referred to this [guide][1].
```
sudo apt-get install  curl apt-transport-https ca-certificates software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce
sudo systemctl status docker
# to avoid further issues, we set ourselves as docker users
sudo groupadd docker # this may return an error
sudo usermod -aG docker $USER


```
For *Docker compose*, I followed this [guide][2].
```
# install curl, who never knows
sudo apt update && sudo apt install curl
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
# restart the shell
docker-compose --version
```
NOTE: afaik, new versions of Docker should allow handling groups of containers
like Docker compose does. However, I found much easier this approach.

For Python and Flask, instead, the things are much simpler:
```
sudo apt update
sudo apt install python3 python3-pip
pip3 install flask
```

## Entry Point ##
The entry point is a simple Web browser written in Python3 and Flask.
Let's have a look to this simple code.
```
#!/usr/bin/python3
import sys
import socket
from flask import Flask, request

app = Flask(__name__)

if len(sys.argv) != 2:
    print("usage: {0} <logfile>".format(sys.argv[0]))
    exit(0)

peerips = sys.argv[1]

@app.route('/add')
def add():
    global peerips
    # ip = request.args.get('peer-ip')
    ip = request.remote_addr
    if ip:
        with open(peerips, 'a') as l:
            l.write(ip + "\n")
        return "done"
    return "miss peer-ip"

app.run(debug=True, port=2222, host='0.0.0.0')
```
Just dump the former code in a file, e.g., `app_pc.py`. It will be useful later.

Also, don't forget.
```
chmod +x ./app_pc.py
```

The scope of the entry point is quite simple, it receives a *ping* from the peers
and makes a local log.
Clearly, this is just an example to show how peers and entry point exchange messages.

## Docker Image ##

As stated before, any peer is a Docker container.

Basically, create a new file, called `Dockerfile`, and dump inside the following text.
```
FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install wget -y

RUN mkdir -p /home/peer
COPY . /home/peer/

CMD wget 172.20.0.2:2222/add; sleep 50; echo "My IP is `hostname -I | awk '{print $1}'`" > local.txt
```
The peer is quite simple. When it boots, it will contact the entry point by using
a `wget`. This action sends the peer IP to the entry point, which is then logged.

From the Dockerfile previously described, we create a Docker image by throwing:
```
docker build -t "docker-network-peer" .
```

## Network Configuration ##

Docker-compose can help handling interesting and complex sets of containers.
In this setting, we use this tool to run and stop an arbitrary
number of peers.
One of the most useful thing of docker-compose is the ability
to group a lot of boring setting in a simple configuration file
called `docker-compose.yml`.
In my case, I used docker-compose to setting a virtual network called `docker-network-test` and to run/stop the peers.

Save a `docker-compose.yml` file with the following content:
```
version: '2.4'

services:
  peer:
    image: docker-network-peer:latest
    networks:
     - docker-network-test

networks:
    docker-network-test:
      driver: bridge
      ipam:
        driver: default
        config:
          - subnet: 172.20.0.0/16
            gateway: 172.20.0.2
```
In the next session, we see how to run the entire network.

## Start-stop and network control ##

Open a shell and start the entry point:
```
python3 app_pc.py entrypoint.txt
```
In another shell, launch the peers:
```
docker-compose up --scale peer=10
```
The former command launches 10 peers.
Then, wait until everything finishes.
Finally, close the server with a classic `ctrl+c`.

In my example, each peer shuts down itself.
If your peer application is meant to run for an undetermined time, you can use a command like that:
```
docker-compose up --scale peer=10; sleep 60; docker-compose stop
```
This command runs 10 peers, sleep for 60 seconds, and then stop itself.

After the execution, we have this situation:
1. each Docker container has a local log file
2. the entry point has its own log file, which is saved in the host.

## Log Collection ##

To collect and inspect the logs, we can do:

**Entry points**  
This is pretty simple, the entry point saves its log in the host machine.
So, you can read it in this way:
```
cat entrypoint.txt
```

**Peers**  
Each peer saves its log in the container, which is basically a file system not normally accessible from the host.
For instance, to read the log from the container 1, you can use the following command.
```
docker cp dockernetwork_peer_1:/local.txt ./log1.txt
```
It is possible to automatize the log extraction by using the following script:
```
#!/bin/bash

NDEV=$1

echo "NDEV: $NDEV"

for i in `seq $NDEV`; do
  echo $i
  docker cp dockernetwork_peer_$i:/local.txt ./log\_$i.txt
done;
```
Just save this code in a script called `extractlog.sh`.
Then, give some execution permission:
```
chmod +x extractlog.sh
```
This script just copies the local logs of each container to the host in the following way:
```
./extractlog.sh 10
```

[1]: https://www.hostinger.com/tutorials/how-to-install-and-use-docker-on-ubuntu/ "Docker installation"
[2]: https://docs.docker.com/compose/install/ "Docker compose installation"
[3]: https://en.wikipedia.org/wiki/Distributed_hash_table "Distributed Hash Table"
