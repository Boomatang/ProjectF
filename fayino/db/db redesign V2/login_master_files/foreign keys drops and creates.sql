ALTER TABLE login_master_files.person_TBL
ADD CONSTRAINT `company_ID_FK`
	FOREIGN KEY (`company_ID`)
    REFERENCES `login_master_files`.`company_TBL` (`company_ID`);


ALTER TABLE login_master_files.person_TBL
DROP FOREIGN KEY `company_ID_FK`;



-- --------------company_schema_example`.`job_time_log_TBL--------------------------------------------------------
ALTER TABLE `company_schema_example`.`job_time_log_TBL`
ADD CONSTRAINT `job_time_FK`
    FOREIGN KEY (`job_ID_year` , `job_ID_number`)
    REFERENCES `company_schema_example`.`job_TBL` (`job_ID_year` , `job_ID_number`);

ALTER TABLE `company_schema_example`.`job_time_log_TBL`
ADD CONSTRAINT `per_job_FK`
    FOREIGN KEY (`person_ID`)
    REFERENCES `company_schema_example`.`person_TBL` (`person_ID`);
    
ALTER TABLE `company_schema_example`.`job_time_log_TBL`
DROP FOREIGN KEY `job_time_FK`;

ALTER TABLE `company_schema_example`.`job_time_log_TBL`
DROP FOREIGN KEY `per_job_FK`;