# Cabl API - Prototyp

The project contains a small python Flask REST-API and can be build and started with a docker container.
It's still a prototyp with a few REST-endpoints to demonstrate the usage.

## Test Environment
To test and use the prototype, i have set up a snall test database you can use for free.
i won't maintain this test-setup, but it's always possible to create a new one on freemysqlhosting.net

### Test-Database Setting
Site, where i created a small Database: freemysqlhosting.net
Username: cabl_mariadb_test@10minmail.de   
Password: vFZRYBeJGGQXMmXt

 (Mails for that Account  can be accessed with URL https://muellmail.com/#/cabl_mariadb_test@10minmail.de )

##### Database
Server: sql11.freemysqlhosting.net
Name: sql11526068
Username: sql11526068
Password: mjXiwJQ9vn
Port number: 3306

## Building the API-Container
```sh
docker build -t cabl-api .
```

## Running the API Container
```sh
docker run -d \
-p 5000:5000 \
--name cabl-api \
-e MYSQL_PORT=3306 \
-e MYSQL_DATABASE=sql11526068 \
-e MYSQL_USER=sql11526068 \
-e MYSQL_PASSWORD=mjXiwJQ9vn \
-e MYSQL_HOST=sql11.freemysqlhosting.net \
-e CABL_ADMIN_EMAIL=admin@email.de \
-e CABL_ADMIN_PASSWORD=admin \
-e CABL_DEFAULT_LOCATION=Leipzig \
cabl-api
```

### Docker Parameter
ame=os.getenv('CABL_DEFAULT_LOCATION', default='Leipzig'),

| Parameter | Usage | Default |
| ------ | ------ | --------|
| MYSQL_HOST | hostname for mysql database| localhost
| MYSQL_DATABASE | datbase name for mysql database | cabl
| MYSQL_USER | user for mysql login | cabl
| MYSQL_PASSWORD | password for mysql user | cabl
| MYSQL_PORT| Default mysql port | 3306
| CABL_ADMIN_EMAIL | Default admin login to use the API | admin@email.de
| CABL_ADMIN_PASSWORD | Default password for the admin user | admin
| CABL_DEFAULT_LOCATION | Default location | Leipzig

### API-Endpoint Examples with Curl

#### Login (get token)
```sh
curl \
-X POST \
-H 'Content-Type: application/json' \
-d '{"email":"admin@email.de","password":"admin"}' \
http://<host>:5000/login
```
#### GET users (with token login)
```sh
curl \
-H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkFkbWluaXN0cmF0b3IiLCJlbWFpbCI6ImFkbWluQGVtYWlsLmRlIiwibG9jYXRpb24iOm51bGwsImV4cCI6MTY2NTU5OTMyOH0.V9eeE_JfoTb9EE057wbRGTNe-3As3WchNjQc2Eu0gxE" \
http://<host>:5000/users
```

#### # POST (create) user (with token login)
```sh
curl \
-X POST \
-H 'Content-Type: application/json' \
-d '{"email":"test@email.de","password":"test", "username":"test"}' \
-H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkFkbWluaXN0cmF0b3IiLCJlbWFpbCI6ImFkbWluQGVtYWlsLmRlIiwibG9jYXRpb24iOm51bGwsImV4cCI6MTY2NTU5OTMyOH0.V9eeE_JfoTb9EE057wbRGTNe-3As3WchNjQc2Eu0gxE" \
http://<host>:5000/user
```


#### DELETE user (with token login)
```sh
curl \
-X DELETE \
-H 'Content-Type: application/json' \
-d '{"email":"test@email.de"}' \
-H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkFkbWluaXN0cmF0b3IiLCJlbWFpbCI6ImFkbWluQGVtYWlsLmRlIiwibG9jYXRpb24iOm51bGwsImV4cCI6MTY2NTU5OTMyOH0.V9eeE_JfoTb9EE057wbRGTNe-3As3WchNjQc2Eu0gxE" \
http://<host>:5000/user
```

#### GET cases (with token login)
```sh
curl \
-H 'Content-Type: application/json' \
-H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkFkbWluaXN0cmF0b3IiLCJlbWFpbCI6ImFkbWluQGVtYWlsLmRlIiwibG9jYXRpb24iOm51bGwsImV4cCI6MTY2NTU5OTMyOH0.V9eeE_JfoTb9EE057wbRGTNe-3As3WchNjQc2Eu0gxE" \
http://<host>:5000/cases
```

#### DELETE case (with token login)
```sh
curl \
-X DELETE \
-H 'Content-Type: application/json' \
-d '{"id":"<id>"}' \
-H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkFkbWluaXN0cmF0b3IiLCJlbWFpbCI6ImFkbWluQGVtYWlsLmRlIiwibG9jYXRpb24iOm51bGwsImV4cCI6MTY2NTU5OTMyOH0.V9eeE_JfoTb9EE057wbRGTNe-3As3WchNjQc2Eu0gxE" \
http://<host>:5000/case
```



