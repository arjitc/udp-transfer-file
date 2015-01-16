#!/usr/bin/env python
##############################
# File-Sender
# Created by: Arie 
# Date: 17/01/2015
# Version: 0.2
##############################
from socket import *
import sys
import os
import argparse
import logging
import subprocess
import hashlib

DOC = """ This program ment to send files to private networks with
          one-way communcation.

          Transfer reliability depend on UDP protocol

          Technical Notes:
		Connection is based on UDP protocol
                timeout of the connection is: 2
                buffer: 1024
      """

class Connection():
	
	def __init__(self, host, port, buff):
		''' connection initialization '''
		self.s 	  = socket(AF_INET,SOCK_DGRAM)
		self.host = host
		self.port = port
		self.buff = buff
		self.sock = (host, port)
	
	def send_file(self, file_name):
		''' sending file to remote host '''
		self.s.sendto(file_name, self.sock)
		self.s.sendto(self.get_md5_checksum(file_name), self.sock)
		self.s.sendto(str(os.path.getsize(file_name)), self.sock)
		f=open(file_name, "rb")
		data = f.read(self.buff)
		while (data):
       			if(self.s.sendto(data,self.sock)):
               			data = f.read(self.buff)
		self.close_connection(f)

	def close_connection(self,f):
		''' closing socket connection and file which was sent '''
		logger.info("File Sent")
		self.s.close()
		f.close()

	def get_md5_checksum(self, file_name):
		''' get file md5 checksum for verfication '''
		return hashlib.md5(open(file_name, 'rb').read()).hexdigest()

if __name__ == '__main__':
	logging.basicConfig(level = logging.INFO)
	logger = logging.getLogger("Transmitter")

	parser = argparse.ArgumentParser( description = "File-Sender")
	parser.add_argument('filename', help='file name')
	parser.add_argument('ip',help='ip of the remote host')
	parser.add_argument('port',help='port of remote host', type=int)
	args = parser.parse_args()

	if os.path.exists(args.filename):
		logger.info("Creating connection")
		conn = Connection(args.ip, args.port, 1024)
		logger.info("Sending File")
		conn.send_file(args.filename)
	else:
		print "Sorry, the file does not exist"
