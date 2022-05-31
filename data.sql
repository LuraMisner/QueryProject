create table State (
    name        varchar(100) PRIMARY KEY, 
    capital     varchar(100),
    population  integer
); 

create table College (
    id          integer PRIMARY KEY AUTO_INCREMENT,
    enrollment  integer,
    name        varchar(100),
    president   varchar(100),
    state       varchar(100),
    FOREIGN KEY(state) REFERENCES STATE(name)
); 
