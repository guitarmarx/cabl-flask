create table if not exists location(
	name varchar(255),
	is_disabled boolean,
	PRIMARY KEY( name )
);

create table if not exists user(
    email varchar(255),
	user varchar(255),
	password varchar(255),
	location varchar(255),
	PRIMARY KEY( email ),
	FOREIGN KEY (location) REFERENCES location(name) 
);