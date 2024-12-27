import csv
import os
import subprocess
import re

def create_user(student_id, last_name, first_name):
   
    username = f"{first_name[0].lower()}{last_name.lower()}{student_id}"
    username = re.sub(r'[^a-z0-9]', '', username)
    
    try:
        subprocess.run(["id", username], check=False, capture_output=True)
        print(f"User {username} already exists. Skipping creation.")
        return username
    except subprocess.CalledProcessError:
       
        try:
            subprocess.run(["sudo", "useradd", "-m", "-g", "students", username], check=True, capture_output=True)
            subprocess.run(["sudo", "passwd", "-e", username], check=True, capture_output=True)  # Force password change
            
            
            user_home = f"/home/{username}"
            subprocess.run(["sudo", "chmod", "700", user_home], check=True, capture_output=True)

            print(f"User {username} created successfully.")
            return username
        except subprocess.CalledProcessError as e:
            print(f"Error creating user {username}: {e}")
            raise
    


def create_users_from_csv(csv_file, output_csv_file):
    
    with open(csv_file, 'r', encoding='utf-8') as infile, open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader, None)
        if header:
          writer.writerow(["student_id", "username"]) 
        
        for row in reader:
            if len(row) == 3:
                student_id, last_name, first_name = row
                try:
                  username = create_user(student_id, last_name, first_name)
                  if username:
                      writer.writerow([student_id, username])
                except subprocess.CalledProcessError:
                    print(f"Skipping user {first_name} {last_name} ({student_id}) due to an error.")
            else:
               print(f"Skipping row {row} due to invalid number of elements.")


if __name__ == "__main__":
   
    input_csv = "test_data/2024_fall.csv"
    output_csv = "test_data/2024_fall_users.csv"
    
   
    try:
      subprocess.run(["groupadd", "students"], check=False, capture_output=True)
    except subprocess.CalledProcessError:
      print("Group students already exists.")

    create_users_from_csv(input_csv, output_csv)
    print("User creation process completed.")