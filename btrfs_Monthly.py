#!/usr/bin/python3
import os
import datetime
from dateutil import relativedelta

SUBVOLUMES = ["/Container/Gitea"]

date_format = "%Y-%m-%d"
todaydate = datetime.date.today()
age = 3 # How many days to keep
#diff = todaydate - olddate
#diff.days


#Iterate through all SUBVOLUMES 
for SUBVOLUME in SUBVOLUMES:
  SUBVOLUME_SNAPSHOTS_DIR = SUBVOLUME + "/.snapshots"
  SUBVOLUME_NAME = SUBVOLUME.split("/")
  SUBVOLUME_DIR = os.listdir(SUBVOLUME)
  print(SUBVOLUME)
  
  #Find if .snapshots exist in btrfs subvolume, create if it does not exist
  if ".snapshots" not in SUBVOLUME_DIR:
    print("not exist")
    n = "sudo btrfs subvolume create " + SUBVOLUME_SNAPSHOTS_DIR
    os.system(n)
  else:
    print("snapshot directroy for " + SUBVOLUME_NAME[-1] + " exists")
  

  SUBVOLUME_SNAPSHOTS = os.listdir(SUBVOLUME_SNAPSHOTS_DIR)
  SUBVOLUME_WEEKLY = todaydate.strftime(date_format) + "_" + SUBVOLUME_NAME[-1] + "_Weekly"
  SUBVOLUME_WEEKLY_SNAPSHOT = SUBVOLUME_SNAPSHOTS_DIR + "/" + SUBVOLUME_WEEKLY
  i = "sudo btrfs subvolume snapshot -r " + SUBVOLUME + " " + SUBVOLUME_WEEKLY_SNAPSHOT
  ## if there is currently no Weekly snapshots create one
  if SUBVOLUME_WEEKLY not in SUBVOLUME_SNAPSHOTS:
    os.system(i)
  else:
      for SNAPSHOTS in SUBVOLUME_SNAPSHOTS:
        SNAPSHOTS_DATE = SNAPSHOTS.split("_")
        ## print type of snapshots
        if SNAPSHOTS_DATE[2] == "Weekly":
            ## Check if todays snapshot is taken
            if SUBVOLUME_WEEKLY in SNAPSHOTS:
                print("This Week exists")
            ## if not then create one
            else:
                os.system(i)
            DATE = SNAPSHOTS_DATE[0].split("-")
            ## Compare date of Snapshot with current date to find how many months has passed
            diff = relativedelta.relativedelta(todaydate, datetime.date(int(DATE[0]), int(DATE[1]), int(DATE[2])))
            ## Deletes snapshot if older that age variable
            if diff.months > age:
               a = "sudo btrfs subvolume delete " + SNAPSHOTS
               os.system(a)