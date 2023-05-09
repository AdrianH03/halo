from netmiko import ConnectHandler
#
# --- Router adatok
# 
routerek_adatok = [{
    'device_type': 'cisco_ios',
    'ip': '172.16.0.5',
    'username': 'TothBela',
    'password': 'TothBela_1000',
    },{
    'device_type': 'cisco_ios',
    'ip': '172.16.0.6',
    'username': 'TothBela',
    'password': 'TothBela_1000',
}]  
routerek = []
ip = []
#
# --- Csatlakozás a routerekhez
#
def csatlakoz(): 
    n = 0
    try:
        for eszkoz in routerek_adatok:
            print(f"\n{eszkoz['ip']}: Csatlakozás folyamatban...")
            routerek.append(ConnectHandler(**eszkoz))
            ip.append(eszkoz['ip'])
            print(f"{eszkoz['ip']}: Sikeres csatlakozás")
            acl_beallit(n)
            n += 1
    except Exception as e:
        print("Hiba történt:\n"+str(e))
#
# --- ACL létrehozása a PAT-hoz
#
def acl_beallit(n):
    print(f"{ip[n]}: Belső ACL konfigurálása folyamatban...")
    # Belső ACL konfigurálás
    acl_belso = '''
    ip access-list standard PAT-inside
    permit 172.16.100.0 0.0.0.127
    permit 172.16.100.128 0.0.0.63
    permit 172.16.100.240 0.0.0.15
    '''
    # Belső ACL parancsok mentése
    routerek[n].send_config_set(acl_belso.splitlines())
    print(f"{ip[n]}: PAT ACL konfiguráció sikeres")
    nat_beallit(n)
#
# --- NAT beállítása az interfészeken
#    
def nat_beallit(n):
    print(f"{ip[n]}: NAT beállítása folyamatban az interfészeken...")
    nat_beallit = '''
    interface GigabitEthernet0/0
    no sh
    ip nat outside
    interface GigabitEthernet2/0
    no sh
    ip nat inside
    interface GigabitEthernet2/0.100
    no sh
    ip nat inside
    interface GigabitEthernet2/0.101
    no sh
    ip nat inside
    interface GigabitEthernet2/0.102
    no sh
    ip nat inside
    ip nat inside source list PAT-inside interface GigabitEthernet0/0 overload
    '''
    routerek[n].send_config_set(nat_beallit.splitlines())
    print(f"{ip[n]}: NAT beállítva")
    ment(n)
#
# --- Konfiguráció mentése, illetve a kapcsolatok megszakítása
#    
def ment(n):
        print(f"{ip[n]}: Konfiguráció mentése folyamatban...")
        routerek[n].save_config()
        print(f"{ip[n]}: Változtatások sikeresen mentve a konfigfájlba")
        routerek[n].disconnect()    
        print(f"{ip[n]}: Kapcsolat vége")
# --- Alapprogram
csatlakoz()
print("\nVáltoztatások elmentve a konfigfájlokba az összes routeren, kapcsolatok megszakítva")
print("Script sikeresen lefutott")