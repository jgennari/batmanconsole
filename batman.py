import tkinter as tk
import sys, os, time, subprocess 

# Setting debug to false will enable GPIO and disable helper buttons in UI
debug = False
subsample = 1
showbuttons = True

if debug == False:
	import RPi.GPIO as GPIO

# Setup the movies and process that play the movies
mov_security = ("/home/pi/Desktop/batman/security.mp4")
mov_code = ("/home/pi/Desktop/batman/code.mp4")
mov_24 = ("/home/pi/Desktop/batman/24.mp4")
mov_23 = ("/home/pi/Desktop/batman/23.mp4")
mov_25 = ("/home/pi/Desktop/batman/25.mp4")
mov_18 = ("/home/pi/Desktop/batman/18.mp4")
proc_security = None
proc_code = None
proc_24 = None
proc_23 = None
proc_25 = None
proc_18 = None

sec_x1 = int(round((13) / subsample,0))
sec_y1 = int(round((527) / subsample,0))
sec_x2 = int(round((13 + 960) / subsample,0))
sec_y2 = int(round((527 + 540) / subsample,0))

code_x1 = int(round((990) / subsample,0))
code_y1 = int(round((40) / subsample,0))
code_x2 = int(round((990 + 920) / subsample,0))
code_y2 = int(round((40 + 517) / subsample,0))

minil_x1 = int(round((40) / subsample,0))
minil_y1 = int(round((10) / subsample,0))
minil_x2 = int(round((40 + 880) / subsample,0))
minil_y2 = int(round((10 + 500) / subsample,0))

minir_x1 = int(round((1010) / subsample,0))
minir_y1 = int(round((570) / subsample,0))
minir_x2 = int(round((1010 + 880) / subsample,0))
minir_y2 = int(round((570 + 500) / subsample,0))

full_x = int(round(1920 / subsample,0)) 
full_y = int(round(1080 / subsample,0)) 

delay = 15
last_play = 0

# Setup the callback events
def event_24(*channel):  
	global last_play
	if time.time() - last_play > delay:
		last_play = time.time()
		proc_24 = start_topleft(mov_24)
	else:
		print("Elapsed time is only " + str(time.time() - last_play) + "sec ... need " + str(delay))

def event_23(*channel): 
	global last_play
	if time.time() - last_play > delay:
		last_play = time.time()
		proc_23 = start_bottomright(mov_23)
	else:
		print("Elapsed time is only " + str(time.time() - last_play) + "sec ... need " + str(delay))

def event_25(*channel):  
	global last_play
	if time.time() - last_play > delay:
		last_play = time.time()
		proc_25 = start_topleft(mov_25)
	else:
		print("Elapsed time is only " + str(time.time() - last_play) + "sec ... need " + str(delay))

def event_18(*channel):  
	global last_play
	if time.time() - last_play > delay:
		last_play = time.time()
		proc_18 = start_bottomright(mov_18)
	else:
		print("Elapsed time is only " + str(time.time() - last_play) + "sec ... need " + str(delay))

def kill_video():
	if not (debug):
		kill_process(proc_24)
		kill_process(proc_23)
		kill_process(proc_25)
		kill_process(proc_18)
		kill_process(proc_security)
		kill_process(proc_code)
		subprocess.Popen(['killall', 'omxplayer.bin'])
	print("killing existing video")

def kill_process(proc):
	if proc != None:
		proc.kill()

def start_topleft(video):
	print("starting in top left: " + video)
	if not (debug):
		return subprocess.Popen(['omxplayer', "--win", str(minil_x1) + "," + str(minil_y1) + "," + str(minil_x2) + "," + str(minil_y2), "--alpha", "255", "--vol", "100", "-o", "local", video])

def start_bottomright(video):
	print("starting in bottom right: " + video)
	if not (debug):
		return subprocess.Popen(['omxplayer', "--win", str(minir_x1) + "," + str(minir_y1) + "," + str(minir_x2) + "," + str(minir_y2), "--alpha", "255", "--vol", "100", "-o", "local", video])

def start_topright(video):
	print("starting in top right: " + video)
	if not (debug):
		return subprocess.Popen(['omxplayer', "--win", str(code_x1) + "," + str(code_y1) + "," + str(code_x2) + "," + str(code_y2), "--alpha", "125", "--loop", "--vol", "0", video])

def start_bottomleft(video):
	print("starting in bottom left: " + video)
	if not (debug):
		return subprocess.Popen(['omxplayer', "--win", str(sec_x1) + "," + str(sec_y1) + "," + str(sec_x2) + "," + str(sec_y2), "--alpha", "255", "--loop", "--vol", "0", video])

def end_loop():
	print("terminating")
	kill_video()
	root.destroy()

# Setup the GPIO callback events
if debug == False:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
	GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
	GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
	GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
	GPIO.add_event_detect(24, GPIO.RISING, callback=event_24)  
	GPIO.add_event_detect(23, GPIO.RISING, callback=event_23)  
	GPIO.add_event_detect(25, GPIO.RISING, callback=event_25)  
	GPIO.add_event_detect(18, GPIO.RISING, callback=event_18)  

root = tk.Tk()


if subsample > 0:
	bigbackground_image = tk.PhotoImage(file="/home/pi/Desktop/batman/wallpaper.png")
	background_image = bigbackground_image.subsample(subsample, subsample)
else:	
	background_image = tk.PhotoImage(file="/home/pi/Desktop/batman/wallpaper.png")

background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

root.title("Batcave v1.0")

if showbuttons:
	button24 = tk.Button(root, text="Pin 24", command=event_24)
	button24.place(y=10,x=50)
	button23 = tk.Button(root, text="Pin 23", command=event_23)
	button23.place(y=10,x=125)
	button25 = tk.Button(root, text="Pin 25", command=event_25)
	button25.place(y=50,x=50)
	button18 = tk.Button(root, text="Pin 18", command=event_18)
	button18.place(y=50,x=125)	

if debug:
	w, h = root.winfo_screenwidth()/subsample, root.winfo_screenheight()/subsample
else:
	w, h = root.winfo_screenwidth(), root.winfo_screenheight() #fullscreen
	root.overrideredirect(1) #remove window chrome

quitButton = tk.Button(root, text="Quit", command=end_loop)
quitButton.place(y=10,x=10)

root.geometry("%dx%d+0+0" % (w, h))
background_label.image = background_image

print("Starting security video ...")
proc_security = start_bottomleft(mov_security)

print("Starting code video ...")
proc_code = start_topright(mov_code)

root.mainloop()
