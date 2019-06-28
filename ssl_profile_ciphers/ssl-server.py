from f5.bigip import ManagementRoot, BigIP
import queue, urllib3, time, threading, json, getpass, requests
urllib3.disable_warnings()
ip='192.168.0.1'
user='admin'
password='password'

def rgetData(vip_info_collection,ip,user,password):
    name = vip_info_collection['name']
    vip_ip = vip_info_collection['destination'].split('/')[2]
    vip_part = vip_info_collection['partition']
    pd_data = [name, vip_ip,vip_part]
    cert_list = []
    profile_list = rgetProfiles(vip_info_collection,ip,user,password)
    pd_data.append(profile_list)
    print(pd_data)

def rgetProfiles(vip_info_collection, ip, user, password):
    pd_data = {}
    profiles = []
    try:

        profile_link = vip_info_collection['profilesReference']['link']
        prof_res = requests.get('https://' + str(ip) + profile_link[17:], auth=(user, password), verify=False)
        p_json = json.loads(prof_res.text)
        print(p_json)
        if not (p_json['items']):
            raise Exception('ITS EMPTY')
        for profile in p_json['items']:
            if 'server' in profile['context']:
                #if 'ssl' in profile['name']:
                profiles.append(profile['name'])

        if profiles:
            pd_data[vip_info_collection['name']] = profiles
        else:
            raise Exception('ITS EMPTY')
    except:
        pd_data[vip_info_collection['name']] = ['No Profile Found']

    return [pd_data]


response_test_all = requests.get('https://' + str(ip) +
                                             '/mgmt/tm/ltm/virtual', auth=(user, password),
                                             verify=False).json()['items']

for x in response_test_all:
    rgetData(x, ip, user, password)