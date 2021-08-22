#!/usr/bin/python3
import os
import yaml
from icecream import ic
from yaml.loader import SafeLoader
import sys
import Daily 
import Weekly
import argparse

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
    ## Arguments to use in script
    parser = argparse.ArgumentParser(description="Auto Snapshot btrfs subvolumes from policys")
    parser.add_argument('--config', '-c', type=str, default="./config.yml", help="sets full path for config")
    args = parser.parse_args()
    print(args.config)

    ## Check the config file exists
    try:
        file = open(args.config, 'r')
    except FileNotFoundError as err:
        print(f"Error: {err}")
    else:

        ## Read file into yaml
        with file:
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
