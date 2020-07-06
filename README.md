# Скрипт для зачистки старых бекапов в облачном хранилище Selectel 

Используется подключение по FTP.
Скрипт принимает параметры: логин и пароль от FTP, за сколько дней оставлять бекапы в хранилище, путь к хранилищу (дефолтное значение backups/mif/dbs).

## Пример использования
```bash
./clear_backups.py -u Username -W Password -d 2 -p mybackup/database

./clear_backups.py --user=Username --pass=Password --days=2 --path=mybackup/database

./clear_backups.py --help // Просмотр описания 