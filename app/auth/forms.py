from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), 
        Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegisterForm(Form):
    username = StringField('Username', validators=[Required(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9._]*$', 0, 'Usernames must contain only'
                                              ' letters, numbers, periods, '
                                              ' or underscores.')])
    email = StringField('Email', validators=[Required(), Length(1, 64),
        Email()])
    password = PasswordField('Password', validators=[Required(), 
        EqualTo('password2', message="Passwords must match.")])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[Required(),
        EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password', 
        validators=[Required()])
    submit = SubmitField('Update password')


class RequestPasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
        Email()])
    submit = SubmitField('Reset password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Email not registered.')


class ResetPasswordForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
        Email()])
    password = PasswordField('New password', validators=[Required(),
        EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Reset password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangeEmailForm(Form):
    email = StringField('New email address', validators=[Required(),
        Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update email address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError('Email address already registered.')