from f5.bigip import ManagementRoot

mgmt = ManagementRoot('ip-address-here', 'username-here', 'password-here')
ltm = mgmt.tm.ltm

client_ssl = ltm.profile.client_ssls.get_collection()

cipher_str = (
    '-ALL:!SSLv2:!SSLv3:!TLSv1:'
    'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:'
    'ECDHE-RSA-AES128-CBC-SHA:ECDHE-RSA-AES256-CBC-SHA')

for profile in client_ssl:
    profile_cert_name = (profile.certKeyChain[0]['name'])
    with open('sslprofiles.txt') as file_input:
        names_in_file = file_input.read()
        if profile_cert_name in names_in_file:
            print(profile_cert_name)
            profile.ciphers = cipher_str
            profile.update()
