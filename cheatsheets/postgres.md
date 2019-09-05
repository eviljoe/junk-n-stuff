# Postgres Cheatsheet

## Dump Database To File

```sh
sudo -u ${DATABASE_USER_NAME} pg_dump --file=${DUMP_FILE} ${DATABASE_NAME}
# (1)   (3)                   (4)     (5)                 (6)
```

1.  Need to run the command as the Postgres database user
2.  The user name for the Postgres database user
3.  The command to dump a Postgres database
4.  The file that the database should be dumped into
6.  The name of the database that is being dumped to a file

## Import Database From File

```sh
sudo -u ${DATABASE_USER_NAME} psql ${DATABASE_NAME} < ${DUMP_FILE}
# (1)   (2)                   (3)  (4)                (5)
```

1.  Need to run the command as the Postgres database user
2.  The user name for the Postgres database user
3.  The Postgres command line (not running in interactive mode in this case)
4.  The name of the database that is being updated using the dump file
5.  The file that the database is being updated from

