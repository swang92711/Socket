#!/usr/bin/python


import argparse
import subprocess
import threading


dns_server="cs5700cdnproject.ccs.neu.edu"


http_servers=[]
http_servers.append('ec2-52-90-80-45.compute-1.amazonaws.com')
http_servers.append('ec2-54-183-23-203.us-west-1.compute.amazonaws.com')
http_servers.append('ec2-54-70-111-57.us-west-2.compute.amazonaws.com')
http_servers.append('ec2-52-215-87-82.eu-west-1.compute.amazonaws.com')
http_servers.append('ec2-52-28-249-79.eu-central-1.compute.amazonaws.com')
http_servers.append('ec2-54-169-10-54.ap-southeast-1.compute.amazonaws.com')
http_servers.append('ec2-52-62-198-57.ap-southeast-2.compute.amazonaws.com')
http_servers.append('ec2-52-192-64-163.ap-northeast-1.compute.amazonaws.com')
http_servers.append('ec2-54-233-152-60.sa-east-1.compute.amazonaws.com')



def main(args):
    #Clear CDN
    cdn_clear_command="ssh -i "+args.keyfile+" "+args.username+"@"+dns_server+ "  rm -rf DNS"
    subprocess.call(cdn_clear_command,shell=True)
    #Deploy CDN
    cdn_deploy_command="tar -czf - DNS/ | ssh -i "+args.keyfile+" "+args.username+"@"+dns_server+" tar -xzf -"
    subprocess.call(cdn_deploy_command,shell=True)

    thread_list=[]
    for server in http_servers:
        thread = threading.Thread(target=deploy_http,args=(server,))
        thread.setDaemon(True)
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    '''
    #Clear
    for server in http_servers:
        http_clear_command = "ssh -i " + args.keyfile + " " + args.username + "@" + server + " rm -rf HTTP"
        subprocess.call(http_clear_command, shell=True)
    '''





def deploy_http(server):
    # Clear CDN
    http_clear_command = "ssh -i " + args.keyfile + " " + args.username + "@" + server + "  rm -rf HTTP"
    subprocess.call(http_clear_command, shell=True)
    # Deploy CDN
    http_deploy_command = "tar -czf - HTTP/ | ssh -i " + args.keyfile + " " + args.username + "@" + server + " tar -xzf -"
    subprocess.call(http_deploy_command, shell=True)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="__deployCDN -p <port> -o <origin> -n <name> -u <username> -i <keyfile>");
    parser.add_argument("-p", "--port", type=int)
    parser.add_argument("-o","--origin",type=str)
    parser.add_argument("-n","--name",type=str)
    parser.add_argument("-u","--username",type=str)
    parser.add_argument("-i","--keyfile",type=str)
    args=parser.parse_args()
    main(args)

