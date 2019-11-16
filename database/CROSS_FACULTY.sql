CREATE TABLE CROSS_FACULTY
(
    croos_fid SERIAL PRIMARY KEY,
    start_date_of_cross_faculty  DATE,
    fid INTEGER,
    designation VARCHAR(20),
    FOREIGN KEY (fid) REFERENCES log_of_faculty(fid)  
);

CREATE TABLE LOG_FOR_CROSS_FACULTY
(
    croos_fid SERIAL PRIMARY KEY,
    start_date_of_cross_faculty  DATE,
    end_date_of_cross_faculty DATE,
    fid INTEGER,
    designation VARCHAR(20),
    FOREIGN KEY (fid) REFERENCES log_of_faculty(fid)  
);

