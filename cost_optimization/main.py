from google.cloud import compute_v1
from google.auth import default
from datetime import datetime, timedelta, date
import pytz
from google.api_core.exceptions import GoogleAPIError, NotFound, Forbidden, TooManyRequests


    
def delete_snapshots(project_id):
  
  
 #get the snapshots
  snapshots_client = compute_v1.SnapshotsClient() 
  snapshot_list = snapshots_client.list(project=project_id)
  
  if not snapshot_list.items:
        print("no snapshots to delete") 
    
  

  #get the list of disks
  disks_client = compute_v1.DisksClient() 
  disk_list = disks_client.list(project=project_id, zone="us-central1-b")
  

#create a dictonory for the running lists
  running_disk = []
  for disk in disk_list.items:
     disk_id = disk.id
     disk_status = disk.status
     if disk_status == 'READY':
       running_disk.append(disk_id)
     else:
        print("there are no running disk")


  snapshots_client = compute_v1.SnapshotsClient() 

  snapshot_list = snapshots_client.list(project=project_id)
  cutoff_date = datetime.now(pytz.UTC) - timedelta(days=15) 

  cutoff_dat1 = cutoff_date.date()

  for snapshot in snapshot_list.items:
     creation_timestamp = snapshot.creation_timestamp
     date_type = datetime.fromisoformat(creation_timestamp)
     snapshot_date = date_type.date()
     disk_id1 = snapshot.source_disk_id
     print(disk_id1)
     
     
     if disk_id1 not in running_disk and snapshot_date < cutoff_dat1:
           try:
               snapshots_client.delete(project=project_id, snapshot=snapshot.name)
               print(f"deleting the snapshot {snapshot.name} as it is not associated with teh disk and it is older than 15 days")
          
           except NotFound:
             print("Snapshot list not found.")
             
           except Exception as e:
                print(f"An error occurred while deleting snapshot {snapshot.name}: {e}")
          
           except GoogleAPIError as e:
                print(f"An error occurred while listing snapshots: {e}")
            
           except Forbidden:
                print(f"Permission denied: Unable to delete snapshot {snapshot.name}.")
     else:
            print("All snapshots are associated with disk and deletion is not required")
    
delete_snapshots("forward-map-432605-v5")                                
