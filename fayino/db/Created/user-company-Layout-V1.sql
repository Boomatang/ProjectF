-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema fayino
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema fayino
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `fayino` DEFAULT CHARACTER SET utf8 ;
USE `fayino` ;

-- -----------------------------------------------------
-- Table `fayino`.`email_TBL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fayino`.`email_TBL` (
  `emailID` INT NOT NULL,
  `emailAddress` VARCHAR(150) NOT NULL,
  `emailType` VARCHAR(45) NULL,
  `Default` TINYINT(1) NULL,
  `personID` INT NULL,
  `companyID` INT NULL,
  PRIMARY KEY (`emailID`),
  UNIQUE INDEX `emailID_UNIQUE` (`emailID` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `fayino`.`phone_TBL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fayino`.`phone_TBL` (
  `phoneID` INT NOT NULL,
  `phoneNumber` VARCHAR(45) NULL,
  `phoneType` VARCHAR(45) NULL,
  `default` TINYINT(1) NULL,
  `personID` INT NULL,
  `companyID` INT NULL,
  UNIQUE INDEX `phoneID_UNIQUE` (`phoneID` ASC),
  PRIMARY KEY (`phoneID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `fayino`.`address_TBL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fayino`.`address_TBL` (
  `addressID` INT NOT NULL,
  `addressLine1` VARCHAR(45) NULL,
  `addressLine2` VARCHAR(45) NULL,
  `addressTown` VARCHAR(45) NULL,
  `addressCounty` VARCHAR(45) NULL,
  `addressCountry` VARCHAR(45) NULL,
  `addressPostcode` VARCHAR(45) NULL,
  `addressType` VARCHAR(45) NULL,
  `Default` TINYINT(1) NULL,
  `personID` INT NULL,
  `companyID` INT NULL,
  PRIMARY KEY (`addressID`),
  UNIQUE INDEX `addressID_UNIQUE` (`addressID` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `fayino`.`employee_TBL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fayino`.`employee_TBL` (
  `personID` INT NOT NULL,
  `companyID` INT NOT NULL,
  PRIMARY KEY (`personID`, `companyID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `fayino`.`company_TBL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fayino`.`company_TBL` (
  `companyID` INT NOT NULL,
  `companyName` VARCHAR(100) NOT NULL,
  `companyCode` VARCHAR(8) NOT NULL,
  `companyDesc` VARCHAR(1000) NULL,
  `companyType` VARCHAR(45) NULL,
  `companyOwer` INT NULL,
  `companyAdmin` INT NULL,
  PRIMARY KEY (`companyID`),
  UNIQUE INDEX `companyID_UNIQUE` (`companyID` ASC),
  UNIQUE INDEX `companyCode_UNIQUE` (`companyCode` ASC)/**,
  CONSTRAINT `fk_company_TBL_email_TBL1`
    FOREIGN KEY (`companyID`)
    REFERENCES `fayino`.`email_TBL` (`companyID`),
  CONSTRAINT `fk_company_TBL_phone_TBL1`
    FOREIGN KEY (`companyID`)
    REFERENCES `fayino`.`phone_TBL` (`companyID`),
  CONSTRAINT `fk_company_TBL_address_TBL1`
    FOREIGN KEY (`companyID`)
    REFERENCES `fayino`.`address_TBL` (`companyID`),
  CONSTRAINT `fk_company_TBL_employee_TBL1`
    FOREIGN KEY (`companyID`)
    REFERENCES `fayino`.`employee_TBL` (`companyID`)
    */)
ENGINE = InnoDB;




-- -----------------------------------------------------
-- Table `fayino`.`person_TBL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fayino`.`person_TBL` (
  `personID` INT NOT NULL,
  `fName` VARCHAR(45) NULL,
  `lName` VARCHAR(45) NULL,
  `userName` VARCHAR(100) NULL,
  `DOB` DATE NULL,
  `personType` VARCHAR(45) NULL,
  `joinDate` DATE NULL,
  `acceptTErms` DATE NOT NULL,
  `password` VARCHAR(150) NOT NULL,
  `loginEmail` VARCHAR(150) NOT NULL,
  UNIQUE INDEX `personID_UNIQUE` (`personID` ASC),
  UNIQUE INDEX `userName_UNIQUE` (`userName` ASC),
  UNIQUE INDEX `loginEmail_UNIQUE` (`loginEmail` ASC),
  PRIMARY KEY (`personID`)/**,
  CONSTRAINT `fk_person_TBL_email_TBL`
    FOREIGN KEY (`personID`)
    REFERENCES `fayino`.`email_TBL` (`personID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_person_TBL_address_TBL1`
    FOREIGN KEY (`personID`)
    REFERENCES `fayino`.`address_TBL` (`personID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_person_TBL_phone_TBL1`
    FOREIGN KEY (`personID`)
    REFERENCES `fayino`.`phone_TBL` (`personID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_person_TBL_employee_TBL1`
    FOREIGN KEY (`personID`)
    REFERENCES `fayino`.`employee_TBL` (`personID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION*/)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
