ALTER TABLE login_master_files.person_TBL
ADD CONSTRAINT `company_ID_FK`
	FOREIGN KEY (`company_ID`)
    REFERENCES `login_master_files`.`company_TBL` (`company_ID`);


ALTER TABLE login_master_files.person_TBL
DROP FOREIGN KEY `company_ID_FK`;