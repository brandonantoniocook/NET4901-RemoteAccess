#!/usr/bin/python3

#"""TermServer.py: Napalm auto configuration of terminal server tty lines."""

#__author__      = "Brandon Antonio Cook"
#__copyright__   = "Copyright 2018, YARN"

import os
import datetime
from netmiko import ConnectHandler

#------------------------------------------------------
#CREATE MERGE FILES PER POD BASIS
#------------------------------------------------------
def mediaryConfigAdditions(podNumber, Password):

  #Add the proper configurations for each line/pod
  if podNumber == 'pod1':
    open('pod1.cfg', 'w').close()
    f=open("pod1.cfg", "a")
    for x in range(0,8):
          f.write('!\nline 1/' + str(x) + '\n  exec-timeout 0 0\n  password ' + Password)
          f.write('\n  login authentication PODS\n  rotary ' + str(x+1) + '\n  no exec\n  transport input ssh\n')
    f.close()
    NAPALM_MERGE('1')
    os.remove('pod1.cfg')

  if podNumber == 'pod2':
    open('pod2.cfg', 'w').close()
    f=open("pod2.cfg", "a")
    for x in range(8,16):
          f.write('!\nline 1/' + str(x) + '\n  exec-timeout 0 0\n  password ' + Password)
          f.write('\n  login authentication PODS\n  rotary ' + str(x+2) + '\n  no exec\n  transport input ssh\n')
    f.close()
    NAPALM_MERGE('2')
    os.remove('pod2.cfg')

  if podNumber == 'pod3':
    open('pod3.cfg', 'w').close()
    f=open("pod3.cfg", "a")
    for x in range(16,24):
          f.write('!\nline 1/' + str(x) + '\n  exec-timeout 0 0\n  password ' + Password)
          f.write('\n  login authentication PODS\n  rotary ' + str(x+4) + '\n  no exec\n  transport input ssh\n')
    f.close()
    NAPALM_MERGE('3')
    os.remove('pod3.cfg')

#------------------------------------------------------
#MERGE CONFIGURATION COMMIT
#------------------------------------------------------
def NAPALM_MERGE(num):

  #CREATE LOG FILE IF NOT ALREADY CREATED
  now = datetime.datetime.now()
  file = open('yarn_terminal.log', 'w+')

  #OPEN THE CONNECTION
  from napalm import get_network_driver

  #LOAD THE DRIVER
  try:
    print('Loading the Driver...')
    driver = get_network_driver('ios')
  except e:
    print (e)
    file.write(str(now) + e + "Failpoint: Loading the Driver...")

  #ASSIGN SSH PORT
  try:
    print ('Assigning Non-Standard SSH Port...')
    optional_args = {'port': "22"}
  except e:
    print (e)
    file.write(str(now) + e + "Failpoint: Assigning Non-Standard SSH Port...")

  #LOAD CONNECTION SETTINGS
  try:
    print ('Loading Connection Settings...')
    device = driver('172.20.5.4', 'console01', '7554306100$#@!', optional_args=optional_args)
  except e:
    print (e)
    file.write(str(now) + e + "Failpoint: Loading Connection Settings...")

  #OPEN THE CONNECTION
  try:
    print ('Opening the Connection...')
    device.open()
  except e:
    print (e)
    file.write(str(now) + e + "Failpoint: Opening the Connection...")

  #PREPARE MERGE CONFIGURATION
  try:
    print ('Merging the Configuration...')
    device.load_merge_candidate(filename='pod' + num + '.cfg')
  except e:
    print (e)
    file.write(str(now) + e + "Failpoint: Merging the Configuration...")

  #COMPARE THE CONFIGURATION
  try:
    print ('Comparing Config...')
    print (device.compare_config())
  except e:
    print (e)
    file.write(str(now) + e + "Failpoint: Comparing Config...")

  #COMMIT THE CONFIGURATION
  try:
    print ('Committing the New Config...')
    device.commit_config()
  except e:
    print (e)
    file.write(str(now) + e + "Failpoint: Committing the New Config...")

  #CLOSE THE CONNECTION
  try:
    print ('Closing the Connection...')
    device.close()
  except e:
    print (e)
    file.write(str(now) + e + "Failpoint: Closing the Connection...")

  #------------------------------------------------------
  #Kick off prior users
  #------------------------------------------------------

  #Set device connection params
  termServ = {
      'device_type': 'cisco_ios',
      'ip': '172.20.5.4',
      'username': 'console01',
      'password': '7554306100$#@!',
      'port': 2222,
  }
  #Connect to device
  net_connect = ConnectHandler(**termServ)
  net_connect.find_prompt()

  #Close prior connections
  if num == 'pod1':
    for x in range(0,8):
          output = net_connect.send_command_timing("clear line 1/" + str(x))
          if output == '[confirm]':
              output += net_connect.send_command_timing("y")
  if num == 'pod2':
    for x in range(8,16):
          output = net_connect.send_command_timing("clear line 1/" + str(x))
          if output == '[confirm]':
              output += net_connect.send_command_timing("y")
  if num == 'pod3':
    for x in range(16,24):
          output = net_connect.send_command_timing("clear line 1/" + str(x))
          if output == '[confirm]':
              output += net_connect.send_command_timing("y")
