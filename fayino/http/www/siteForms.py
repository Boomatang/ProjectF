from wtforms import Form, StringField, validators, SelectField, BooleanField, PasswordField


#: Here you will find forms that can be used to take information form a user


class AddressForm(Form):
    """
    This class takes in a standard format Postal address
    """
    address_line1 = StringField(u'Line 1',
                                validators=[validators.input_required()])
    address_line2 = StringField(u'Line 2',
                                validators=[validators.optional()])
    address_town = StringField(u'City',
                               validators=[validators.input_required()])
    address_county = StringField(u'County/Province',
                                 validators=[validators.input_required()])
    address_country = SelectField(u'Country',
                                  choices=[('fist', '1st'), ('second', '2nd'), ('thired', '3rd')],
                                  validators=[validators.input_required()])
    address_postcode = StringField(u'Postcode/Zip code',
                                   validators=[validators.optional()])

    address_type = SelectField(u'What type of address is this?',
                               choices=[('Home', 'HomeBilling'), ('Work', 'Work'), ('Billing', 'Billing'),
                                        ('Postal', 'Postal')],
                               validators=[validators.input_required()])
    address_default = BooleanField(u'Is this the default address to be used',
                                   validators=[validators.optional()])


class Signup(Form):
    """
    This form is used to sign new user up for an account it is not an
    account that a company admin would set up for their users
    """
    user_name = StringField(u'User Name',
                            validators=[validators.input_required(),
                                        validators.length(min=6, max=100),
                                        validators.Regexp(r'^[a-zA-Z0-9_]+$',
                                                          message=(u"Username should be one word, letters,"
                                                                   u"numbers, and underscores only."))])
    userEmail = StringField(u'Email address',
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
    accept_terms = BooleanField(u'I accept the &lt;a href={{url_for(termsandcoditions)}}&gt;'
                                u'Terms and Conditions&lt;/a&gt;.',
                                validators=[validators.input_required()])


class Set_up_company(Form):
    """
    This form is used to set up the ower's company
    """

    company_name = StringField(u'Company Name',
                               validators=[validators.length(max=150)])
    company_code = StringField(u'Set company',
                               validators=[validators.length(max=150)])
    company_type = SelectField(label='Company Type',
                               choices=[('unknown', 'unknown'),
                                        ('Arts & Crafts', 'ArtsandCrafts'),
                                        ('More  to be added', 'more')],
                               validators=[validators.input_required()])


class LoginConfirm(Form):
    userEmail = StringField(u'Email address',
                            validators=[validators.input_required(),
                                        validators.length(min=6, max=150),
                                        validators.email()])
    password = PasswordField(u'Password',
                             validators=[validators.input_required(),
                                         validators.length(min=5, max=120)])
