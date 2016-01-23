
# This takes 5 values and will insert in to the main table
insert_member = u'INSERT INTO person_TBL' \
                u'(login_email, password, accept_terms, join_date, password_set, company_ID)' \
                u'VALUES (%s, %s, %s, %s, %s, %s)'

clean_master = u'ALTER TABLE test_login_master_files.person_TBL ' \
              u'DROP FOREIGN KEY `company_ID_FK`;' \
              u'TRUNCATE TABLE test_login_master_files.person_TBL;' \
              u'TRUNCATE TABLE test_login_master_files.company_TBL;' \
              u'ALTER TABLE test_login_master_files.person_TBL ' \
              u'ADD CONSTRAINT `company_ID_FK` ' \
              u'FOREIGN KEY (`company_ID`) ' \
              u'REFERENCES `login_master_files`.`company_TBL` (`company_ID`);'
