from f5.bigip import ManagementRoot

mgmt = ManagementRoot('192.168.0.1', 'admin', 'password')
ltm = mgmt.tm.ltm

client_ssl = ltm.profile.client_ssls.get_collection()

cipher_str = (
    '-ALL:!SSLv2:!SSLv3:!TLSv1:'
    'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:'
    'ECDHE-RSA-AES128-CBC-SHA:ECDHE-RSA-AES256-CBC-SHA')
print("Ciphers Should Match: " + cipher_str)
print("********************* ")
for profile in client_ssl:
    client_ssl_profile_ciphers = (profile.ciphers)
    profile_cert_name = (profile.certKeyChain[0]['name'])
    if client_ssl_profile_ciphers != cipher_str: #and profile_cert_name != "default":
        print("Cert.CN: " + profile_cert_name + " Ciphers:" + profile.ciphers)
    elif client_ssl_profile_ciphers == cipher_str and profile_cert_name != "default":
        print("Cert.CN: " + profile_cert_name + " Ciphers:MATCH**************")
