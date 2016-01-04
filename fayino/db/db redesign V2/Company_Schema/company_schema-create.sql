DROP SCHEMA `company_schema_example`;
CREATE SCHEMA IF NOT EXISTS `company_schema_example`;
USE `company_schema_example`;

-- At top of script
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
-- ----------------------------------------------------------------------

-- Client Company Table
CREATE TABLE IF NOT EXISTS `company_schema_example`.`client_company_TBL` (
	`client_company_ID` INT(11) AUTO_INCREMENT NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `sort_code` VARCHAR(6),
    PRIMARY KEY (`client_company_ID`),
    UNIQUE INDEX `client_company_ID_UNIQUE` 
    (`client_company_ID` ASC))    
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- Member table
CREATE TABLE IF NOT EXISTS `company_schema_example`.`member_TBL` (
  `person_ID` INT(11) AUTO_INCREMENT NOT NULL,
  `first_name` VARCHAR(45) NULL DEFAULT NULL,
  `last_name` VARCHAR(45) NULL DEFAULT NULL,
  `username` VARCHAR(100) NULL DEFAULT NULL,
  `DOB` DATE NULL DEFAULT NULL,
  `join_date` DATE NULL DEFAULT NULL,
  `accept_terms` DATE NOT NULL,
  `login_master_ID` INT(11) NOT NULL,
  PRIMARY KEY (`person_ID`),
  UNIQUE INDEX `person_ID_UNIQUE` (`person_ID` ASC),
  UNIQUE INDEX `login_master_ID_UNIQUE` (`login_master_ID` ASC),
  UNIQUE INDEX `user_name_UNIQUE` (`username` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- Communication table
CREATE TABLE IF NOT EXISTS `company_schema_example`.`communication_TBL` (
  `communication_ID` INT(11) AUTO_INCREMENT NOT NULL,
  `detail` VARCHAR(150) NOT NULL,
  `location_type` VARCHAR(45) NULL DEFAULT NULL COMMENT 'This for home, work, that kind of type. Should allow custom',
  `main` TINYINT(1) NULL DEFAULT NULL,
  `person_ID` INT(11) NULL DEFAULT NULL,
  `client_company_ID` INT(11) NULL DEFAULT NULL,
  `communication_type` VARCHAR(15) NOT NULL DEFAULT 'email' COMMENT 'To set type as email, phone, fax. May allow custom',
  PRIMARY KEY (`communication_ID`),
  UNIQUE INDEX `communication_ID_UNIQUE` (`communication_ID` ASC),
  CONSTRAINT `person_communication_FK`
    FOREIGN KEY (`person_ID`)
    REFERENCES `company_schema_example`.`member_TBL` (`person_ID`),
  CONSTRAINT `client_communication_FK`
    FOREIGN KEY (`client_company_ID`)
    REFERENCES `company_schema_example`.`client_company_TBL` (`client_company_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- Address Table
-- This table is for adress that are in the real world, which a person can visit
CREATE TABLE IF NOT EXISTS `company_schema_example`.`address_TBL` (
  `address_ID` INT(11) AUTO_INCREMENT NOT NULL,
  `line_1` VARCHAR(50),
  `line_2` VARCHAR(50),
  `city` VARCHAR(50),
  `county` VARCHAR(50),
  `country` VARCHAR(50),
  `type` VARCHAR(15) COMMENT 'Example type would be home, company, po box',
  `billing_address` TINYINT(1) NOT NULL DEFAULT 0,
  `main_address` TINYINT(1) NOT NULL DEFAULT 0 COMMENT'This the default address, word default can not be used',
  `person_ID` INT(11) NULL DEFAULT NULL,
  `client_company_ID` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`address_ID`),
  UNIQUE INDEX `address_ID_UNIQUE` (`address_ID` ASC),
  CONSTRAINT `person_address_FK`
    FOREIGN KEY (`person_ID`)
    REFERENCES `company_schema_example`.`member_TBL` (`person_ID`),
  CONSTRAINT `client_address_FK`
    FOREIGN KEY (`client_company_ID`)
    REFERENCES `company_schema_example`.`client_company_TBL` (`client_company_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- Job table
CREATE TABLE IF NOT EXISTS `company_schema_example`.`job_TBL` (
  `job_ID_year` INT(4) NOT NULL,
  `job_ID_number` INT(6) NOT NULL,
  `title` VARCHAR(150) NOT NULL,
  `description` VARCHAR(1000) NULL DEFAULT NULL,
  `entry_date` DATE NOT NULL,
  `quoted_time` INT(11) NULL DEFAULT NULL,
  `quoted_cost` FLOAT(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`job_ID_year`, `job_ID_number`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- job time log table
CREATE TABLE IF NOT EXISTS `company_schema_example`.`job_time_log_TBL` (
  `job_time_log_ID` INT(11) NOT NULL AUTO_INCREMENT,
  `job_ID_year` INT(4) NOT NULL,
  `job_ID_number` INT(6) NOT NULL,
  `person_ID` INT(11) NOT NULL,
  `start_time` DATETIME NOT NULL,
  `finish_time` DATETIME NULL DEFAULT NULL,
  `total_time` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`job_time_log_ID`),
  INDEX `per_job_FK` (`person_ID` ASC),
  INDEX `job_time_FK` (`job_ID_year` ASC, `job_ID_number` ASC),
  CONSTRAINT `job_time_FK`
    FOREIGN KEY (`job_ID_year` , `job_ID_number`)
    REFERENCES `company_schema_example`.`job_TBL` (`job_ID_year` , `job_ID_number`),
  CONSTRAINT `per_job_FK`
    FOREIGN KEY (`person_ID`)
    REFERENCES `company_schema_example`.`member_TBL` (`person_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- Member Linked Jobs Table
CREATE TABLE IF NOT EXISTS `company_schema_example`.`member_linked_jobs_TBL` (
	 `job_ID_year` INT(4) NOT NULL, 
	 `job_ID_number` INT(6) NOT NULL, 
	 `person_ID` INT(11) NOT NULL, 
	 `assigned_date` DATE NOT NULL,
	 PRIMARY KEY (`job_ID_year`, `job_ID_number`, `person_ID`),
	 UNIQUE INDEX `member_linked_jobs_ID_UNIQUE`
	 (`job_ID_year`, `job_ID_number`, `person_ID` ASC),
	 CONSTRAINT `per_link_jobs_FK`
		FOREIGN KEY (`person_ID`) 
		REFERENCES `member_TBL`(`person_ID`), 
	 CONSTRAINT `job_link_jobs_FK` 
		FOREIGN KEY (`job_ID_year` , `job_ID_number`)
		REFERENCES `job_TBL`(`job_ID_year` , `job_ID_number`))
 ENGINE = InnoDB 
 DEFAULT CHARACTER SET = utf8; 



-- At bottom of script
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
-- --------------------------------------------