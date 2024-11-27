# CyberSecurityProjectPart1

This is the repository for Cyber Security Project Part 1 (Helsinki University)

Note!:

- This app is designed to be very insecure and should not be used anything else than educational purposes! Do not implement in production!
- This project is a modified version of my own website that was created for a different course.

Instructions for installing and running:

Klone this repository in your computer -> go in the root file -> create .env -file
Add in .env file:

DATABASE_URL = < computer's-local-address >

SECRET_KEY = < secret-key >

Install in terminal (Linux, Mac and Windows):

```
python3 -m venv venv
```

```
source venv/bin/activate
```
or in Windows:

```
.venv\Scripts\activate
```

```
pip install -r ./requirements.txt
```

```
psql < schema.sql
```

```
flask run
```

If there are problems during running of the program, you can test the running of psql with this code: start-pg.sh
