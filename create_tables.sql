DO $$
BEGIN
  IF current_database() = 'prod' THEN
    CREATE TABLE IF NOT EXISTS table1 (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS table2 (
      id SERIAL PRIMARY KEY,
      value INT NOT NULL
    );

  ELSIF current_database() = 'test' THEN
    CREATE TABLE IF NOT EXISTS table1 (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      test_param_1 TEXT 
    );

    CREATE TABLE IF NOT EXISTS table2 (
      id SERIAL PRIMARY KEY,
      value INT NOT NULL,
      test_param_2 TEXT
    );

    CREATE TABLE IF NOT EXISTS table3 (
      id SERIAL PRIMARY KEY,
      created_at TIMESTAMP DEFAULT now(),
      test_param_3 TEXT 
    );
  END IF;
END $$;
