from multiprocessing import Process, Queue
from saleae import automation
import os
import os.path
import pandas as pd
from datetime import datetime
import multiprocessing as mp
import queue

def saleae_acquire():
    with automation.Manager.connect(port=10430) as manager:

    # Configure the capturing device to record on desired channels
        device_configuration = automation.LogicDeviceConfiguration(
            enabled_analog_channels=[1, 2],
            analog_sample_rate=1_562_500,
            enabled_digital_channels=[0],
            digital_sample_rate=6_250_000,
            digital_threshold_volts=3.3,
        )

        capture_configuration = automation.CaptureConfiguration(
        capture_mode=automation.DigitalTriggerCaptureMode(automation.manager.DigitalTriggerType.RISING,0,None,None,after_trigger_seconds=4)
        ) 

    with manager.start_capture(
        #device_id='F4241', #Uncomment & edit to the ID of your device if the software is not able to find it automatically
        device_configuration=device_configuration,
        capture_configuration=capture_configuration) as capture:
        print("**Saleae_acquire process has started!**") 

        print("Waiting for capture to complete...")

        capture.wait()

        print("Capture complete!")

        saveDirectory = "/Users/bu5/Documents/Project Info/Pyrometer/Saleae/" #Edit this to choose directory output is saved in
        os.chdir(saveDirectory)
        output_dir = os.path.join(os.getcwd(), f'output-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
        os.makedirs(output_dir)

        q.put(output_dir)

def saleae_save():

    with automation.Manager.connect(port=10430) as manager:

    # Configure the capturing device to record on desired channels
        device_configuration = automation.LogicDeviceConfiguration(
        enabled_analog_channels=[1, 2],
        analog_sample_rate=1_562_500,
        enabled_digital_channels=[0],
        digital_sample_rate=6_250_000,
        digital_threshold_volts=3.3,
    )

    capture_configuration = automation.CaptureConfiguration(
    capture_mode=automation.DigitalTriggerCaptureMode(automation.manager.DigitalTriggerType.RISING,0,None,None,after_trigger_seconds=4)
    ) 

    with manager.start_capture(
    #device_id='F4241', #Uncomment & edit to the ID of your device if the software is not able to find it automatically
    device_configuration=device_configuration,
    capture_configuration=capture_configuration) as capture:
        print("Saleae_save process has started!**")

        output_dir = q.get()

        # Export raw digital data to a CSV file
        capture.export_raw_data_csv(directory=output_dir, analog_channels=[1, 2])

        capture_filepath = os.path.join(output_dir, 'Pyrometer_capture.sal')

        capture.save_capture(capture_filepath)

if __name__ == '__main__':
 
        q = queue.Queue()
        p1 = Process(target = saleae_acquire)
        p2 = Process(target = saleae_save)
        p1.start()
        p2.start()

    