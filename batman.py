import tkinter as tk
import sys, os
import subprocess 

# Setting debug to false will enable GPIO and disable helper buttons in UI
debug = True
subsample = 2

if debug == False:
	import RPi.GPIO as GPIO

# Setup the movies and process that play the movies
mov_security = ("security.mp4")
mov_code = ("code.mp4")
mov_24 = ("24.mp4")
mov_23 = ("23.mp4")
mov_25 = ("25.mp4")
mov_18 = ("18.mp4")
proc_security = None
proc_code = None
proc_24 = None
proc_23 = None
proc_25 = None
prop_18 = None

sec_x1 = int(round((47) / subsample,0))
sec_y1 = int(round((503) / subsample,0))
sec_x2 = int(round((sec_x1 + 960) / subsample,0))
sec_y2 = int(round((sec_y1 + 540) / subsample,0))

code_x1 = int(round((911) / subsample,0))
code_y1 = int(round((34) / subsample,0))
code_x2 = int(round((code_x1 + 960) / subsample,0))
code_y2 = int(round((code_y1 + 540) / subsample,0))

full_x = int(round(1920/ subsample,0)) 
full_y = int(round(1080/ subsample,0)) 

# Setup the callback events
def event_24(*channel):  
	kill_video()
	proc_24 = start_fullscreen(mov_24)

def event_23(*channel): 
	kill_video()
	proc_23 = start_fullscreen(mov_23)

def event_25(*channel):  
	kill_video()
	proc_25 = start_fullscreen(mov_25)

def event_18(*channel):  
	kill_video()
	proc_18 = start_fullscreen(mov_18)

def kill_video():
	if proc_24 != None:
		proc_24.kill()
	if proc_23 != None:
		proc_23.kill()
	if proc_25 != None:
		proc_25.kill()
	if prop_18 != None:
		prop_18.kill()

	print("killing existing video")

def start_fullscreen(video):
    print("starting full screen: " + video)
    return subprocess.Popen(['omxplayer', video, "--win", "0,0," + str(full_x) + "," + str(full_y), "--alpha", "155", "--loop", "--vol 0", video])

def start_topright(video):
    print("starting in top right: " + video)
    return subprocess.Popen(['omxplayer', video, "--win", str(code_x1) + "," + str(code_y1) + "," + str(code_x2) + "," + str(code_y2), "--alpha", "200", "--loop", "--vol 0", video])
    return start_video(video, "--win " + str(code_x1) + "," + str(code_y1) + "," + str(code_x2) + "," + str(code_y2) + " --alpha 155 --loop --vol 0")

def start_bottomleft(video):
    print("starting in bottom left: " + video)
    return subprocess.Popen(['omxplayer', video, "--win", str(sec_x1) + "," + str(sec_y1) + "," + str(sec_x2) + "," + str(sec_y2), "--alpha", "200", "--loop", "--vol 0", video])

def end_loop():
	print("terminating")
	kill_video()
	if proc_code != None:
		proc_code.kill()
	if proc_security != None:
		proc_security.kill()

	sys.exit(0)

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
	bigbackground_image = tk.PhotoImage(file="wallpaper.png")
	background_image = bigbackground_image.subsample(subsample, subsample)
else:	
	background_image = tk.PhotoImage(file="wallpaper.png")

background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

root.title("Batcave v1.0")

if debug:
	button24 = tk.Button(root, text="Emulate 24", command=event_24)
	button24.place(y=10,x=50)
	button23 = tk.Button(root, text="Emulate 23", command=event_23)
	button23.place(y=10,x=125)
	button25 = tk.Button(root, text="Emulate 25", command=event_25)
	button25.place(y=50,x=50)
	button18 = tk.Button(root, text="Emulate 18", command=event_18)
	button18.place(y=50,x=125)
	w, h = root.winfo_screenwidth()/subsample, root.winfo_screenheight()/subsample
else:
	w, h = root.winfo_screenwidth(), root.winfo_screenheight() #fullscreen
	root.overrideredirect(1) #remove window chrome

root.geometry("%dx%d+0+0" % (w, h))

quitButton = tk.Button(root, text="Quit", command=end_loop)
quitButton.place(y=10,x=10)

background_label.image = background_image

print("Starting security video ...")
proc_security = start_bottomleft(mov_security)

print("Starting code video ...")
proc_code = start_topright(mov_code)

root.mainloop()