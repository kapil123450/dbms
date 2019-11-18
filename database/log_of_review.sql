CREATE TABLE log_of_review(
    leave_id INTEGER ,
    review TEXT ,
    to_fid INTEGER,
    PRIMARY KEY (leave_id , to_fid)
);