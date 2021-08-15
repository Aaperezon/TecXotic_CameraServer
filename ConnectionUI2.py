import asyncio
import websockets
import json
from ManualControl import *
from ConnectionPixhawk import *

indicator_pixhawk = False
pixhawk_status = False
master = None


def Control(arm_disarm, roll, pitch, yaw, throttle, connect_pixhawk):
    global indicator_pixhawk, master
    if(master != None):
        master.recv_match()

        Arm_Disarm(master, arm_disarm)
        Move(master, roll, pitch, yaw, throttle, 0)
        master = ConnectDisconnectPixhawk(connect_pixhawk)
        if (indicator_pixhawk == False):
            indicator_pixhawk = True
    else:
        indicator_pixhawk = False
        master = ConnectDisconnectPixhawk(connect_pixhawk)

def UtilityControl(pitch_camera,yaw_camera,miniROV_direction,reel_direction):
    #pitch_servo.MoveServo(pitch_camera, 1)
    #yaw_servo.MoveServo(yaw_camera, 1)
    #MoveMiniROV(miniROV_direction)
    #MoveReel(reel_direction)
    pass
	



client = set()
async def echo(websocket,path):
    print("Client connected...")
    client.add(websocket)
    try:
        async for commands in websocket:
            print ("client say -> "+commands)
            commands = json.loads(commands)
            Control(commands['arm_disarm'],commands['roll'],commands['pitch'],commands['yaw'],commands['throttle'], commands['connect_pixhawk'])
            UtilityControl(commands['pitch_camera'],commands['yaw_camera'], commands['miniROV_direction'],commands['reel_direction'])
            hum, temp = (0,0)
            send = {
                    "connection_pixhawk": indicator_pixhawk,
                    "pressure":0,
                    "clamp": False,
                    "light": False,
                    "throttle":commands['throttle'],
                    "roll":commands['roll'],
                    "pitch":commands['pitch'],
                    "yaw":commands['yaw'],
                    "temperature": hum,
                    "humidity": temp,
                    "camera1_showing": False, #bool(camera1_image),
                    "camera2_showing": False,
                }
            send = json.dumps(send)
            send = str(send)
            await websocket.send(bytearray(send,'utf-8'))
    except websocket.exceptions.ConnectionClosed:
        print("Client disconnected...")
    finally:
        client.remove(websocket)




if __name__ == "__main__":
    try:
        print("Running...")
        start_server = websockets.serve(echo, "127.0.0.1", 55000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

      