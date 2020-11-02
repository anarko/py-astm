import time
import threading

#Local
from constantes import *

DEBUG_ERROR = 1
DEBUG_INFO = 2
DEBUG_DEBUG = 3

ERROR_LEVEL = DEBUG_INFO

def debug_log( nivel,  msg ):

	th_name = threading.currentThread().name
	if nivel == DEBUG_ERROR:
	    fecha = time.strftime("%x")+" "+time.strftime("%X")
	    th_name = th_name.replace("/","-").replace("--dev","")
	    f = file("/var/log/laboratorio/ERROR_"+th_name+".log","a")
	    f.write(fecha+"\n")
	    f.write(msg+"\n")
	    f.write("------------------------------------------------------------------\n")
	    f.close()


	if nivel > ERROR_LEVEL: return

	try:
		fecha = time.strftime("%x")+" "+time.strftime("%X")
		if type(msg) is str:
			print "[ "+fecha+" | "+th_name+" ] "+msg
		elif type(msg) is list:			
			print "[ "+fecha+" | "+th_name+" | Inicio lista ]"
			for m in msg:
				print "[ "+fecha+" | "+th_name+" ]",m
			print "[ "+fecha+" | "+th_name+" | Fin lista ]"
		else:
			print "[ "+fecha+" | "+th_name+" ]"
			print msg
	except:
		print "ERROR EN LOG (?)"

def log_transmision(dato,sentido):
	
	th_name = threading.currentThread().name
	fecha = time.strftime("%x")+" "+time.strftime("%X")
	stri = fecha+" | "+th_name+" | "+sentido+" |"+dato
	stri = stri.replace(STX,"<STX>")
	stri = stri.replace(EOT,"<EOT>")
	stri = stri.replace(ETX,"<ETX>")
	stri = stri.replace(ETB,"<ETB>")
	stri = stri.replace(CR,"<CR>")
	stri = stri.replace(LF,"<LF>")
	stri = stri.replace(ACK,"<ACK>")
	stri = stri.replace(NAK,"<NAK>")
	stri = stri.replace(ENQ,"<ENQ>")
	stri = stri.replace(STX,"<STX>")
	th_name = th_name.replace("/","-").replace("--dev","")
	f = file("/var/log/laboratorio/cobas_"+th_name+".log","a")
	f.write(stri+"\n")
	f.close()
