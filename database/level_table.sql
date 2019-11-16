CREATE TABLE level_table
(
    designation varchar(20) NOT NULL PRIMARY KEY,
    level_posiotion integer
);

INSERT INTO level_table(designation,level_posiotion) VALUES('simple_faculty',0);
INSERT INTO level_table(designation,level_posiotion) VALUES('HOD',1);
INSERT INTO level_table(designation,level_posiotion) VALUES('A_DEAN',2);
INSERT INTO level_table(designation,level_posiotion) VALUES('DEAN',3);
INSERT INTO level_table(designation,level_posiotion) VALUES('DIRECTOR',4);