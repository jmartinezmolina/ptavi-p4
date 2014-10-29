#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor SIP
"""

import SocketServer
import sys
import time


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class
    """
    Dic_Client = {}
    def handle(self):
    	"""
    	Metodo que actualiza el dic de clientes y trata la peticion REGISTER
    	"""
    	for x in self.Dic_Client.keys():

		if self.Dic_Client[x][1]< time.time():
			del self.Dic_Client[x]
			print self.Dic_Client

        # Escribe dirección y puerto del cliente (de tupla client_address)

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print line
            line = line.split()
            if "REGISTER" in line:
     		if line[5] == "0":
     			if line[2] in self.Dic_Client:
     				del self.Dic_Client[line[2]]
     		else :
            		self.Dic_Client[line[2]] = (self.client_address[0],time.time()+float(line[5]))
            	self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            	self.register2file()
        
            if not line:
                break
        
        
    def register2file(self):
    	"""
    	Metodo que escribe en el fichero el dic de clientes.
    	"""
    	fich = open("registered.txt", 'w')
    	line = ("Use"+ "\t" + "IP" + "\t" + "Expires"+ "\r\n")
    	for x in self.Dic_Client.keys():
    		h_Expires = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(self.Dic_Client[x][1]))
    		line += x + "\t" + self.Dic_Client[x][0] + "\t" + h_Expires + "\r\n"
	fich.write(line)
    	fich.close()

if __name__ == "__main__":
    # Creamos servidor de sip y escuchamos
    serv = SocketServer.UDPServer(("",int(sys.argv[1])), SIPRegisterHandler)
    serv.serve_forever()
