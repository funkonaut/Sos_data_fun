# SOS DATA
## Database Setup
- Use postgreSQL to create a database named Sos\_data\_fun or whatever you would like
- Use the sql files in the sql folder to create the tables to populate `psql -d {local_database_name} -f {filename}`
- Or run the .dump file `pg_restore -O -x -c -d {local_database_name} {dumped_file_name.dump}`
- Create a .env file with LOCAL\_DATABASE\_URL set to your database url 
    - Use psql \conninfo to get info to make url `postgresql://[user[:password]@][netloc][:port][,...][/dbname]`

