from netmiko import ConnectHandler

# SZHELY1 belépési adatok
router_szhely1 = {
    'device_type': 'cisco_ios',
    'ip': '172.16.100.241',
    'username': 'your_username',
    'password': 'your_password',
}

# SZHELY2 belépési adatok
router_szhely2 = {
    'device_type': 'cisco_ios',
    'ip': '172.16.100.242',
    'username': 'your_username',
    'password': 'your_password',
}

# Csatlakozás a routerekhez
szhely1 = ConnectHandler(**router_szhely1)
szhely2 = ConnectHandler(**router_szhely2)

# Belső ACL konfigurálása
acl_belso = '''
ip access-list standard PAT-inside
 permit 172.16.100.0 0.0.0.127
 permit 172.16.100.128 0.0.0.63
 permit 172.16.100.240 0.0.0.15
'''
# Belső ACL parancsok mentése
szhely1.send_config_set(acl_belso.splitlines())
szhely1.send_command('write memory')
szhely2.send_config_set(acl_belso.splitlines())
szhely2.send_command('write memory')

# NAT inside, overload beállítása
# NAT outside interface-t majd be kell állítani a megfelelőre
nat_beallit = '''
interface GigabitEthernet0/0/0
ip nat outside
exit
interface GigabitEthernet0/2.100
ip nat inside
exit
interface GigabitEthernet0/2.101
ip nat inside
exit
interface GigabitEthernet0/2.102
ip nat inside
exit
ip nat inside source list pat-inside interface GigabitEthernet0/0/0 overload
exit
'''
szhely1.send_config_set(nat_beallit.splitlines())
szhely1.send_command('write memory')
szhely2.send_config_set(nat_beallit.splitlines())
szhely2.send_command('write memory')

# Configure ACLs on Router1 
# GPT által generált, törölhető majd
acl_inside_cmd_router1 = 'access-list acl-inside permit ip source-ip source-wildcard'
acl_inside_router1 = 'access-list acl-inside permit ip 172.16.100.0 0.0.0.127 any'
acl_outside_cmd_router1 = 'access-list acl-outside permit ip source-ip source-wildcard'
acl_outside_router1 = 'access-list acl-outside permit ip any any'
acl_inside_cmd_router1_vlan101 = 'access-list acl-inside permit ip source-ip source-wildcard'
acl_inside_router1_vlan101 = 'access-list acl-inside permit ip 172.16.100.240 0.0.0.15 any'
acl_inside_cmd_router1_vlan102 = 'access-list acl-inside permit ip source-ip source-wildcard'
acl_inside_router1_vlan102 = 'access-list acl-inside permit ip 172.16.100.128 0.0.0.63 any'
szhely1.send_config_set([acl_inside_cmd_router1, acl_inside_router1,
                                     acl_outside_cmd_router1, acl_outside_router1,
                                     acl_inside_cmd_router1_vlan101, acl_inside_router1_vlan101,
                                     acl_inside_cmd_router1_vlan102, acl_inside_router1_vlan102])

# Configure ACLs on Router2
# GPT által generált, törölhető majd

acl_inside_cmd_router2 = 'access-list acl-inside permit ip source-ip source-wildcard'
acl_inside_router2 = 'access-list acl-inside permit ip 172.16.100.0 0.0.0.127 any'
acl_outside_cmd_router2 = 'access-list acl-outside permit ip source-ip source-wildcard'
acl_outside_router2 = 'access-list acl-outside permit ip any any'
acl_inside_cmd_router2_vlan101 = 'access-list acl-inside permit ip source-ip source-wildcard'
acl_inside_router2_vlan101 = 'access-list acl-inside permit ip 172.16.100.240 0.0.0.15 any'
acl_inside_cmd_router2_vlan102 = 'access-list acl-inside permit ip source-ip source-wildcard'
acl_inside_router2_vlan102 = 'access-list acl-inside permit ip 172.16.100.128 0.0.0.63 any'
szhely2.send_config_set([acl_inside_cmd_router2, acl_inside_router2,
                                     acl_outside_cmd_router2, acl_outside_router2,
                                     acl_inside_cmd_router2_vlan101, acl_inside_router2_vlan101,
                                     acl_inside_cmd_router2_vlan102, acl_inside_router2_vlan102])

# NAT konfigurálás - lehet törölhető
nat_konfig = 'ip nat inside source list acl-inside interface GigabitEthernet0/1 overload'
szhely1.send_command(nat_konfig)
szhely2.send_command(nat_konfig) 