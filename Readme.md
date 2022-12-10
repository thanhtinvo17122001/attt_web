python3 manage.py migrate sessions
python3 manage.py crawler

docker exec mysql_container /usr/bin/mysqldump --no-tablespaces  -u mysql --password=changeme attt_web > backup.sql
docker exec mysql_container /usr/bin/mysqldump --no-tablespaces  -u mysql --password=changeme attt_web > crawler_data.sql

docker exec -i mysql_container mysql -u mysql -p changeme attt_web < db.sql
