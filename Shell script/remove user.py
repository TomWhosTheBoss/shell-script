import csv
import os
import subprocess
import datetime

def remove_user(username):
   
    user_home = f"/home/{username}"
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"{username}_{timestamp}.tar.gz"
    
    try:
       subprocess.run(["sudo", "tar", "-czf", archive_name, user_home], check=True, capture_output=True)
       print(f"User {username} data archived to {archive_name}")

       subprocess.run(["sudo", "userdel", "-r", username], check=True, capture_output=True)
       print(f"User {username} removed successfully.")

    except subprocess.CalledProcessError as e:
      print(f"Error processing user {username}: {e}")
      raise


def remove_users_from_csv(csv_file, archive_name):
   
    with open(csv_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader, None) 
        for row in reader:
          if len(row) == 2:
            _, username = row
            try:
                remove_user(username)
            except subprocess.CalledProcessError:
                print(f"Skipping user {username} due to an error.")
          else:
             print(f"Skipping row {row} due to invalid number of elements.")
    
    
   
    try:
        subprocess.run(["sudo", "tar", "-czf", archive_name, "*.tar.gz"], check=True, capture_output=True)
        print(f"User archives compressed to {archive_name}")
        
       
        subprocess.run(["sudo", "rm", "*.tar.gz"], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
       print(f"Error creating compressed archive : {e}")

if __name__ == "__main__":
    
    input_csv = "test_data/2024_fall_users.csv"
    output_archive = "2024_fall.tar.gz"
    remove_users_from_csv(input_csv, output_archive)
    print("User removal process completed.")
