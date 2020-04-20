import csv
import datetime
import flask
import io
import tempfile

from app import the_app
from app import forms
from src import generate_csv


@the_app.route('/', methods=['GET', 'POST'])
@the_app.route('/index', methods=['GET', 'POST'])
def index():
  form = forms.CsvForm()

  if form.validate_on_submit():
    firstdate =  datetime.datetime.strptime(
        flask.request.form['firstdate'], '%Y%m%d')
    lastdate =  datetime.datetime.strptime(
        flask.request.form['lastdate'], '%Y%m%d')

    # TODO: flask.send_file can accept a BytesIO, but that doesn't work with
    # uWSGI. Find a workaround. Writing a file here sucks.
    _, fname = tempfile.mkstemp(dir=the_app.config['TEMP_DIR'])
    with open(fname, 'w') as outp:
      writer = csv.writer(outp)
      for row in generate_csv.csv_rows(
          firstdate, lastdate, the_app.config['ROLL_CACHE'],
          the_app.config['VOTE_CACHE']):
        writer.writerow(row)

    return flask.send_file(
        fname, as_attachment=True, attachment_filename='senate_votes.csv',
        mimetype='text/csv')

  else:
    return flask.render_template('index.html', form=form)
