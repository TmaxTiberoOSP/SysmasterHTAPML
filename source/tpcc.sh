#!/bin/bash

export JAVA_HOME=/usr/lib/jdk-21.0.3/
export PATH=$JAVA_HOME/bin:$PATH

cd target
cd benchbase-mysql
java -jar benchbase.jar -b tpcc -c config/tibero/tpcc.xml --create=true --load=true --execute=true

