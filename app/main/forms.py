from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, SubmitField
from wtforms.validators import DataRequired
from datetime import date

class ShiftSubmissionForm(FlaskForm):
    date = DateField('日付', validators=[DataRequired()], default=date.today)
    start_time = TimeField('開始時間', validators=[DataRequired()])
    end_time = TimeField('終了時間', validators=[DataRequired()])
    submit = SubmitField('シフトを提出') 