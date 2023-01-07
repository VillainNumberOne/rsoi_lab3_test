psql -U postgres -d ratings -a -f /docker-entrypoint-initdb.d/init/rating_system.sql
psql -U postgres -d ratings -a -f /docker-entrypoint-initdb.d/init/rating_system_inserts.sql
psql -U postgres -d reservations -a -f /docker-entrypoint-initdb.d/init/reservation_system.sql
psql -U postgres -d reservations -a -f /docker-entrypoint-initdb.d/init/reservation_system_inserts.sql
psql -U postgres -d libraries -a -f /docker-entrypoint-initdb.d/init/library_system.sql
psql -U postgres -d libraries -a -f /docker-entrypoint-initdb.d/init/library_system_inserts.sql