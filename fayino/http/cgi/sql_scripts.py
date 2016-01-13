
# This takes 5 values and will insert in to the main table
insert_member = u'INSERT INTO person_TBL' \
                u'(login_email, password, accept_terms, join_date, password_set)' \
                u'VALUES (%s, %s, %s, %s, %s)'
