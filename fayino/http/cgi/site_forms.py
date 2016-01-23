from wtforms import Form, StringField, validators, PasswordField


class Signup(Form):
    """
    This form is used to sign new user up for an account it is not an
    account that a company admin would set up for their users
    """
    username = StringField(u'User Name',
                           validators=[validators.input_required(),
                                       validators.length(min=6, max=100),
                                       validators.Regexp(r'^[a-zA-Z0-9_]+$',
                                                         message=(u"Username should be one word, letters,"
                                                                  u"numbers, and underscores only."))])
    email = StringField(u'Email address',
                        validators=[validators.input_required(),
                                    validators.length(min=6, max=150),
                                    validators.email()])
    password = PasswordField(u'Password',
                             validators=[validators.input_required(),
                                         validators.length(min=5, max=120),
                                         validators.EqualTo('confirm',
                                                            message='Passwords must match')])
    confirm = PasswordField(u'ReType your Password',
                            validators=[validators.input_required()])
    # FIXME the href is not rendering out as it should there is no link been placed
    '''
    accept_terms = BooleanField(r'I accept the &lt;a href={{url_for(termsandcoditions)}}&gt;'
                                r'Terms and Conditions&lt;/a&gt;.',
                                validators=[validators.input_required()])
    '''
    company_name = StringField(u'Company Name',
                               validators=[validators.length(max=150)])
