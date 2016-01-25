
top = [u'SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;',
       u'SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;',
       u"SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';"]

bottom = [u'SET SQL_MODE=@OLD_SQL_MODE;',
          u'SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;',
          u'SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;']

client_company_tbl = u'CREATE TABLE IF NOT EXISTS `client_company_TBL` (' \
                     u'`client_company_ID` INT(11) AUTO_INCREMENT NOT NULL, ' \
                     u'`name` VARCHAR(100) NOT NULL, ' \
                     u'`sort_code` VARCHAR(6), ' \
                     u'PRIMARY KEY (`client_company_ID`), ' \
                     u'UNIQUE INDEX `client_company_ID_UNIQUE` ' \
                     u'(`client_company_ID` ASC)) ' \
                     u'ENGINE = InnoDB ' \
                     u'DEFAULT CHARACTER SET = utf8;'

member_tbl = u'CREATE TABLE IF NOT EXISTS `member_TBL` ( ' \
             u'`person_ID` INT(11) AUTO_INCREMENT NOT NULL, ' \
             u'`first_name` VARCHAR(45) NULL DEFAULT NULL, ' \
             u'`last_name` VARCHAR(45) NULL DEFAULT NULL, ' \
             u'`username` VARCHAR(100) NULL DEFAULT NULL, ' \
             u'`DOB` DATE NULL DEFAULT NULL, ' \
             u'`join_date` DATE NULL DEFAULT NULL, ' \
             u'`accept_terms` DATE NOT NULL, ' \
             u'`login_master_ID` INT(11) NULL, ' \
             u'PRIMARY KEY (`person_ID`), ' \
             u'UNIQUE INDEX `person_ID_UNIQUE` (`person_ID` ASC), ' \
             u'UNIQUE INDEX `login_master_ID_UNIQUE` (`login_master_ID` ASC),' \
             u'UNIQUE INDEX `user_name_UNIQUE` (`username` ASC)) ' \
             u'ENGINE = InnoDB ' \
             u'DEFAULT CHARACTER SET = utf8;'

communication_tbl = u'CREATE TABLE IF NOT EXISTS `communication_TBL` (' \
                    u'`communication_ID` INT(11) AUTO_INCREMENT NOT NULL, ' \
                    u'`detail` VARCHAR(150) NOT NULL, ' \
                    u'`location_type` VARCHAR(45) NULL DEFAULT NULL COMMENT "This for home, work, that kind of type. Should allow custom", ' \
                    u'`main` TINYINT(1) NULL DEFAULT NULL, ' \
                    u'`person_ID` INT(11) NULL DEFAULT NULL, ' \
                    u'`client_company_ID` INT(11) NULL DEFAULT NULL, ' \
                    u'`communication_type` VARCHAR(15) NOT NULL DEFAULT "email" COMMENT "To set type as email, phone, fax. May allow custom", ' \
                    u'PRIMARY KEY (`communication_ID`), ' \
                    u'UNIQUE INDEX `communication_ID_UNIQUE` (`communication_ID` ASC), ' \
                    u'CONSTRAINT `person_communication_FK` ' \
                    u'FOREIGN KEY (`person_ID`) ' \
                    u'REFERENCES `member_TBL` (`person_ID`), ' \
                    u'CONSTRAINT `client_communication_FK` ' \
                    u'FOREIGN KEY (`client_company_ID`) ' \
                    u'REFERENCES `client_company_TBL` (`client_company_ID`)) ' \
                    u'ENGINE = InnoDB ' \
                    u'DEFAULT CHARACTER SET = utf8;'

address_tbl = u'CREATE TABLE IF NOT EXISTS `address_TBL` (' \
              u'`address_ID` INT(11) AUTO_INCREMENT NOT NULL, ' \
              u'`line_1` VARCHAR(50), ' \
              u'`line_2` VARCHAR(50), ' \
              u'`city` VARCHAR(50), ' \
              u'`county` VARCHAR(50), ' \
              u'`country` VARCHAR(50), ' \
              u'`type` VARCHAR(15) COMMENT "Example type would be home, company, po box", ' \
              u'`billing_address` TINYINT(1) NOT NULL DEFAULT 0, ' \
              u'`main_address` TINYINT(1) NOT NULL DEFAULT 0 COMMENT"This the default address, word default can not be used", ' \
              u'`person_ID` INT(11) NULL DEFAULT NULL, ' \
              u'`client_company_ID` INT(11) NULL DEFAULT NULL, ' \
              u'PRIMARY KEY (`address_ID`), ' \
              u'UNIQUE INDEX `address_ID_UNIQUE` (`address_ID` ASC), ' \
              u'CONSTRAINT `person_address_FK` ' \
              u'FOREIGN KEY (`person_ID`) ' \
              u'REFERENCES `member_TBL` (`person_ID`), ' \
              u'CONSTRAINT `client_address_FK` ' \
              u'FOREIGN KEY (`client_company_ID`) ' \
              u'REFERENCES `client_company_TBL` (`client_company_ID`)) ' \
              u'ENGINE = InnoDB ' \
              u'DEFAULT CHARACTER SET = utf8; '

job_tbl = u'CREATE TABLE IF NOT EXISTS `job_TBL` (' \
          u'`job_ID_year` INT(4) NOT NULL, ' \
          u'`job_ID_number` INT(6) NOT NULL, ' \
          u'`title` VARCHAR(150) NOT NULL, ' \
          u'`description` VARCHAR(1000) NULL DEFAULT NULL, ' \
          u'`entry_date` DATE NOT NULL, ' \
          u'`quoted_time` INT(11) NULL DEFAULT NULL, ' \
          u'`quoted_cost` FLOAT(10,2) NULL DEFAULT NULL, ' \
          u'PRIMARY KEY (`job_ID_year`, `job_ID_number`)) ' \
          u'ENGINE = InnoDB ' \
          u'DEFAULT CHARACTER SET = utf8; '

job_time_log_tbl = u'CREATE TABLE IF NOT EXISTS `job_time_log_TBL` (' \
                   u'`job_time_log_ID` INT(11) NOT NULL AUTO_INCREMENT, ' \
                   u'`job_ID_year` INT(4) NOT NULL, ' \
                   u'`job_ID_number` INT(6) NOT NULL, ' \
                   u'`person_ID` INT(11) NOT NULL, ' \
                   u'`start_time` DATETIME NOT NULL, ' \
                   u'`finish_time` DATETIME NULL DEFAULT NULL, ' \
                   u'`total_time` INT(11) NULL DEFAULT NULL, ' \
                   u'PRIMARY KEY (`job_time_log_ID`), ' \
                   u'INDEX `per_job_FK` (`person_ID` ASC), ' \
                   u'INDEX `job_time_FK` (`job_ID_year` ASC, `job_ID_number` ASC), ' \
                   u'CONSTRAINT `job_time_FK` ' \
                   u'FOREIGN KEY (`job_ID_year` , `job_ID_number`) ' \
                   u'REFERENCES `job_TBL` (`job_ID_year` , `job_ID_number`), ' \
                   u'CONSTRAINT `per_job_FK` ' \
                   u'FOREIGN KEY (`person_ID`) ' \
                   u'REFERENCES `member_TBL` (`person_ID`)) ' \
                   u'ENGINE = InnoDB ' \
                   u'DEFAULT CHARACTER SET = utf8; '

member_linked_jobs_tbl = u'CREATE TABLE IF NOT EXISTS `member_linked_jobs_TBL` (' \
                         u'`job_ID_year` INT(4) NOT NULL, ' \
                         u'`job_ID_number` INT(6) NOT NULL, ' \
                         u'`person_ID` INT(11) NOT NULL, ' \
                         u'`assigned_date` DATE NOT NULL, ' \
                         u'PRIMARY KEY (`job_ID_year`, `job_ID_number`, `person_ID`), ' \
                         u'UNIQUE INDEX `member_linked_jobs_ID_UNIQUE` ' \
                         u'(`job_ID_year`, `job_ID_number`, `person_ID` ASC), ' \
                         u'CONSTRAINT `per_link_jobs_FK` ' \
                         u'FOREIGN KEY (`person_ID`) ' \
                         u'REFERENCES `member_TBL` ' \
                         u'(`person_ID`), ' \
                         u'CONSTRAINT `job_link_jobs_FK` ' \
                         u'FOREIGN KEY (`job_ID_year` , `job_ID_number`) ' \
                         u'REFERENCES `job_TBL` ' \
                         u'(`job_ID_year` , `job_ID_number`)) ' \
                         u'ENGINE = InnoDB ' \
                         u'DEFAULT CHARACTER SET = utf8; '
client_com_link_jobs = u'CREATE TABLE IF NOT EXISTS `client_com_link_jobs_TBL` (' \
                       u'`job_ID_year` INT(4) NOT NULL, ' \
                       u'`job_ID_number` INT(6) NOT NULL, ' \
                       u'`client_company_ID` INT(11) NOT NULL, ' \
                       u'CONSTRAINT `client_com_link_jobs_FK` ' \
                       u'FOREIGN KEY (`job_ID_year` , `job_ID_number`) ' \
                       u'REFERENCES `job_TBL`(`job_ID_year` , `job_ID_number`), ' \
                       u'CONSTRAINT `client_com_link_job_FK` ' \
                       u'FOREIGN KEY (`client_company_ID`) ' \
                       u'REFERENCES `client_company_TBL` (`client_company_ID`)) ' \
                       u'ENGINE = InnoDB  ' \
                       u'DEFAULT CHARACTER SET = utf8; '

tables = [client_company_tbl,
          member_tbl,
          communication_tbl,
          address_tbl,
          job_tbl,
          job_time_log_tbl,
          member_linked_jobs_tbl,
          client_com_link_jobs]
sql = [top, tables, bottom]