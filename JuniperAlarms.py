import netmiko
from getpass import getpass

''' User input for password not displayed on screen '''
def define_password():
    password = None
    while not password:
        password = getpass('Enter TACACS+ Password: ')
        passwordverify = getpass('Re-enter TACACS+ Password to Verify: ')
        if not password == passwordverify:
            print('Passwords Did Not Match Please Try Again')
            password = None
    return password

''' Formatting devices.txt into list to be passed to for loop '''
def reformat_devices(devices):
    devices = devices.read()
    devices = devices.strip().splitlines()
    return devices

''' Common exceptions that could cause issues'''
exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
              netmiko.ssh_exception.NetMikoAuthenticationException)

print('~'*79)
print('~'*29+' Juniper Alarm Check '+'~'*29)
print('~'*79)
''' Get Variables '''
username = input('Enter TACACS+ Username: ')
password = define_password()
devices = open('.\\devices\\devices.txt','r')
devices = reformat_devices(devices)
device_type = 'juniper_junos'
''' Loop for devices '''
for device in devices:
    try:
        ''' Connection Break '''
        print('*'*79)
        print('Connecting to:',device)
        ''' Connection Handler '''
        connection = netmiko.ConnectHandler(ip=device, device_type=device_type, username=username, password=password)
        ''' Sending config commands to device '''
        output = connection.send_command('show system alarms')
        if 'No alarms currently active' in output:
            print('No Active System Alarms')
        else:
            print(output)
        output = connection.send_command('show chassis alarms')
        if 'No alarms currently active' in output:
            print('No Active Chassis Alarms')
        else:
            print(output)

    except exceptions as exception_type:
        print('Failed to ', device, exception_type)
print('*'*79)
