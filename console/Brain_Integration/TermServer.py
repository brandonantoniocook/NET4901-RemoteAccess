#!/usr/bin/python3

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
  f.write('line vty 0 4\n transport input ssh\n transport output ssh\n!\nscheduler allocate 20000 1000\nend')
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
          f.write('\n  login authentication PODS\n  rotary ' + str(x+1) + '\n  no exec\n  transport input ssh\n')
    f.close()
    NAPALM_MERGE('1')
  
  if podNumber == 'pod2':
    open('pod2.cfg', 'w').close()
    f=open("pod2.cfg", "a")
    for x in range(8,16):      
          f.write('!\nline 1/' + str(x) + '\n  exec-timeout 0 0\n  password ' + Password)
          f.write('\n  login authentication PODS\n  rotary ' + str(x+2) + '\n  no exec\n  transport input ssh\n')
    f.close() 
    NAPALM_MERGE('2')
  
  if podNumber == 'pod3':
    open('pod3.cfg', 'w').close()
    f=open("pod3.cfg", "a")
    for x in range(16,24):
          f.write('!\nline 1/' + str(x) + '\n  exec-timeout 0 0\n  password ' + Password)
          f.write('\n  login authentication PODS\n  rotary ' + str(x+4) + '\n  no exec\n  transport input ssh\n')
    f.close()    
    NAPALM_MERGE('3')

#Full Configuration Commit
def NAPALM_CONFIG():
  from napalm import get_network_driver
  
  print ('Loading the Driver')
  driver = get_network_driver('ios')
  print ('OK')
  
  print ('Assigning Non-Standard SSH Port')
  optional_args = {'port': "2222"}
  print ('OK')

  print ('Load Connection Settings')
  device = driver('netproj.peregrination.life', 'console01', '7554306100$#@!', optional_args=optional_args)
  print ('OK')  

  print ('Open the connection')
  device.open()
  print ('OK')  

  print ('Load Config')
  device.load_replace_candidate(filename='YARN_TERMINAL_SERVER.cfg')
  print ('OK') 

  print ('Compare Config')
  print (device.compare_config())
  print ('OK')

  print ('Commit the new config')
  device.commit_config()
  print ('OK')

  print ('Close the connection')
  device.close()
  print ('OK')

#Merge Config Comit
def NAPALM_MERGE(num):
  from napalm import get_network_driver
  
  print ('Loading the Driver')
  driver = get_network_driver('ios')
  print ('OK')
  
  print ('Assigning Non-Standard SSH Port')
  optional_args = {'port': "2222"}
  print ('OK')

  print ('Load Connection Settings')
  device = driver('netproj.peregrination.life', 'console01', '7554306100$#@!', optional_args=optional_args)
  print ('OK')  

  print ('Open the connection')
  device.open()
  print ('OK')  

  print ('Merge Config')
  device.load_merge_candidate(filename='pod' + num + '.cfg')
  print ('OK') 

  print ('Compare Config')
  print (device.compare_config())
  print ('OK')

  print ('Commit the new config')
  device.commit_config()
  print ('OK')

  print ('Close the connection')
  device.close()
  print ('OK')

#Test Action 1
#configurationCreate('test', 'test', 'test')

#Test Action 2
#mediaryConfigAdditions('pod1', 'itworked')