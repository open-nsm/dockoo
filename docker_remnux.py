#!/usr/bin/python

# To run this script, install and start Docker first.  You also need to
# get the Docker images you want to run.  You can do this with a command
# like "docker pull remnux/pescanner"

import docker
import ConfigParser
import time
from os import path
import docker.tls as tls

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

# Docker or docker-machine
docker_exec = config.get("docker", "docker_exec")

# The command to run -- add options later?
command2run = command_line_exe + " " + malware_file

c = docker.Client()

# Make a connection to docker
if (docker_exec.lower() == 'docker'):
    c = docker.Client(base_url='unix://var/run/docker.sock')

# Make a connection to docker-machine
if (docker_exec.lower() == 'docker-machine'):
    ip_address = config.get("docker", "ip_address")
    port = config.get("docker", "port")
    address_str = 'https://' + ip_address + ':' + port
    certs = config.get("docker", "cert_path")
    tls_config = tls.TLSConfig(
        client_cert=(path.join(certs, 'cert.pem'), path.join(certs,'key.pem')),
        ca_cert=path.join(certs, 'ca.pem'),
        verify=True,
        assert_hostname=False
    )
    c = docker.Client(base_url=address_str, tls=tls_config)

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
