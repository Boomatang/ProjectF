CREATE SCHEMA IF NOT EXISTS `company_schema_example`;
USE `company_schema_example`;

-- At top of script
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
-- ----------------------------------------------------------------------


CREATE TABLE IF NOT EXISTS `company_schema_example`.`member_TBL` (
  `person_ID` INT(11) NOT NULL,
  `first_name` VARCHAR(45) NULL DEFAULT NULL,
  `last_name` VARCHAR(45) NULL DEFAULT NULL,
  `username` VARCHAR(100) NULL DEFAULT NULL,
  `DOB` DATE NULL DEFAULT NULL,
  `joinDate` DATE NULL DEFAULT NULL,
  `accept_terms` DATE NOT NULL,
  `login_master_ID` INT(11) NOT NULL,
  PRIMARY KEY (`person_ID`),
  UNIQUE INDEX `person_ID_UNIQUE` (`person_ID` ASC),
  UNIQUE INDEX `user_name_UNIQUE` (`username` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- At bottom of script
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
-- --------------------------------------------