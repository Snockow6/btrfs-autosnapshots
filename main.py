#!/usr/bin/python3
import os
import yaml
from icecream import ic
from yaml.loader import SafeLoader
import sys
import Daily 
import Weekly

SUBVOLUME = ""
SUBVOLUMES = []

CONFIG_LOC = ""
CONFIG_NUM = ""

SUBVOLUME_SNAPSHOTS_DIR =""
Name = ""
SUBVOLUME_DIR = ""

def snapshot_dir(Name):
    SUBVOLUME_DIR = os.listdir(Name)
    SUBVOLUME_NAME = Name.split("/")
    if ".snapshots" not in SUBVOLUME_DIR:
        print("not exist")
        n = "sudo btrfs subvolume create " + SUBVOLUME_SNAPSHOTS_DIR
        os.system(n)
    else:
        print("snapshot directroy for " + SUBVOLUME_NAME[-1] + " exists")


def main():
    if "--config" in sys.argv:
        CONFIG_NUM = sys.argv.count("--config") + 1
        CONFIG_LOC = sys.argv[CONFIG_NUM]
    else:
        CONFIG_LOC = "./config.yml"
    with open(CONFIG_LOC, 'r') as file:
        config = yaml.load(file, Loader=SafeLoader)

    ## Add Subvolume dir to Name variable
        for i in config["Name"]:
            ic(i)
            SUBVOLUMES.append(i)

        for SUBVOLUME in SUBVOLUMES:
            ic(SUBVOLUME)
            ## Make sure Subvolume Snapshot directory exists for SUBVOLUME
            snapshot_dir(SUBVOLUME)

            ## Daily Snapshots
            ic(config["Name"][SUBVOLUME])
            if "Daily" in config["Name"][SUBVOLUME]:
                ## Make sure Daily Snapshot is greater than 0
                # as snapshot will be created and then deleted imediatly
                if config["Name"][SUBVOLUME]["Daily"] > 0:
                    Daily.Snapshot_Daily(SUBVOLUME, config["Name"][SUBVOLUME]["Daily"])

            ## Weekly Snapshots
            if "Weekly" in config["Name"][SUBVOLUME]:
                ## Make sure Weekly Snapshot is greater than 0
                # as snapshot will be created and then deleted imediatly
                if config["Name"][SUBVOLUME]["Weekly"] > 0:
                    Weekly.Snapshot_Weekly(SUBVOLUME, config["Name"][SUBVOLUME]["Weekly"])
        
if __name__ == "__main__":

    main()
