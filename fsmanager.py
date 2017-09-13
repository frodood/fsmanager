#!/usr/bin/python
#	Script Developed for Dialog Impelemtation 
#	creatd by Dasun Hettiarachchi
#	13-09-2017
#

from lxml import etree
import os
import sys
import commands

print 'Company Name: '+ sys.argv[1] + ' IP: ' + sys.argv[2]

try:
	xml_file = "/usr/src/sample.xml"
	xml_file_output = '/usr/src/' + sys.argv[1] +'.xml'.format(os.path.splitext(xml_file)[0])
	print 'Creating XML Profile Completed...'

	parser = etree.XMLParser(remove_comments=False)
	tree = etree.parse(xml_file, parser)
	root = tree.getroot()

	for param in root.iter("param"):
   		replaced_ip = param.get("value").replace("10.10.10.75", sys.argv[2])
   		param.set("value", replaced_ip)
   	
   	for name in root.iter("profile"):
		replace_name = name.get("name").replace("duosoftware", sys.argv[1])
		name.set("name", replace_name)
	print 'IP Added into Profile Completed...'

	tree.write(xml_file_output)
except:
	print "Operation Failed"
else:
	print 'XML Deploy Completed...'



try:
   file=open("ifaceID", "r")
   output=file.read()
   c = int(output)+1

#print output, c

   file2write=open("ifaceID",'w')
   file2write.write('%d' % c)
   
#print c

   file2write=open("/etc/network/interfaces",'a')
   line1 = 'auto eth0:' + str(c)
   line2 = 'iface eth0:' + str(c) +' inet static'
   line3 = 'address' +' '+ sys.argv[2]
   line4 = 'netmask 255.255.255.0'
   file2write.write("%s \n %s \n %s \n %s \n" % (line1, line2, line3, line4))
   
except IOError:
   print "Error: Can't find file or read data"

else:
   print "Virtual Interface added sucessfully"
   file2write.close()

try:
	command1 = commands.getoutput('ifup eth0:'+str(c))
	command = commands.getoutput('fs_cli -x "sofia profile ' + sys.argv[1] + ' restart"')
	print "Profile " +  sys.argv[1] + " Load Completed in Freeswitch"
except:
   print "Loading Profile in FS Failed"
