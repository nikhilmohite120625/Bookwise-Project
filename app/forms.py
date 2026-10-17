from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    TextAreaField, IntegerField, FloatField, SelectField, SelectMultipleField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Optional, NumberRange, ValidationError
)
from app.models.user import User

ALL_GENRES = [
    'Fiction', 'Fantasy', 'Science Fiction', 'Mystery', 'Thriller',
    'Romance', 'Biography', 'History', 'Philosophy', 'Self-Help',
    'Technology', 'Education', 'Adventure', 'Young Adult', "Children's Literature"
]

ALL_LANGUAGES = ['English', 'French', 'Spanish', 'German', 'Japanese', 'Italian']

AGE_CATEGORIES = ['All Ages', 'Young Adult', 'Adult', 'Mature']


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=191)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Keep me signed in')
    submit = SubmitField('Enter The Atelier')


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=191)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters.")])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Create Reader Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError('An account with this email address already exists.')


class OnboardingForm(FlaskForm):
    preferred_genres = SelectMultipleField('Favorite Genres', choices=[(g, g) for g in ALL_GENRES], validators=[Optional()])
    preferred_languages = SelectMultipleField('Preferred Languages', choices=[(l, l) for l in ALL_LANGUAGES], default=['English'], validators=[Optional()])
    age_preference = SelectField('Reading Level / Age Preference', choices=[(a, a) for a in AGE_CATEGORIES], default='Adult')
    preferred_duration = SelectField(
        'Typical Session Duration',
        choices=[
            ('15', '15 Minutes (Brief & Focused)'),
            ('20', '20 Minutes (Standard Daily)'),
            ('30', '30 Minutes (Recommended Deep Reading)'),
            ('45', '45 Minutes (Extended Immersion)'),
            ('60', '60 Minutes (Long Reading Retreat)')
        ],
        default='30'
    )
    interest_keywords = StringField('Key Themes & Interests (comma-separated)', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Complete Reading Profile')


class ProfilePreferencesForm(FlaskForm):
    name = StringField('Display Name', validators=[DataRequired(), Length(min=2, max=100)])
    preferred_genres = SelectMultipleField('Favorite Genres', choices=[(g, g) for g in ALL_GENRES], validators=[Optional()])
    preferred_languages = SelectMultipleField('Preferred Languages', choices=[(l, l) for l in ALL_LANGUAGES], validators=[Optional()])
    age_preference = SelectField('Age Suitability', choices=[(a, a) for a in AGE_CATEGORIES])
    preferred_duration = IntegerField('Preferred Duration (Minutes)', validators=[DataRequired(), NumberRange(min=5, max=180)])
    interest_keywords = StringField('Interests & Keywords (comma-separated)', validators=[Optional(), Length(max=255)])
    theme_preference = SelectField('Atelier Theme', choices=[('light', 'Ivory Light'), ('dark', 'Midnight Dark')])
    submit = SubmitField('Save Preferences')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='New passwords must match.')
    ])
    submit = SubmitField('Update Password')


class DeleteAccountForm(FlaskForm):
    confirm_email = StringField('Confirm Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Current Password', validators=[DataRequired()])
    submit = SubmitField('Permanently Delete My Account')


class BookAdminForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired(), Length(max=255)])
    author = StringField('Author', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description / Synopsis', validators=[Optional()])
    genres = StringField('Genres (comma-separated)', validators=[DataRequired()])
    language = StringField('Language', default='English', validators=[DataRequired(), Length(max=64)])
    publication_year = IntegerField('Publication Year', validators=[Optional(), NumberRange(min=0, max=2100)])
    age_suitability = SelectField('Age Suitability', choices=[(a, a) for a in AGE_CATEGORIES], default='Adult')
    estimated_duration = IntegerField('Estimated Reading Duration (Minutes)', validators=[Optional(), NumberRange(min=1, max=600)])
    keywords = StringField('Keywords & Tags (comma-separated)', validators=[Optional()])
    rating = FloatField('Catalogue Rating (1.0 - 5.0)', validators=[Optional(), NumberRange(min=1.0, max=5.0)])
    isbn = StringField('ISBN', validators=[Optional(), Length(max=32)])
    cover_url = StringField('Cover Image URL (optional)', validators=[Optional(), Length(max=500)])
    page_count = IntegerField('Page Count', validators=[Optional(), NumberRange(min=1, max=10000)])
    submit = SubmitField('Save Book to Catalogue')


class ReadingRecordForm(FlaskForm):
    status = SelectField('Shelf', choices=[
        ('want_to_read', 'Want to Read'),
        ('currently_reading', 'Currently Reading'),
        ('completed', 'Completed')
    ], validators=[DataRequired()])
    pages_read = IntegerField('Pages Read', default=0, validators=[Optional(), NumberRange(min=0)])
    total_pages = IntegerField('Total Pages', validators=[Optional(), NumberRange(min=1)])
    personal_rating = FloatField('Personal Rating (1-5)', validators=[Optional(), NumberRange(min=1.0, max=5.0)])
    notes = TextAreaField('Personal Reading Notes', validators=[Optional()])
    submit = SubmitField('Update Shelf')


class JournalForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    book_id = SelectField('Associated Book (Optional)', coerce=int, validators=[Optional()])
    content = TextAreaField('Reflection Content', validators=[DataRequired()])
    submit = SubmitField('Save Reflection')


class CollectionForm(FlaskForm):
    name = StringField('Collection Name', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save Collection')


class ReadingGoalForm(FlaskForm):
    target_books = IntegerField('Target Books for the Year', validators=[DataRequired(), NumberRange(min=1, max=365)])
    goal_year = IntegerField('Goal Year', validators=[DataRequired(), NumberRange(min=2000, max=2100)])
    monthly_target = IntegerField('Monthly Target (Optional)', validators=[Optional(), NumberRange(min=1, max=50)])
    submit = SubmitField('Save Reading Goal')
