# SOS DATA
## 
- Follow the [rules here](https://github.com/openvenues/libpostal) or comment out the function cu.normalize\_dataframe in fwf\_read.py
- Create a virtual python environment and `pip install -r requirements.txt`

## Database Setup and Population
- Use postgreSQL to create a database named Sos\_data\_fun or whatever you would like
- Use the sql files in the sql folder to create the tables to populate `psql -d {local_database_name} -f {filename}`
- Or run the .dump file `pg_restore -O -x -c -d {local_database_name} {dumped_file_name.dump}`
- Create a .env file with LOCAL\_DATABASE\_URL set to your database url 
    - Use psql \conninfo to get info to make url `postgresql://[user[:password]@][netloc][:port][,...][/dbname]`
- Create a folder named "data" in the projects parent directory and place your fixed width txt files there
- Run fwf\_read.py once the above steps are completed to populate the SQL tables

## Data Cleanup
- Many entries in the SQL database are commands to edit the data the file clean\_up.py contains the functions and commands to execute them to "clean" the data


