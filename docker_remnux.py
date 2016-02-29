#!/usr/bin/python

# To run this script, install and start Docker first.  You also need to
# get the Docker images you want to run.  You can do this with a command
# like "docker pull remnux/pescanner"

import docker
import ConfigParser
import time
# For running on OSX docker-machine uncomment imports below
#from os import path
#import docker.tls as tls

# Location of config file
cfgfile = "remnux.conf"

# File to be analyzed
malware_file = "1d53a61b4ec187230f23fd66076ff605"

# Docker tool to use
docker_tool = "pescanner"

# Read in parameters from the config file
config = ConfigParser.ConfigParser()
config.read(cfgfile)
container_name = config.get(docker_tool, "container_name")
local_working_dir = config.get(docker_tool, "local_working_dir")
docker_bind_dir = config.get(docker_tool, "docker_bind_dir")
command_line_exe = config.get(docker_tool, "command_line_exe") 
options = config.get(docker_tool, "options")
mode = config.get(docker_tool, "mode")

# The command to run -- add options later?
command2run = command_line_exe + " " + malware_file

# Make a connection to Docker
c = docker.Client(base_url='unix://var/run/docker.sock')

# For docker-machine on OSX, this should work but will 
# throw "InsecureRequestWarning" errors.
# Probably not that big a deal for developing/debugging for now.  
# As docker-machine matures, maybe a better solution will become available.
# IP address and port comes from command "docker-machine env default". 
# Should be added to conf file at some point.
# For running on OSX comment out line above uncomment code below

#CERTS = CERTS = path.join(path.expanduser('~'), '.docker', 'machine', 'machines', 'default')
#tls_config = tls.TLSConfig(
#    client_cert=(path.join(CERTS, 'cert.pem'), path.join(CERTS,'key.pem')),
#    ca_cert=path.join(CERTS, 'ca.pem'),
#    verify=False
#)
#c = docker.Client(base_url='https://192.168.99.100:2376', tls=tls_config)

# Grab the image
c.images(container_name)

# Create a container based on parameters
cntnr = c.create_container(
   container_name, command2run, volumes=[docker_bind_dir],
    host_config=c.create_host_config(binds={
        local_working_dir: {
            'bind': docker_bind_dir,
            'mode': mode,
        }
    })
)

# Start the container
c.start(cntnr)

# Wait for container to finish executing before accessing logs
containers = c.containers()
# For now, just see if there are any containers executing
num_containers = len(containers)
while (num_containers > 0):
   time.sleep(1)
   containers = c.containers()
   num_containers = len(containers)

# Access output logs
output = c.logs(cntnr)
print(output)

