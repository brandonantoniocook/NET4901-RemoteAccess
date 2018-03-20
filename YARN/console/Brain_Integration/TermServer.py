#!/usr/bin/python3

"""TermServer.py: Napalm auto configuration of terminal server tty lines."""

__author__      = "Brandon Antonio Cook"
__copyright__   = "Copyright 2018, YARN"

import os

def configurationCreate(pod1Pass, pod2Pass, pod3Pass):

  #Create Full Configuration File
  open("YARN_TERMINAL_SERVER.cfg", "w").writelines([l for l in open("TestBaseScript.txt").readlines()])

  #Open the file to be written to.
  f=open("YARN_TERMINAL_SERVER.cfg", "a")

    #Add the proper configurations for each line/pod
  for x in range(0, 8):
      f.write('!\nline 1/' + str(x) + '\n  exec-timeout 0 0\n  password ' + pod1Pass)
      f.write('\n  login authentication PODS\n  rotary ' + str(x+1) + '\n  no exec\n  transport input ssh\n')

  for y in range(8, 16):
      f.write('!\nline 1/' + str(y) + '\n  exec-timeout 0 0\n  password ' + pod2Pass)
      f.write('\n  login authentication PODS\n  rotary ' + str(y+2) + '\n  no exec\n  transport input ssh\n')

  for j in range(16, 24):
      f.write('!\nline 1/' + str(j) + '\n  exec-timeout 0 0\n  password ' + pod3Pass)
      f.write('\n  login authentication PODS\n  rotary ' + str(j+4) + '\n  no exec\n  transport input ssh\n')

  #Add the Remainder of the Configuration File Contents
  f.write('line vty 0 4\n transport input ssh\n transport output ssh\n!\nscheduler allocate 20000 1000\n end\n')
  f.close()

  #Commit the Changes
  NAPALM_CONFIG()

def mediaryConfigAdditions(podNumber, Password):

  #Add the proper configurations for each line/pod
  if podNumber == 'pod1':
    open('pod1.cfg', 'w').close()
    f=open("pod1.cfg", "a")
    for x in range(0,8):
          f.write('!\nline 1/' + str(x) + '\n  exec-timeout 0 0\n  password ' + Password)
          f.write('\n  login authentication PODS\n  rotary ' + str(x+1) + '\n  no exec\n  transport input ssh\n end\n')
    f.close()
    NAPALM_MERGE('1')
    os.remove('pod1.cfg')
  
  if podNumber == 'pod2':
    open('pod2.cfg', 'w').close()
    f=open("pod2.cfg", "a")
    for x in range(8,16):      
          f.write('!\nline 1/' + str(x) + '\n  exec-timeout 0 0\n  password ' + Password)
          f.write('\n  login authentication PODS\n  rotary ' + str(x+2) + '\n  no exec\n  transport input ssh\n end\n')
    f.close() 
    NAPALM_MERGE('2')
    os.remove('pod2.cfg')
  
  if podNumber == 'pod3':
    open('pod3.cfg', 'w').close()
    f=open("pod3.cfg", "a")
    for x in range(16,24):
          f.write('!\nline 1/' + str(x) + '\n  exec-timeout 0 0\n  password ' + Password)
          f.write('\n  login authentication PODS\n  rotary ' + str(x+4) + '\n  no exec\n  transport input ssh\n end\n')
    f.close()    
    NAPALM_MERGE('3')
    os.remove('pod3.cfg')


#Full Configuration Commit
def NAPALM_CONFIG():
  from napalm import get_network_driver

  try:
    print ('Loading the Driver...')
    driver = get_network_driver('ios')
  except:
    print ('ERROR LOADING THE DRIVER')

  try:
    print ('Assigning Non-Standard SSH Port...')
    optional_args = {'port': "22"}
  except:
    print ('ERROR BINDING SSH PORT')

  try:
    print ('Loading Connection Settings...')
    device = driver('172.20.5.4', 'console01', '7554306100$#@!', optional_args=optional_args)
  except:
    print ('ERROR APPLYING CONNECTION SETTINGS')

  try:
    print ('Opening the Connection...')
    device.open()
  except:
    print ('ERROR OPENING THE CONNECTION')

  try:
    print ('Loading the Config...')
    device.load_replace_candidate(filename='YARN_TERMINAL_SERVER.cfg')
  except:
    print ('ERROR LOADING THE CONFIG')

  try:
    print ('Comparing the Config...')
    print (device.compare_config())
  except:
    print ('ERROR COMPARING THE CONFIG')

  try:
    print ('Committing the New Config...')
    device.commit_config()
  except:
    print ('ERROR COMMITTING THE CONFIG')

  try:
    print ('Closing the Connection...')
    device.close()
  except:
    print ('ERROR CLOSING THE CONNECTION')

#Merge Config Comit
def NAPALM_MERGE(num):
  from napalm import get_network_driver

  try:
    print('Loading the Driver...')
    driver = get_network_driver('ios')
  except:
    print ('LOAD ERROR')

  try:
    print ('Assigning Non-Standard SSH Port...')
    optional_args = {'port': "22"}
  except:
    print ('SSH ASSIGN ERROR')

  try:
    print ('Loading Connection Settings...')
    device = driver('172.20.5.4', 'console01', '7554306100$#@!', optional_args=optional_args)
  except:
    print ('ERROR BINDING CONNECTION SETTINGS')

  try:
    print ('Opening the Connection...')
    device.open()
  except:
    print ('OPEN CONNECTION ERROR')

  try:
    print ('Merging the Configuration...')
    device.load_merge_candidate(filename='pod' + num + '.cfg')
  except:
    print ('MERGE ERROR')

  try:
    print ('Comparing Config...')
    print (device.compare_config())
  except:
    print ('COMPARE ERROR')

  try:
    print ('Committing the New Config...')
    device.commit_config()
  except:
    print ('COMMIT ERROR')

  try:
    print ('Closing the Connection...')
    device.close()
  except:
    print ('CONNECTION NOT CLOSED')
