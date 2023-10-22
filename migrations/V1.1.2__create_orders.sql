BEGIN;

CREATE TABLE orders (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(100),
    price int,
    description VARCHAR(200),
    full_description text,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_id INT REFERENCES customer(id),
    skill VARCHAR(100),
    status bool default true
);

COMMIT;