################## ASTM-PROTOCOL-SERIAL
import string
import serial
import time

from log import *
from constantes import *

class cola_envio:
    def __init__(self,p):
		self.puerto = p
		self.cola_envio = []

    def agrega_elemento(self,e):
		self.cola_envio.append(e)

    def procesa_cola( self ):
		debug_log( DEBUG_DEBUG, "( procesa_cola ) INICIO ")
		if self.cola_envio == [] :
		    debug_log( DEBUG_DEBUG, "( procesa_cola ) No hay envios ")
		    return None
		
		debug_log( DEBUG_DEBUG, "( procesa_cola ) Enviando... ")
		ret = self.puerto.verifica_envio_enq()
		if ret == ACK:
			for mesg in self.cola_envio:
				#print "Enviando mensage : ", mesg
				ret = self.puerto.envia_respuesta(mesg)
				if ret == ACK:
				    #elimino el elemento de la lista
				    self.cola_envio.remove(mesg)
			self.puerto.escribe_char(EOT)
		
		if ret == ENQ:
			#el coso ese quiere seguir enviando datos, bien molesto
			return None


class astm_protocol_serial:
    def __init__(self,p, th_name):
		self.portName = p
		self.th_name = th_name
		self.puerto = serial.Serial(p, timeout=None)
		self.cola_envio = cola_envio(self)

    def verifica_envio_enq(self):
		self.escribe_char(ENQ)
		e = self.leer_char()
		return e

    def leer_char(self):
		c = self.puerto.read(1)
		log_transmision(c,"RX")
		return c
	
    def escribe_char(self,c):
		self.puerto.write(c)
		log_transmision(c,"TX")

    def recive_enq(self):
		message = []
		self.escribe_char(ACK)
		r = self.lee_frame()
		while r != EOT:
			message.append( r )
			r = self.lee_frame()
		return message


    def lee_frame(self):
		frame = ""
		c = self.puerto.read(1)
		while c != LF and c != EOT:
			frame = frame + c
			c = self.puerto.read(1)
		frame = frame + c
		if c == EOT:
			log_transmision(c,"RX")
			resp = EOT
		else:
			log_transmision(frame,"RX")
			resp = self.check_frame(frame)
			if resp :
				self.puerto.write(ACK)
				log_transmision(ACK,"TX")
		return resp

    def check_frame( self, frame ):
		# Parsea en el frame leido del aparato y verifica el checksum del mensaje
		# devulve false si el checksum no es valido o el mensaje si es valido
		frame_type = ETX
		if frame.find(ETB) != -1:
			frame_type = ETB
		tmp_arr = frame.split( CR+frame_type )
		checksum = tmp_arr[1][:-2]
		message =  tmp_arr[0][1:]
		
		try:
		    chksum = float.fromhex( checksum )
		except:
		    return False
		
		if self.calc_checksum( message+CR+frame_type ) == chksum :
			return message
		return False

    def calc_checksum( self, line ):
		chksum = 0
		for c in line :
			chksum = ( chksum + ord(c) ) % 256
		return chksum

    def sent_line(self, frame ):
		frame = str(self.frame_env_nro)+frame
		chk = self.calc_checksum(frame+CR+ETX)
		chk = hex(chk).split("x")
		chk = chk[1]
		if len(chk) == 1 :
			chk = "0"+chk
		chk = chk.upper()
		frame = STX+frame+CR+ETX+chk+CR+LF
		ret = self.sent_frame(frame)
		self.frame_env_nro += 1
		if self.frame_env_nro > 7:
			self.frame_env_nro = 0
		return ret

    def sent_frame(self,frame ):
		self.puerto.write( str(frame) )
		log_transmision(frame,"TX")
		c = self.puerto.read(1)
		log_transmision(c,"RX")
		if c == ACK:
			return ACK
		else :
			return False

    def envia_respuesta( self, messg ):
		self.frame_env_nro = 1
		for line in  messg:
			ret = self.sent_line(line)
		return ret
