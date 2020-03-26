import re

import flask_wtf
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError


class DateValidator(object):
  def __call__(self, unused_form, field):
    data = field.data
    if not re.search(r'^\d{8}$', data):
      raise ValidationError(f'Dates should look like YYYMMDD, not {data}.')


class CsvForm(flask_wtf.FlaskForm):
  firstdate = StringField('First Date', validators=[DateValidator()])
  lastdate = StringField('Last Date', validators=[DateValidator()])
  submit = SubmitField('Generate CSV')
