 # Import the F5 module (Use pip to install> pip install f5-sdk)
from f5.bigip import ManagementRoot

# Define unique variables
user = 'admin'
password = 'password'
active_f5 = []

# Find the active F5
for f5_ip in ['192.168.0.1', '192.168.0.2', '192.168.0.3', '192.168.0.4']:
    mgmt = ManagementRoot(f5_ip, user, password)
    fail = mgmt.tm.sys.failover.load()
    failOverStat = fail.apiRawValues['apiAnonymous'].rstrip()
    #print(f5_ip, mgmt.tmos_version, failOverStat)
    if "active" in failOverStat:
        active = f5_ip
        active_f5.append(active)

print(active_f5)


# Connect to the active F5s
for mgmt_ip in active_f5:
    mgmt = ManagementRoot(mgmt_ip, user, password)
    ltm = mgmt.tm.ltm

#serverIP = "192.168.101.182"

# First remove the node from all pools
    def del_pool_member():
        pools = ltm.pools.get_collection()
        for pool in pools:
            #print(pool.name)
            for member in pool.members_s.get_collection():
                if serverIP in member.address:
                    print("Removing " + member.name + " from " + "/" + member.partition + "/" + pool.name)
                    #member.delete()

# Second delete the node
    def del_node():
        nodes = ltm.nodes.get_collection()
        for node in nodes:
            #print(node.address)
            if serverIP in node.address:
                print("Deleting " + node.name)
                #node.delete()
            
                #Third validate
                #check = ltm.nodes.node.exists(partition=node.partition, name=node.name)
                #print("{} still exist? {}".format(serverIP, check))

# Import list of IP addresses (one per line) to use for serverIP 
    with open("ip.txt", "r") as file:
        for serverIP in file:
            serverIP = serverIP.strip()
            del_pool_member()
            del_node()
