from icecream import ic
import os
import datetime
from dateutil import relativedelta

date_format = "%Y-%m-%d"
todaydate = datetime.date.today()

def Snapshot_Daily(Name, Age):
    ic(Name, Age, "Snapshot_Daily Function")

    ## Variables for making snapshots
    SUBVOLUME_NAME = Name.split("/")
    SUBVOLUME_SNAPSHOTS_DIR = Name + "/.snapshots"
    SNAPSHOT_NAME =  SUBVOLUME_SNAPSHOTS_DIR + "/" + todaydate.strftime(date_format) + "_" + SUBVOLUME_NAME[-1] + "_" + "Daily"
    SUBVOLUME_CREATE = "sudo btrfs subvolume snapshot -r " + Name + " " + SNAPSHOT_NAME 
    SNAPSHOTS_COUNT = 0
    SNAPSHOTS_DAILY_DATES = []
    SNAPSHOTS_DIFF = []

    ## Variables for finding snapshots
    SUBVOLUME_DIR = os.listdir(SUBVOLUME_SNAPSHOTS_DIR)

    ic(SUBVOLUME_NAME[-1])
    
    for SNAPSHOTS in SUBVOLUME_DIR:
        SNAPSHOTS_SPLIT = SNAPSHOTS.split("_")
        SNAPSHOTS_TYPE = SNAPSHOTS_SPLIT[2]

        ic(SNAPSHOTS_SPLIT[0])
        ## Find if any Daily Snapshots have been taken
        if "Daily" in SNAPSHOTS_TYPE:
            ic(SNAPSHOTS)
            SNAPSHOTS_COUNT = SNAPSHOTS_COUNT + 1
            SNAPSHOTS_DAILY_DATES.append(SNAPSHOTS_SPLIT[0])
            
    
    ## If Snapshots count is less than 1 than assume there is no snapshot and create one
    if SNAPSHOTS_COUNT == 0:
        ic(SNAPSHOTS_COUNT)
        os.system(SUBVOLUME_CREATE)
    else: 
        ic(SNAPSHOTS_DAILY_DATES)
        ## Take All Daily Snapshots dates and find if any were created today
        for SNAPSHOTS_DAILY_DATE in SNAPSHOTS_DAILY_DATES:
            SNAPSHOTS_DATE_SPLIT = SNAPSHOTS_DAILY_DATE.split("-")
            diff = relativedelta.relativedelta(todaydate, datetime.date(int(SNAPSHOTS_DATE_SPLIT[0]), int(SNAPSHOTS_DATE_SPLIT[1]), int(SNAPSHOTS_DATE_SPLIT[2])))
            SNAPSHOTS_DIFF.append(diff.days)
            ic(SNAPSHOTS_DAILY_DATE)
            ic(Name)
            if diff.days > Age:
                ic("Its is older than Current set Age")
                SNAPSHOT_DAILY_DELETE = "sudo btrfs subvolume snapshot -r " + SUBVOLUME_SNAPSHOTS_DIR + "/" + SNAPSHOTS_DAILY_DATE + "_" + SUBVOLUME_NAME[-1] + "_" + "Daily"

        
        ic(SNAPSHOTS_DIFF)
        ## IF 0 is contained in SNAPSHOTS_DIFF then there must be a snapshot created for today
        if 0 not in SNAPSHOTS_DIFF:
            ic("There is not a snapshot for today")
            os.system(SUBVOLUME_CREATE)