# Prerequisites
## Flask
```bash
pip install -r requirements.txt
```
## MySQL database
### Installation
Platform-specific.
### Set-up
Enter mysql console
```bash
mysql
```

Create a database `group25`.
```
CREATE DATABASE group25;
```


Create a user `group25` with a password `buzzers228` and give them access to the created database.

```
CREATE USER 'group25'@'localhost' IDENTIFIED BY 'buzzers228';
```

Create tables using `schema.sql` from the team repo.

# Usage
```bash
python app.py
```
Admin pages are accessible through their respective urls.