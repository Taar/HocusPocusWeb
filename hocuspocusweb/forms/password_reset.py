from wtforms import (
    Form,
    StringField,
    PasswordField,
    validators,
)
from wtforms.validators import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from ..models.user import User


class PasswordResetForm(Form):
    password = PasswordField(validators=[
        validators.Required(),
    ])
    password_confirm = PasswordField(validators=[
        validators.Required(),
    ])

    def __init__(self, dbsession, *args, **kwargs):
        self.dbsession = dbsession
        super().__init__(*args, **kwargs)

    def validate_password(self, field):
        password = field.data
        password_confirm = self.password_confirm.data
        if password != password_confirm:
            raise ValidationError('Passwords do not match')
