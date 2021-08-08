#!/usr/bin/python3
import os
import datetime

SUBVOLUMES = ["/Container/Gitea", "/Container/Heimdall", "/Container/Jackett", "/Container/Jellyfin", "/Container/Letsencrypt", "/Container/Nextcloud", "/Container/Pihole", "/Container/Qbittorrent", "/Container/Sonarr", "/Container/Webtop", "/Container/Wordpress"]

date_format = "%Y-%m-%d"
todaydate = datetime.date.today()
age = 30 # How many days to keep
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
  
  #subvolume dir + todaysdate + the name of the subvolume + the type = Daily snapshot
  SUBVOLUME_DAILY = todaydate.strftime(date_format) + "_" + SUBVOLUME_NAME[-1] + "_Daily"
  SUBVOLUME_DAILY_SNAPSHOT = SUBVOLUME_SNAPSHOTS_DIR + "/" + SUBVOLUME_DAILY
  #print(SUBVOLUME_DAILY_SNAPSHOT)
  i = "sudo btrfs subvolume snapshot -r " + SUBVOLUME + " " + SUBVOLUME_DAILY_SNAPSHOT

  # Check if theres a snapshot for today, if not snapshot create one
  if SUBVOLUME_DAILY not in SUBVOLUME_SNAPSHOTS:
    os.system(i)
  else:
    print("Already a snapshot for " + SUBVOLUME_NAME[-1] + " for today")
  
  # Check and remove any snapshots that are older than age
  for SNAPSHOTS in SUBVOLUME_SNAPSHOTS:
    ## split into date type and name
    SNAPSHOTS_DATE = SNAPSHOTS.split("_")
    ## split up the date
    DATE = SNAPSHOTS_DATE[0].split("-")
    ## Compare date of Snapshot with current date to find how many days has passed
    diff = todaydate - datetime.date(int(DATE[0]), int(DATE[1]), int(DATE[2]))
    a = "sudo btrfs subvolume delete " + SNAPSHOTS
    ## remove any snapshots older that variable age
    if diff.days > age:
      os.system(a)
      print("removing " + SNAPSHOTS)
  print("end Script")
