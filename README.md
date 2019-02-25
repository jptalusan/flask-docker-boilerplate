trying to setup a flask + dockers + flask-socketio + gunicorn + redis service and redis connection boilerplate  

Because i am tired of having to relearn everything everytime I have to add a new implementation to this system.  

-----  
Problems:  

Need to create a mosquitto.log file with the following permissions...  

mkdir mosquitto/log  
cd mosquitto/log  
sudo touch mosquitto.log  
sudo chown 1883:1883 ../../mosquitto/log -R  

