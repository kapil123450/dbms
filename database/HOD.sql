CREATE TABLE HOD
(
    hod_id SERIAL PRIMARY KEY,
    start_date_of_hod  DATE,
    fid INTEGER,
    departement VARCHAR(20),
    FOREIGN KEY (fid) REFERENCES log_of_faculty(fid)  
);

CREATE TABLE LOG_FOR_HOD
(
    hod_id SERIAL PRIMARY KEY,
    start_date_of_hod  DATE,
    end_date_of_hod DATE,
    fid INTEGER,
    departement VARCHAR(20),
    FOREIGN KEY (fid) REFERENCES log_of_faculty(fid)  
);