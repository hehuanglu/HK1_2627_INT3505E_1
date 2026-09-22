PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT,
        price REAL,
        etag TEXT
    );
INSERT INTO books VALUES(1,'Clean Code','Robert C. Martin','978-0132350884',29.98999999999999844,'aa92d66c1eb5fa8a2b618bfe4d687f70');
INSERT INTO books VALUES(2,'Design Patterns','Erich Gamma','978-0201633610',45.0,'f9fe9232d0bd950e800ac770ed89bdd3');
INSERT INTO books VALUES(3,'High Performance Browser Networking','Ilya Grigorik','978-1449344764',34.99000000000000198,'609c1eff4c4235c49d1425ea27e80e97');
INSERT INTO books VALUES(4,'The Pragmatic Programmer','Andy Hunt','',42.0,'90e05f59b9dc142c3bc3627854929de8');
CREATE TABLE orders (
        id TEXT PRIMARY KEY,
        status TEXT NOT NULL DEFAULT 'pending',
        total REAL NOT NULL,
        items TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
INSERT INTO orders VALUES('o_5c0236bf','cancelled',29.98999999999999844,'[{"book_id": 1, "qty": 1, "price": 29.99}]','2026-09-20 16:14:27');
INSERT INTO sqlite_sequence VALUES('books',4);
COMMIT;
