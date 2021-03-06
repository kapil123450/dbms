CREATE TABLE log_of_leaves_comment
(
    id SERIAL PRIMARY KEY,
    leave_id INTEGER,
    status_ INTEGER,
    comment TEXT,
    fid INTEGER ,
    time_of_generation DATE,
    position_level INTEGER,
    FOREIGN KEY (fid) REFERENCES log_of_faculty(fid),
    FOREIGN KEY (leave_id) REFERENCES log_of_leaves(leave_id)
);