from tkinter import *
import thread
from subprocess import PIPE
import subprocess
from PIL import Image, ImageTk
import datetime
import os
import serial
import time
import struct
import serial.tools.list_ports
import re


############################################################################################
#Name Prompt
############################################################################################
def okay():
	tech_name.set(text.get('1.0',END))
	lang.destroy()

lang = Tk()
question = Label(lang, text = "Type in your name",font = ('Arial',25))
squestion = Label(lang,text = 'Escriba su nombre',font = ('Arial',25))
text = Text(lang,height=1, width=20,font = ('Arial',25))
tech_name=StringVar()
#tech_name = IntVar()
lang_b1 = Button(lang, text = "Okay", command = okay,font = ('Arial',25))
question.grid(row = 0, column =0)
squestion.grid(row = 1, column =0)
text.grid(row = 2 , column = 0)
lang_b1.grid(row = 3 , column = 0)
lang.mainloop()


path = (os.path.realpath(__file__))
script_directory = str(path).replace('mpower.py','')	
script_directory = str(path).replace('MPOWER.py','')
desktop_directory = script_directory.replace('mpower\\mpower.py','')
print ("Script Directory:\t"+script_directory)
print ("Maybe Desktop Directory:\t"+desktop_directory)





def yes():
	boolean.set(True)
	waiting.set(False)
	b3.configure(state= "disabled")
	b2.configure(state= "disabled")
	b1.configure(state= "normal")
	#text.insert(INSERT,"[Aux Continuity] PASS\n\n\n")
	#text.insert(INSERT,"Change M/Power and \nPress start to test again")
	
def no():
	boolean.set(False)
	waiting.set(False)
	b3.configure(state= "disabled")
	b2.configure(state= "disabled")
	b1.configure(state= "normal")
	#text.insert(INSERT,"[Aux Continuity] FAIL\n\n\n")
	#text.insert(INSERT,"Change M/Power and \nPress start to test again")
config_file = open("config.config",'r')
config_port = []
meter_count = 0

for line in  config_file:
	if line.find("C1") >=0:
		splizzy = line.split('\t',1)
		config_port.append(splizzy[1].replace("\n",'').replace("\t",''))
	if line.find("A1") >=0:
		splizzy = line.split('\t',1)
		config_port.append(splizzy[1].replace("\n",'').replace("\t",''))
	if line.find("A2") >=0:
		splizzy = line.split('\t',1)
		config_port.append(splizzy[1].replace("\n",'').replace("\t",''))
config_file.close()

if os.path.exists(desktop_directory+'MPower QA Software'+'{:%m-%d-%Y}'.format(datetime.datetime.now())+".txt")!= True:
	log = open(str(desktop_directory)+'MPower QA Software'+'{:%m-%d-%Y}'.format(datetime.datetime.now())+".txt",'w')
	log.write("###########################################################################\n")
	log.write('M/Power QA Software \n')
	log.write('[App Version]......................................ver. 00\n')
	log.write('[Test Technician]..................................' + tech_name.get().replace('\n','')+'\n')
	log.write('[Test Start Date]..................................'+'{:%m-%d-%Y,%H:%M:%S}'.format(datetime.datetime.now())+'\n')
	log.write("###########################################################################\n")
	log.write('\n')
	log.close()
else:
	log = open(desktop_directory+'MPower QA Software'+'{:%m-%d-%Y}'.format(datetime.datetime.now())+".txt",'a')
	log.write("###########################################################################\n")
	log.write('M/Power QA Software (Continued) \n')
	log.write('[App Version]......................................ver. 00\n')
	log.write('[Test Technician]..................................' + tech_name.get().replace('\n','')+'\n')
	log.write('[Test Start Date].................................'+'{:%m-%d-%Y,%H:%M:%S}'.format(datetime.datetime.now())+'\n')
	log.write("###########################################################################\n")
	log.write('\n')
	log.close()


def routine(delay):
	cycle = 0
	
	while 1:
		if go.get():
			log = open(desktop_directory+'MPower QA Software'+'{:%m-%d-%Y}'.format(datetime.datetime.now())+".txt",'a')
			time.sleep(0.1)
			b1.configure(state= "disable")
			#cycle = cycle + 1
			
			text.delete("1.0",END)
			text.insert(INSERT,"[USB Power...]Trying to read from USB Meters..\n\n\n\n[Poder de la USB...] Intentando de leer por medio de los medidores de USB..\n")
			meter_count = 0
			meter = []
			meter_data = []
			
			#ser = []
			#log = open(desktop_directory+'MPower QA Software'+'{:%m-%d-%Y}'.format(datetime.datetime.now())+".txt",'a')
			while meter_count < 3:
				serial_list = list(serial.tools.list_ports.comports())
				meter_count = 0
				ser = []
				array = []
				print "Starting USB read.."
				for i in serial_list:
					if i[1].find("STMicroelectronics")>=0:
						#print i[0]
						meter_count = meter_count+1
						#print i[0]
						
						try:
						#print i[0]
							ser.append(serial.Serial(i[0],115200,timeout =1))
							ser[int(meter_count)-1].write("Get Meter Data")
							time.sleep(1)
							c = ser[meter_count-1].readline().encode("hex")
						except serial.serialutil.SerialException:
							text.delete('1.0',END)
							text.insert(INSERT, "Restart Computer/Program\n\n\n\nReinicie la computadora/Programa\n")
							break
						except WindowsError:
							text.delete('1.0',END)
							text.insert(INSERT, "Restart Computer/Program\n\n\n\nReinicie la computadora/Programa\n")
							break
						except ValueError:
							text.delete('1.0',END)
							text.insert(INSERT, "Restart Computer/Program\n\n\n\nReinicie la computadora/Programa\n")
							break
						try:
							meter_data = re.findall('........',c)
						except UnboundLocalError:
							text.delete('1.0',END)
							text.insert(INSERT, "Restart Computer/Program\n\n\n\nReinicie la computadora/Programa\n")
							break
						
						if len(meter_data) == 5:
							for n, k in enumerate(meter_data):
								meter_data[n] = (struct.unpack("<f", k.decode("hex"))[0])
								meter_data[n] = '%.2f' %meter_data[n]
							#print meter_data
							if i[0] == config_port[0]:
								#meter_count = meter_count+1
								if float(meter_data[0]) >= 4.5 and  float(meter_data[1]) >2.6 and float(meter_data[1] )<3.3:
									array.append("USB C @ "+meter_data[0]+'V ' +meter_data[1]+'A - PASS')
								else:
									array.append( "USB C @ "+meter_data[0]+'V '+meter_data[1]+'A - FAIL')
							if i[0] == config_port[1]:
								#meter_count = meter_count+1
								if float(meter_data[0]) >= 4.6 and  float(meter_data[1]) >2.2 and float(meter_data[1]) < 2.6:
									array.append("USB A1 @ "+meter_data[0]+'V '+meter_data[1]+'A - PASS')
								else:
									array.append( "USB A1 @ "+meter_data[0]+'V '+meter_data[1]+'A - FAIL')
							if i[0] == config_port[2]:
								#meter_count = meter_count+1
								if float(meter_data[0]) >= 4.6 and ( float(meter_data[1]) >2.60 and float(meter_data[1]) < 2.60):
									array.append( "USB A2 @ "+meter_data[0]+'V '+meter_data[1]+'A - PASS')
								else:
									array.append( "USB A2 @ "+meter_data[0]+'V '+meter_data[1]+'A - FAIL')
						meter.append(meter_data)
						#print meter_count,meter_data
						try:
							ser[meter_count-1].close()
						except IndexError:
							text.delete('1.0',END)
							text.insert(INSERT, "Restart Computer/Program\n\n\n\nReinicie la computadora/Programa\n")
							break
			for n, i in enumerate(array):
				print n
			if n >=2:
				go.set(False)
				cycle = cycle + 1 
				are_waiting = False
				waiting.set(True)
				are_waiting = waiting.get()
				b3.configure(state= "normal")
				b2.configure(state= "normal")
				load = Image.open("criteria.png")
				photo = ImageTk.PhotoImage(load)
				label.configure(image = photo)
				text.delete('1.0',END)
				text.insert(INSERT, 'Do you see all 4 lights on PCB on?\n\n Ves las 4 luces en la PCB?\n')
			
				while are_waiting:
					time.sleep(0.1)
					are_waiting = waiting.get()
					pass
				if boolean.get():
					array.append("[Aux Continuity] PASS\n\n\n")
				else:
					array.append("[Aux Continuity] FAIL\n\n\n")
				text.delete('1.0',END)
				#for i in array:
				
				log.write("[Cycle Count] \t"+str(cycle)+'\n')
				log.write('[Time Stamp]\t'+str('{:%m-%d-%Y,%H:%M:%S}'.format(datetime.datetime.now())+'\n'))
				try:
					for n, i in enumerate(array):
							text.insert(INSERT, i+'\n')
							log.write(i+'\n')
							#log.write
							#log.write( i+'\n')
							if i.find("PASS")>=0:
								#print 'pass\t'+str(i.index("Pass"))
								text.tag_add("PASS",str(n+1)+'.'+str(i.index("PASS")),str(n+1)+'.'+str(i.index("PASS")+4))
								text.tag_config("PASS", foreground = "green")
							if i.find("FAIL")>=0:
								#print 'Fail\t'+str(i.index("Fail"))
								text.tag_add("FAIL",str(n+1)+'.'+str(i.index("FAIL")),str(n+1)+'.'+str(i.index("FAIL")+4))
								text.tag_config("FAIL", foreground = "red")
							time.sleep(0.001)
				except	_tkinter.TclError:
					go.set(True)
					#text.insert(INSERT,i+'\n')
				text.insert(INSERT, 'Change M/Powers Press Start to test again.\nPor Favor cambie M/Power y persiona inicio\n')		
			log.close()
			load = Image.open("setup.png")
			photo = ImageTk.PhotoImage(load)
			label.configure(image = photo)
			

def set_go():
	go.set(True)
		
		
		
root = Tk()

go = BooleanVar()
go.set(False)
waiting = BooleanVar()
writer = StringVar()
boolean = BooleanVar()
text = Text(root)
text = Text(root,height=15, width = 26,font = ('Arial',20),wrap = WORD)
text.insert(INSERT, "Please Connect M/Power and Press Start \n\n\n Conecte M/Power y presiona Inicio/n")
b1 = Button(root,text = "start",command = set_go ,font = ('Arial',25),width = 5)
b2 = Button(root,text = "Yes", foreground = 'green',command = yes, state = DISABLED,font = ('Arial',25),width = 5)
b3 = Button(root,text = "No ",  foreground = 'red',command = no, state = DISABLED,font = ('Arial',25),width = 5)
load = Image.open("setup.png")
photo = ImageTk.PhotoImage(load)
label = Label(root, image = photo)
label.grid(row = 0, column = 1)
text.grid(row = 0, column = 0)
b1.grid(row=3,column = 0)
b3.grid(row=2,column = 0)
b2.grid(row=1,column = 0)
#b2.grid(row=2, column = 0)
t = thread.start_new_thread(routine, (1,))
root.mainloop() 