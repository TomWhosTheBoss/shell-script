# User Management Scripts

Python scripts for automating the creation and deletion of user accounts on a Linux server for a programming course may be found in this repository.

## Scripts

### `create_users.py`

This script generates user accounts on the Linux system, saves the generated usernames to a new CSV file, and retrieves student data from a CSV file.

**CSV Input File Format:**

The input CSV file should be named `year_semester.csv` (e.g., `2024_fall.csv`) and should have the following structure:

```csv
student_id,last_name,first_name
1234,Doe,John
5678,Smith,Jane
