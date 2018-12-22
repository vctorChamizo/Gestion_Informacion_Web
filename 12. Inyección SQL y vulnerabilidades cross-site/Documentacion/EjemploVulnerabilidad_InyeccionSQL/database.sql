BEGIN TRANSACTION;
CREATE TABLE orders (
        id integer primary key,
        user text,
        item text
      );
INSERT INTO orders VALUES(0,'pepe','silla');
INSERT INTO orders VALUES(1,'juan','cohete');
COMMIT;
