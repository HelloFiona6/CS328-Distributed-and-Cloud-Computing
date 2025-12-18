#!/bin/bash

hdfs dfs -copyFromLocal resources/text.txt /
echo "uploaded file to HDFS!"

echo "showing current contents in HDFS root (/)"
hdfs dfs -ls /

