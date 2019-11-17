CREATE TABLE current_leaves
(
    id SERIAL PRIMARY KEY,
    leave_id INTEGER,
    status_ INTEGER,
    comment TEXT,
    borrow INTEGER,
    fid INTEGER ,
    position_level INTEGER,
    time_of_generation DATE,
    FOREIGN KEY (fid) REFERENCES log_of_faculty(fid),
    FOREIGN KEY (leave_id) REFERENCES log_of_leaves(leave_id)
);