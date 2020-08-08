from wtforms import Form, StringField, PasswordField, validators


class RegisterForms(Form):
    email = StringField("EMAIL")
    password = PasswordField("PASSWORD",
                             [validators.data_required(),
                              validators.equal_to('confirm', message="Password does not match")])
    confirm = PasswordField("CONFIRM PASSWORD")


class Login(Form):
    email = StringField("EMAIL")
    password = PasswordField("PASSWORD",
                             [validators.data_required()])
