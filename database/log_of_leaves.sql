CREATE TABLE log_of_leaves
(
    leave_id SERIAL PRIMARY KEY,
    status_ INTEGER,
    reason TEXT,
    borrow INTEGER,
    fid INTEGER,
    nb_leaves INTEGER,
    time_of_generation DATE,
    end_date DATE ,
    FOREIGN KEY (fid) REFERENCES log_of_faculty(fid)
);
