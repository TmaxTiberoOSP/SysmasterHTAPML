#!/bin/bash 

export JAVA_HOME=/usr/lib/jdk-21.0.3/
export PATH=$JAVA_HOME/bin:$PATH

./mvnw clean package -P mysql
cd target
tar -xvf benchbase-mysql.tgz

