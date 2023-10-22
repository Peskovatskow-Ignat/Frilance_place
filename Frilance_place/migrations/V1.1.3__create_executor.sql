BEGIN;


CREATE TABLE executor (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email VARCHAR(100) NOT null,
    username text,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    specialty VARCHAR(100),
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password VARCHAR(100),
    rating INTEGER CHECK (rating >= 0 AND rating <= 5) DEFAULT 0,
    photo BYTEA
);

COMMIT;