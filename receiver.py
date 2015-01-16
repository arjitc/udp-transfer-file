#!/usr/bin/env python
##############################
# File-Receiver
# Created by: ArieB
# Date: 17/01/2015
# Version: 0.2
##############################

import socket
from socket import AF_INET, SOCK_DGRAM
import sys
import argparse
import logging
import hashlib
import os

DOC = """ This program ment to retrieve files on private networks with 
	  one-way communcation.

	  File integrity is verified by md5 checksum. This way we can 
	  know for sure if file retrieved is 100% identical 

	  Important Notes:
		- The file might still be whole even if the md5 
		  is different

	  Technical Notes:
		Connection is based on UDP protocol
		timeout of the connection is: 2
		buffer: 1024
      """

class Receiver():
	
	def __init__(self, host, port, buff):
		''' connection initialization '''
		self.host = host
		self.port = port
		self.s = socket.socket(AF_INET,SOCK_DGRAM)
		self.buff = buff

	def listen(self):
		''' start listening for connections '''
		self.s.bind((self.host,self.port))		
		file_name = self.retrieve_file_name()
		print "==================================="
		logger.info("Connection Initiated")
		logger.info("Start retrieving file. Please Wait.")
		file_md5 = self.retrieve_md5_checksum()
		file_size = self.retrieve_file_size()
		self.retrieve_file(file_name)
		logger.info("File Name: " + file_name)
		self.validate_file(file_name,file_md5, file_size)

	def retrieve_md5_checksum(self):
		''' return md5 checksum for file verifaction '''
		data,addr = self.s.recvfrom(self.buff)
		return data

	def retrieve_file_size(self):
		''' return remote file size '''
		size,addr = self.s.recvfrom(self.buff)
		return size

	def retrieve_file_name(self): 
		''' return file name '''
		f_name,addr = self.s.recvfrom(self.buff)
		return f_name.strip()

	def retrieve_file(self,file_name):
		''' retrieve file from remote server '''
		f = open(file_name, 'wb')
		data,addr = self.s.recvfrom(self.buff)
		try:
			while(data):
				f.write(data)
				self.s.settimeout(2)
				data,addr = self.s.recvfrom(self.buff)
		except socket.timeout:
			f.close()
			self.s.close()

	def validate_file(self, file_name, remote_f_md5,remote_f_size):
		local_f_md5 = hashlib.md5(open(file_name, 'rb').read()).hexdigest()
		local_f_size = str(os.path.getsize(file_name))
		if local_f_md5 == remote_f_md5:
			logger.info("Checksum Exam: [PASSED]")
			logger.info("Files Are Identical 100% :)")

		else:
			logger.info("Checksum Exam: [FAILED]") 
			logger.info("Files are not 100% identical")
			logger.info("Remote file size: " + remote_f_size )
			logger.info("Local file size: " + local_f_size )
			logger.info("Remmeber: File still might be usable")
			logger.info("File Received!")
		print "==================================="
		

if __name__ == '__main__':
	logging.basicConfig(level = logging.INFO)
        logger = logging.getLogger("Receiver")

        parser = argparse.ArgumentParser( description = "File-Receiver")
        parser.add_argument('port',help='port to listen on',type=int)
        args = parser.parse_args()
	
	logger.info("Creating Receiver")
	while True:
		receiver = Receiver("0.0.0.0", args.port, 1024)
		logger.info("Listening on port: " + str(args.port))
		receiver.listen()
