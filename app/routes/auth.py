from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, limiter
from app.models.user import User
from app.models.preference import UserPreference
from app.forms import (
    LoginForm, RegistrationForm, OnboardingForm,
    ProfilePreferencesForm, ChangePasswordForm, DeleteAccountForm
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with instant preference object initialization."""
    if current_user.is_authenticated:
        return redirect(url_for('reading.my_books'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            role='user'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        # Initialize default user preference
        preference = UserPreference(
            user_id=user.id,
            preferred_genres=[],
            preferred_languages=['English'],
            age_preference='Adult',
            preferred_duration=30,
            interest_keywords=[],
            onboarding_completed=False,
            theme_preference='light'
        )
        db.session.add(preference)
        db.session.commit()

        login_user(user)
        flash('Welcome to BookWise Atelier! Let us personalize your reading journey.', 'success')
        return redirect(url_for('auth.onboarding'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("15 per minute")
def login():
    """Session login with rate limiting and remember me support."""
    if current_user.is_authenticated:
        return redirect(url_for('reading.my_books'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome back, {user.name}. Your personal atelier awaits.', 'success')
            
            # Redirect to next parameter or dashboard
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('reading.my_books'))
        else:
            flash('Invalid email address or password. Please try again.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Secure logout."""
    logout_user()
    flash('You have been signed out of BookWise Atelier. Farewell until your next chapter.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    """5-step reader personalization onboarding wizard."""
    preference = current_user.preference
    if not preference:
        preference = UserPreference(user_id=current_user.id)
        db.session.add(preference)
        db.session.commit()

    form = OnboardingForm()
    if form.validate_on_submit():
        # Parse comma-separated keywords
        keywords_raw = form.interest_keywords.data or ''
        keywords = [k.strip().lower() for k in keywords_raw.split(',') if k.strip()]

        preference.preferred_genres = form.preferred_genres.data or []
        preference.preferred_languages = form.preferred_languages.data or ['English']
        preference.age_preference = form.age_preference.data
        preference.preferred_duration = int(form.preferred_duration.data or 30)
        preference.interest_keywords = keywords
        preference.onboarding_completed = True
        
        db.session.commit()
        flash('Your reader profile has been curated! Your explainable recommendations are ready.', 'success')
        return redirect(url_for('recommendations.index'))

    # Pre-populate form if existing
    if request.method == 'GET':
        form.preferred_genres.data = preference.preferred_genres or []
        form.preferred_languages.data = preference.preferred_languages or ['English']
        form.age_preference.data = preference.age_preference or 'Adult'
        form.preferred_duration.data = str(preference.preferred_duration or 30)
        form.interest_keywords.data = ', '.join(preference.interest_keywords or [])

    return render_template('auth/onboarding.html', form=form, preference=preference)


@auth_bp.route('/onboarding/skip')
@login_required
def skip_onboarding():
    """Allows users to skip onboarding gracefully without broken recommendations."""
    preference = current_user.preference
    if preference:
        preference.onboarding_completed = False
        db.session.commit()
    flash('You can complete your reader profile at any time in your Settings.', 'info')
    return redirect(url_for('books.catalogue'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management: display name, reading preferences, and theme."""
    pref_form = ProfilePreferencesForm()
    pwd_form = ChangePasswordForm()
    del_form = DeleteAccountForm()

    preference = current_user.preference
    if not preference:
        preference = UserPreference(user_id=current_user.id)
        db.session.add(preference)
        db.session.commit()

    if 'pref_submit' in request.form and pref_form.validate_on_submit():
        current_user.name = pref_form.name.data.strip()
        keywords_raw = pref_form.interest_keywords.data or ''
        keywords = [k.strip().lower() for k in keywords_raw.split(',') if k.strip()]

        preference.preferred_genres = pref_form.preferred_genres.data or []
        preference.preferred_languages = pref_form.preferred_languages.data or ['English']
        preference.age_preference = pref_form.age_preference.data
        preference.preferred_duration = pref_form.preferred_duration.data
        preference.interest_keywords = keywords
        preference.theme_preference = pref_form.theme_preference.data
        preference.onboarding_completed = True

        db.session.commit()
        flash('Your reading preferences and theme have been updated.', 'success')
        return redirect(url_for('auth.profile'))

    elif 'pwd_submit' in request.form and pwd_form.validate_on_submit():
        if not current_user.check_password(pwd_form.current_password.data):
            flash('Current password verification failed. Please try again.', 'danger')
        else:
            current_user.set_password(pwd_form.new_password.data)
            db.session.commit()
            flash('Your password has been changed securely.', 'success')
            return redirect(url_for('auth.profile'))

    if request.method == 'GET':
        pref_form.name.data = current_user.name
        pref_form.preferred_genres.data = preference.preferred_genres or []
        pref_form.preferred_languages.data = preference.preferred_languages or ['English']
        pref_form.age_preference.data = preference.age_preference or 'Adult'
        pref_form.preferred_duration.data = preference.preferred_duration or 30
        pref_form.interest_keywords.data = ', '.join(preference.interest_keywords or [])
        pref_form.theme_preference.data = preference.theme_preference or 'light'

    return render_template(
        'profile/index.html',
        pref_form=pref_form,
        pwd_form=pwd_form,
        del_form=del_form,
        preference=preference
    )


@auth_bp.route('/profile/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Account deletion with cascade data cleanup and password confirmation."""
    del_form = DeleteAccountForm()
    if del_form.validate_on_submit():
        if del_form.confirm_email.data.strip().lower() != current_user.email.lower():
            flash('The email address provided does not match your account.', 'danger')
            return redirect(url_for('auth.profile'))
        if not current_user.check_password(del_form.password.data):
            flash('Incorrect password. Account deletion aborted.', 'danger')
            return redirect(url_for('auth.profile'))

        user_to_delete = db.session.get(User, current_user.id)
        logout_user()
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
        flash('Your account and all associated reading records have been permanently deleted.', 'info')
        return redirect(url_for('main.index'))

    flash('Invalid account deletion request.', 'danger')
    return redirect(url_for('auth.profile'))
