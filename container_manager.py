#! /usr/bin/python
# container_manager is part of the dockoo system
# For Open-NSM and Senior Thesis at UIUC
# November 1, 2015
# SEE https://github.com/open-nsm/dockoo.git FOR MORE INFO
import sys
__author__ = 'Shane Rogers'


#  This function takes as input the name of a malware file located in dockoo/malware/
#  and the name of malware container image and spins the container up while passing the malware to it.
#  WARNING
#  This function does not currently sanitize user input in any way, so if you
#  give it a funny value for the malware file name or try to create a container
#  from a nonexistent image, it will break.  Send questions or comments to shane@shanerogers.info

class ContainerMan():
    def __init__(self, malware_file, image_name):
        self.malware_file = malware_file
        self.image_name = image_name

    def start_container(self):
        self.a_container_is_running = True
        os.system("docker start %s" % self.image_name)
    def stop_container(self):
        os.system("docker stop --time=30 %s" % self.image_name)
        os.system("docker rm %s" % self.image_name)

def main():
    # Check to make sure user passed in a pcap file
    if len(sys.argv) != 3:
        print("Usage: ./container_manager <malware filename> <docker image name>")
        print "For more info try: ./container_manager --help"
        exit()

    if sys.argv[1] == "--help":
        print "#  This function takes as input the name of a malware file located in dockoo/malware/"
        print "#  and the name of malware container image and spins the container up while passing the malware to it."
        print "#  WARNING"
        print "#  This function does not currently sanitize user input in any way, so if you"
        print "#  give it a funny value for the malware file name or try to create a container"
        print "#  from a nonexistent image, it will break.  Send questions or comments to shane@shanerogers.info"
        exit()

    else:
        malware_file = sys.argv[1]
        image_name = sys.argv[2]
        dockoo_container = ContainerMan(malware_file, image_name)


if __name__ == "__main__":
    main()
