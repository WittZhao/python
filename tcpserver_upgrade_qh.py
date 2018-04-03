#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
#  
  
import socket  
import threading  
import SocketServer  
import json, types,string
import os, time
import xlrd
from datetime import datetime 

# class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):  
#     def handle(self):
#         print "%s connected!!"% (str(datetime.now())) 
#         while 1:
#             data = self.request.recv(1024)
#             if not data:
#                 break
#             print "%s Receive data: '%r'"% (str(datetime.now()),data) 
#             outd="http://vc.nbiot.com.cn/data/upload/soft/20180310/1807.pack"
#             self.request.sendall(outd)
#         print "%s  disconnet!!"%  (str(datetime.now()))      

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print "%s connected!!"% (str(datetime.now()))   
        while 1:
            data = self.request.recv(1024)
            # data_s = str(data)
            if not data:
                break
            print "%s Receive data: '%r'"% (str(datetime.now()),data)
            point = data.find(',')
            number = data[0:point]
            version = data[point+1:len(data)]
            book = xlrd.open_workbook('8955 upgrade.xlsx')
            sheet = book.sheet_by_index(0)
            col_number = sheet.col_values(0)
            col_version = sheet.col_values(1)
            col_url = sheet.col_values(2)
            col_len = sheet.col_values(3)
            udata = "upgrade is not allowed"
            for i in range(1, sheet.nrows):
                if number == col_number[i]:
                    if version == col_version[i]:
                        udata = col_url[i] + ',' + str(col_len[i])
                        break
            print(udata)
            self.request.sendall(udata)               
        print "%s  disconnet!!"%  (str(datetime.now()))              

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):  
    pass  
                    
            
  
if __name__ == "__main__":  
    # Port 0 means to select an arbitrary unused port  
    # HOST, PORT = "120.27.196.107", 20008
    HOST, PORT = "127.0.0.1", 10001 
      
    SocketServer.TCPServer.allow_reuse_address = True  
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)  
    ip, port = server.server_address  
  
    # Start a thread with the server -- that thread will then start one  
    # more thread for each request  
    server_thread = threading.Thread(target=server.serve_forever)  
  
    # Exit the server thread when the main thread terminates  
    server_thread.daemon = True  
    server_thread.start()  
    print "Server loop running in thread:", server_thread.name  
    print "listen port:%d" %(PORT)
    print " .... waiting for connection"  
  
    # Activate the server; this will keep running until you  
    # interrupt the program with Ctrl-C  
    server.serve_forever()  

