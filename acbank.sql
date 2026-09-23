CREATE DATABASE acbank;

USE acbank;

CREATE TABLE bank (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    balance FLOAT
);
select*from bank;