BEGIN TRANSACTION;
CREATE TABLE messages (id INTEGER PRIMARY KEY, author varchar(50), title varchar(200), body TEXT);
INSERT INTO messages VALUES(1,'pepe','Humanos volando','Quiero saber si los humanos pueden volar');
COMMIT;
