/*
 * ER/Studio 8.0 SQL Code Generation
 * Company :      tt
 * Project :      Model1.DM1
 * Author :       tt
 *
 * Date Created : Sunday, October 31, 2021 08:54:21
 * Target DBMS : Microsoft SQL Server 2008
 */

/* 
 * TABLE: exam_detail 
 */

CREATE TABLE exam_detail(
    id                    varchar(255)    NOT NULL,
    school_id             varchar(255)    NOT NULL,
    exam_name             varchar(255)    NULL,
    exam_time             datetime        NULL,
    exam_show_of_num      int             NULL,
    must_num_of_people    int             NULL,
    real_num_of_people    int             NULL,
    miss_num_of_people    int             NULL,
    reference_rate        float           NULL,
    miss_rate             float           NULL,
    CONSTRAINT PK2 PRIMARY KEY NONCLUSTERED (id, school_id)
)
go



IF OBJECT_ID('exam_detail') IS NOT NULL
    PRINT '<<< CREATED TABLE exam_detail >>>'
ELSE
    PRINT '<<< FAILED CREATING TABLE exam_detail >>>'
go

/* 
 * TABLE: exam_site 
 */

CREATE TABLE exam_site(
    id             varchar(255)    NOT NULL,
    school_name    varchar(255)    NULL,
    CONSTRAINT PK1 PRIMARY KEY NONCLUSTERED (id)
)
go



IF OBJECT_ID('exam_site') IS NOT NULL
    PRINT '<<< CREATED TABLE exam_site >>>'
ELSE
    PRINT '<<< FAILED CREATING TABLE exam_site >>>'
go

/* 
 * TABLE: exam_detail 
 */

ALTER TABLE exam_detail ADD CONSTRAINT Refexam_site1 
    FOREIGN KEY (school_id)
    REFERENCES exam_site(id)
go


