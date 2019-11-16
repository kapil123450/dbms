CREATE TABLE current_leaves
(
    leave_id INTEGER PRIMARY KEY,
    status_ INTEGER,
    comment TEXT,
    borrow INTEGER,
    fid INTEGER ,
    position_level INTEGER,
    time_of_generation TIME,
    FOREIGN KEY (fid) REFERENCES log_of_faculty(fid),
    FOREIGN KEY (leave_id) REFERENCES log_of_leaves(leave_id)
);