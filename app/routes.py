import csv
import datetime
import flask
import io

from app import the_app
from app import forms
from src import generate_csv


@the_app.route('/')
@the_app.route('/index', methods=['GET', 'POST'])
def index():
  form = forms.CsvForm()

  if form.validate_on_submit():
    firstdate =  datetime.datetime.strptime(
        flask.request.form['firstdate'], '%Y%m%d')
    lastdate =  datetime.datetime.strptime(
        flask.request.form['lastdate'], '%Y%m%d')

    with csv.StringIO() as string_buffer:
      writer = csv.writer(string_buffer)
      for row in generate_csv.csv_rows(
          firstdate, lastdate, the_app.config['ROLL_CACHE'],
          the_app.config['VOTE_CACHE']):
        writer.writerow(row)
      
      bytes_buffer = io.BytesIO()
      bytes_buffer.write(string_buffer.getvalue().encode('utf8'))
      bytes_buffer.seek(0)
      return flask.send_file(
          bytes_buffer,
          as_attachment=True,
          attachment_filename='senate_votes.csv',
          mimetype='text/csv')

  else:
    return flask.render_template('index.html', form=form)


@the_app.route('/create_csv', methods=['POST'])
def create_csv():
  firstdate = flask.request.form['firstdate']
  lastdate = flask.request.form['lastdate']
  return f"<script>alert('{firstdate}, {lastdate}');</script>"
