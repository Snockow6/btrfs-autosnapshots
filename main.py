#!/usr/bin/python3
import datetime
import os
import yaml
import icecream
from yaml.loader import SafeLoader

SUBVOLUME = ""
SUBVOLUMES = []
Daily = ""
Yearly = ""
date_format = "%Y-%m-%d"
todaydate = datetime.date.today()
SUBVOLUME_SNAPSHOTS_DIR =""
Name = ""
SUBVOLUME_DIR = ""
SUBVOLUME_NAME = Name.split("/")

def snapshot_dir(Name):
    SUBVOLUME_DIR = os.listdir(Name)
    if ".snapshots" not in SUBVOLUME_DIR:
        print("not exist")
        n = "sudo btrfs subvolume create " + SUBVOLUME_SNAPSHOTS_DIR
        os.system(n)
    else:
        print("snapshot directroy for " + SUBVOLUME_NAME[-1] + " exists")

## This Function will create and remove snapshots
def Snapshot(Name ,Type):
    icecream.ic(Name)
    SUBVOLUME_NAME = Name.split("/")
    SUBVOLUME_SNAPSHOTS_DIR = Name + "/.snapshots"
    SUBVOLUME_SNAPSHOTS = os.listdir(SUBVOLUME_SNAPSHOTS_DIR)
    SNAPSHOT_NAME = todaydate.strftime(date_format) + "_" + SUBVOLUME_NAME[-1] + "_" + Type
    SUBVOLUME_DAILY_SNAPSHOT = SUBVOLUME_SNAPSHOTS_DIR + "/" + SNAPSHOT_NAME
    icecream.ic(SNAPSHOT_NAME, SUBVOLUME_SNAPSHOTS)
    i = "sudo btrfs subvolume snapshot -r " + Name + " " + SUBVOLUME_DAILY_SNAPSHOT
    ## if there is currently no Daily snapshots create one
    if SNAPSHOT_NAME not in SUBVOLUME_SNAPSHOTS:
        icecream.ic("Not in SUBVOLUME_SNAPSHOTS")
        
        os.system(i)
    else:
      for SNAPSHOTS in SUBVOLUME_SNAPSHOTS:
        SNAPSHOTS_DATE = SNAPSHOTS.split("_")
        ## print type of snapshots
        if SNAPSHOTS_DATE[2] == "Daily":
            ## Check if todays snapshot is taken
            if SNAPSHOT_NAME in SNAPSHOTS:
                print("This", Type, "exists")
            ## if not then create one
            else:
                os.system(i)

def main():
    with open("config.yml", 'r') as file:
        config = yaml.load(file, Loader=SafeLoader)
        icecream.ic(config)
    
    ## Add Subvolume dir to Name variable
        for i in config:
            SUBVOLUMES.append(i)

        for SUBVOLUME in SUBVOLUMES:
            SUBVOLUME_SNAPSHOTS_DIR = SUBVOLUME + "/.snapshots"
            SUBVOLUME_NAME = SUBVOLUME.split("/")
            SUBVOLUME_DIR = os.listdir(SUBVOLUME)
            icecream.ic(SUBVOLUME)
            ## Make sure .snapshots exists
            snapshot_dir(SUBVOLUME)
            ## Make sure SUBVOLUME isnt None 
            if config[SUBVOLUME] != None:
                ## Check if Daily is apart of SUBVOLUME
                if "Daily" in config[SUBVOLUME]:
                    ## Run Daily Snapshot with current SUBVOLUME name and type Daily
                    Snapshot(SUBVOLUME, "Daily")
                
main()