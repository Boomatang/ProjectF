CREATE SCHEMA IF NOT EXISTS `company_schema_example`;
USE `company_schema_example`;

-- At top of script
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
-- ----------------------------------------------------------------------

-- Member table
CREATE TABLE IF NOT EXISTS `company_schema_example`.`member_TBL` (
  `person_ID` INT(11) NOT NULL,
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
    REFERENCES `company_schema_example`.`person_TBL` (`person_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- At bottom of script
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
-- --------------------------------------------