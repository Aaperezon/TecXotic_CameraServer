from gpiozero import OutputDevice
import threading
from time import sleep
relay_red = OutputDevice(17) #GPIO
relay_green = OutputDevice(22) #GPIO
relay_blue = OutputDevice(27) #GPIO

def setColorRGB(r=0,g=0,b=0):
        if(r == True):
                relay_red.on()
        else:
                relay_red.off()
        if(g == True):
                relay_green.on()
        else:
                relay_green.off()
        if(b == True):
                relay_blue.on()
        else:
                relay_blue.off()


thread_warning = None
end_thread = False
def WarningConnectionUI(stop):
        while(True):
                setColorRGB(1,0,0)
                sleep(.5)
                setColorRGB(0,0,0)
                sleep(.3)
                if(end_thread == True):
                        break

def WarningConnectionPixhawk(stop):
        while(True):
                setColorRGB(1,1,0)
                sleep(.5)
                setColorRGB(0,0,0)
                sleep(.3)
                if(end_thread == True):
                        break
def AllGood():
        for i in range(3):
                setColorRGB(0,0,1)
                sleep(2)
                setColorRGB(0,0,0)
                sleep(1)

def KillThread():
        global end_thread,thread_warning
        if(end_thread == False):
                end_thread = True
        if(thread_warning != None):
                thread_warning.join()
        end_thread = False
        thread_warning=None
        setColorRGB(0,0,0)


def AssignThread(function):
        global thread_warning,thread_exists
        thread_warning = threading.Thread(target = function,args =(lambda : end_thread, ))
        thread_warning.start()




if __name__ == "__main__":
        try:
                while True:
                        AssignThread(WarningConnectionUI)
                        sleep(3)
                        KillThread()
                        print("iniciando segundo thread")
                        AssignThread(WarningConnectionPixhawk)
                        sleep(3)
                        KillThread()


                """
                while True:
                        r,g,b = input("color rgb :")
                        r = bool(int(r))
                        g = bool(int(g))
                        b = bool(int(b))
                        print(setColorRGB(r,g,b))
                """
        except Exception as e:
