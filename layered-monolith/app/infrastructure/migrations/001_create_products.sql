-- 001_create_products.sql
CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price NUMERIC NOT NULL,
  CONSTRAINT products_name_len CHECK (char_length(name) BETWEEN 1 AND 100),
  CONSTRAINT products_price_positive CHECK (price > 0)
);
