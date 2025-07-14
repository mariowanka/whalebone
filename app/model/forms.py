from flask_wtf import DateTimeField, Form, StringField, validators


class UserForm(Form):
    external_id = StringField(
        "external_id", [validators.DataRequired(), validators.UUID()]
    )
    name = StringField(
        "name",
        [
            validators.DataRequired(),
            validators.Length(1, 30),
        ],
    )
    email = StringField(
        "email",
        [
            validators.DataRequired(),
            validators.Length(1, 40),
        ],
    )
    date_of_birth = DateTimeField("date_of_birth", [validators.DataRequired()])
