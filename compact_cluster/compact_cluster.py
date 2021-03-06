#Compact cluster
#Removes a host from a cluster
import json
import sys
import time
import requests


def get_request(url,username,password):
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers,auth=(username, password))
    if(response.status_code == 200):
        data = json.loads(response.text)
    else:
        print ("Error reaching the server.")
        exit(1)
    return data

def post_request(data,url,username,password):
    headers = {'Content-Type': 'application/json'}
    print (url)
    print (data)
    response = requests.post(url, headers=headers, json=data, auth=(username, password))
    if(response.status_code == 200):
        data = json.loads(response.text)
    else:
        print ("Error reaching the server.")
        response = json.loads(response.text)
        print (json.dumps(response,indent=4, sort_keys=True))
        exit(1)
    return data


def poll_on_id(url,username,password):
    status = get_request(url,username,password)['status']
    c = 0
    while(status == 'IN_PROGRESS'):
        c = c+1
        n = c%6
        print ("\rOperation in progress","."*n," "*(5-n),end = '')
        status = get_request(url,username,password)['status']
        time.sleep(5)
    print()
    return status


def compact_cluster(hostname,username,password,cluster_id):
    data = read_input()
    url =  hostname+'/v1/clusters/'+cluster_id+'/validations/updates'
    headers = {'Content-Type': 'application/json'}
    response = post_request(data,url,username,password)
    print ("Validating the input....")
    if(response['executionStatus'] == 'COMPLETED' and response['resultStatus'] == 'SUCCEEDED'):
        print ('Validation Succeeded.')
    else:
        print ('Validation failed.')
        print (json.dumps(response,indent=4, sort_keys=True))
        exit(0)

    url = hostname + '/v1/clusters/'+cluster_id
    response = requests.patch(url, headers=headers, data=data, auth=(username, password))
    if(response.status_code == 202):
        print ('Compactiong Cluster...')
    else:
        print ('Compacting cluster failed.')
        print (response.text)
        exit(0)
    task_id = response['id']
    url = hostname+'/v1/tasks/'+task_id
    result = poll_on_id(url,username,password)
    if(result == 'SUCCESSFUL'):
        print ('Successfully compacted cluster.')
    else:
        print ('Cluster Compactiong failed.')
        response = json.loads(response.text)
        print (json.dumps(response,indent=4, sort_keys=True))
        print (result)

#cluster_compaction_spec.json is the preconfigured input spec file.
def read_input():
    with open('compact_cluster_spec.json') as json_file:
        data = json.load(json_file)
        return data

def get_help():
    help_description = '''\n\t\t----Compact Cluster----
    Usage:
    python compact_cluster.py <hostname> <username> <password> <cluster_id>\n Refer to documentation for more detais\n'''
    print (help_description)


def action_performer():
    arguments = sys.argv
    if(len(arguments) < 3):
        get_help()
        return
    hostname = 'https://'+arguments[1]
    username = arguments[2]
    password = arguments[3]
    cluster_id = arguments[4]
    compact_cluser(hostname,username,password,cluster_id)
    return

action_performer()
