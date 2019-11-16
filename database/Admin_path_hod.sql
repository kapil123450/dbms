CREATE TABLE Admin_path_hod
(
    path_id SERIAL PRIMARY KEY,
    designation VARCHAR(20),
    FOREIGN KEY (designation) REFERENCES level_table(designation) 
);