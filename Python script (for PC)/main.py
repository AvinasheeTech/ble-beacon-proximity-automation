'''
@file      main.py
@brief     beacon detect and proximity based lock/wakeup script for PC
@author    AvinasheeTech
'''

import asyncio
from bleak import BleakClient,BleakScanner
import datetime
import os
import pyautogui
import psutil
import time

#Advertised Service UUID
ADVERTISED_UUID  = ["761d0df3-aad6-2eb7-4447-c0785c46f2ae"]     #Beacon UUID

'''
@brief  search for our device amongst available nearby devices
@retval instance of the device found
'''
async def __search_for_device__():

    server_device = None

    discovered_devices_and_advertisement_data = await BleakScanner.discover(return_adv=True)
    for device, adv_dat in discovered_devices_and_advertisement_data.values():
        print("scanned device:"+str(device.address))
        if(adv_dat.service_uuids == ADVERTISED_UUID):
            print("device found...................with address "+str(device.address) +" and uuid " + str(adv_dat.service_uuids))
            print("and rssi" + str(adv_dat.rssi))
            server_device = adv_dat

    
    #assert server_device is not None, "device not found................................." 

    return server_device


      
'''
@brief  main function 
@param  None
'''
async def __main__():

    #begin_time = datetime.datetime.now()

    try:
        while(True):
            device = await __search_for_device__()
            if((device is not None)):
                if(device.rssi>-80):
                    #when device is in proximity and RSSI greater than -80
                    for proc in psutil.process_iter():
                        #check if device screen locked 
                        if(proc.name() == "LogonUI.exe"):
                            pyautogui.moveTo(100, 200)
                            pyautogui.click(None,200)
                            pyautogui.moveTo(200, 200)
                            pyautogui.click(None,200)
                            time.sleep(25)
                else:
                    #when RSSI less than -80 
                    #lock the screen
                    os.system("rundll32.exe user32.dll,LockWorkStation")

            else:
                #when device is not in proximity
                #lock the screen
                os.system("rundll32.exe user32.dll,LockWorkStation")


    except Exception as e:
        print(e)
    finally:
        pass
                
                


if __name__=='__main__':
    #select your path to binary file below
    asyncio.run(__main__())