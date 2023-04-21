#!/bin/bash

#give permission for everything in the express-app directory
sudo chmod -R 777 /home/ec2-user/MyDrive

#navigate into our working directory where we have all our github files
cd /home/ec2-user/MyDrive


#start our node app in the background
python3 mainFile.py > mainFile.out.log 2> mainFile.err.log < /dev/null &