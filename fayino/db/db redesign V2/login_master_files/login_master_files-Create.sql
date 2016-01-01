-- At top of script
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
-- ----------------------------------------------------------------------

-- Create the main user login table
CREATE TABLE IF NOT EXISTS `login_master_files`.`person_TBL` (
  `person_ID` INT(11) AUTO_INCREMENT NOT NULL,
  `join_date` DATE NULL DEFAULT NULL,
  `accept_terms` DATE NOT NULL,
  `password` VARCHAR(150) NOT NULL,
  `login_email` VARCHAR(150) NOT NULL,
  `company_ID` INT(11),
  PRIMARY KEY (`person_ID`),
  UNIQUE INDEX `person_ID_UNIQUE` (`person_ID` ASC),
  CONSTRAINT `company_ID_FK`
	FOREIGN KEY (`company_ID`)
    REFERENCES `login_master_files`.`company_TBL` (`company_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- Create the log of companys that user's have set up
CREATE TABLE IF NOT EXISTS `login_master_files`.`company_TBL` (
  `company_ID` INT(11) AUTO_INCREMENT NOT NULL,
  `company_name` VARCHAR(100) NOT NULL,
  `set_up_date` DATE NOT NULL,
  `company_schema` VARCHAR(20) NOT NULL UNIQUE,
  PRIMARY KEY (`company_ID`),
  UNIQUE INDEX `company_ID_UNIQUE` (`company_ID` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- At bottom of script
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
-- --------------------------------------------