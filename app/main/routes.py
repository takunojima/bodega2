from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.main import bp
from app.models import User, Shift
from app.main.forms import ShiftSubmissionForm
from app import db
from datetime import datetime

@bp.route('/')
@bp.route('/index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if current_user.is_manager:
        return redirect(url_for('main.manager_dashboard'))
    return redirect(url_for('main.staff_dashboard'))

@bp.route('/staff/dashboard')
@login_required
def staff_dashboard():
    if current_user.is_manager:
        return redirect(url_for('main.manager_dashboard'))
    shifts = Shift.query.filter_by(user_id=current_user.id).all()
    return render_template('staff/dashboard.html', shifts=shifts)

@bp.route('/staff/submit', methods=['GET', 'POST'])
@login_required
def submit_shift():
    if current_user.is_manager:
        return redirect(url_for('main.manager_dashboard'))
    form = ShiftSubmissionForm()
    if form.validate_on_submit():
        shift = Shift(
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            user_id=current_user.id
        )
        db.session.add(shift)
        db.session.commit()
        flash('シフトが提出されました。承認をお待ちください。')
        return redirect(url_for('main.staff_dashboard'))
    return render_template('staff/submit_shift.html', form=form)

@bp.route('/manager/dashboard')
@login_required
def manager_dashboard():
    if not current_user.is_manager:
        return redirect(url_for('main.staff_dashboard'))
    shifts = Shift.query.all()
    return render_template('manager/dashboard.html', shifts=shifts)

@bp.route('/manager/shift/<int:shift_id>/approve', methods=['POST'])
@login_required
def approve_shift(shift_id):
    if not current_user.is_manager:
        return redirect(url_for('main.staff_dashboard'))
    shift = Shift.query.get_or_404(shift_id)
    shift.status = 'approved'
    db.session.commit()
    flash('シフトが承認されました。')
    return redirect(url_for('main.manager_dashboard'))

@bp.route('/manager/shift/<int:shift_id>/reject', methods=['POST'])
@login_required
def reject_shift(shift_id):
    if not current_user.is_manager:
        return redirect(url_for('main.staff_dashboard'))
    shift = Shift.query.get_or_404(shift_id)
    shift.status = 'rejected'
    db.session.commit()
    flash('シフトが却下されました。')
    return redirect(url_for('main.manager_dashboard')) 