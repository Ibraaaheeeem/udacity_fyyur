#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from unicodedata import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#from models import *
# TODO: connect to a local postgresql database
class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(1000))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(1000))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    artist = db.relationship('Artist', backref = db.backref('artist', cascade = 'all, delete'))
    venue = db.relationship('Venue', backref = db.backref('venue', cascade = 'all, delete'))

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "city": city_n_state.city,
    "state": city_n_state.state,
    "venues": [{
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": len(Show.query.filter(Show.venue_id == venue.id).all()),
    }
    for venue in Venue.query.filter(Venue.city == city_n_state.city, Venue.state == city_n_state.state).all()
    ]
  }
  for city_n_state in db.session.query(Venue.city, Venue.state).distinct()
  ]
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  search_result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  response={
    "count": len(search_result),
    "data": [{
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": len(Show.query.filter(Show.venue_id == venue.id)),
    }
    for venue in search_result
    ]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  if not venue:
    abort(404)
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.city,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "image_link": venue.image_link,
    "past_shows": [{
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    for show in Show.query.join(Artist).filter(Show.venue_id == venue_id, Show.start_time < datetime.now()).all()
    ],
    "upcoming_shows": [{
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    for show in Show.query.join(Artist).filter(Show.venue_id == venue_id, Show.start_time > datetime.now()).all()
    ],
    "past_shows_count": len(Show.query.join(Artist).filter(Show.venue_id == venue_id, Show.start_time < datetime.now()).all()),
    "upcoming_shows_count": len(Show.query.join(Artist).filter(Show.venue_id == venue_id, Show.start_time < datetime.now()).all()),
  }
  
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  new_venue = Venue(
    name = request.form.get('name'),
    city = request.form.get('city'),
    state = request.form.get('state'),
    address = request.form.get('address'),
    phone = request.form.get('phone'),
    genres = request.form.getlist('genres'),
    facebook_link = request.form.get('facebook_link'),
    image_link = request.form.get('image_link'),
    website_link = request.form.get('website_link'),
    seeking_talent = True if request.form.get('seeking_talent') else False,
    seeking_description = request.form.get('seeking_description')
  )
  insert_model('Venue', new_venue)
  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  venue_to_delete = Venue.query.get(venue_id)
  #venue_name_to_delete = venue_to_delete.name
  try:
    db.session.delete(venue_to_delete)
    db.session.commit()
  except:
    db.rollback()
    error=True
  finally:
    db.session.close()

  if not error: 
    flash('Success: Venue has been deleted successfully')
  else:
    flash('Error: Venue could not be deleted')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[{
    "id": artist.id,
    "name": artist.name,
  }
  for artist in Artist.query.all()
  ]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  search_result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  if not search_result:
    abort(404)
  
  response={
    "count": len(search_result),
    "data": [{
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": len(Show.query.filter(Show.artist_id == artist.id)),
    } for artist in search_result
    ]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "seeking_venue": artist.seeking_venue,
    "image_link": artist.image_link,
    "past_shows": [{
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    for show in Show.query.join(Venue).filter(Show.artist_id == artist.id, Show.start_time < datetime.now())
    ],
    "upcoming_shows": [{
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    for show in Show.query.join(Venue).filter(Show.artist_id == artist.id, Show.start_time > datetime.now())
    ],
    "past_shows_count": len(Show.query.join(Venue).filter(Show.artist_id == artist.id, Show.start_time < datetime.now()).all()),
    "upcoming_shows_count": len(Show.query.join(Venue).filter(Show.artist_id == artist.id, Show.start_time > datetime.now()).all())
  }
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist_to_edit = Artist.query.get(artist_id)
  form = ArtistForm()
  artist={
    "id": artist_to_edit.id,
    "name": artist_to_edit.name,
    "genres": artist_to_edit.genres,
    "city": artist_to_edit.city,
    "state": artist_to_edit.state,
    "phone": artist_to_edit.phone,
    "website_link": artist_to_edit.website_link,
    "facebook_link": artist_to_edit.facebook_link,
    "seeking_venue": artist_to_edit.seeking_venue,
    "seeking_description": artist_to_edit.seeking_description,
    "image_link": artist_to_edit.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist(
    name = request.form.get('name'),
    city = request.form.get('city'),
    state = request.form.get('state'),
    phone = request.form.get('phone'),
    genres = request.form.getlist('genres'),
    facebook_link = request.form.get('facebook_link'),
    image_link = request.form.get('image_link'),
    website_link = request.form.get('website_link'),
    seeking_venue = request.form.get('seeking_venue'),
    seeking_description = request.form.get('seeking_description')
  )
  update_model('Artist',  artist)
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm()
  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "image_link": venue.image_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue(
    name = request.form.get('name'),
    city = request.form.get('city'),
    state = request.form.get('state'),
    address = request.form.get('address'),
    phone = request.form.get('phone'),
    genres = request.form.getlist('genres'),
    facebook_link = request.form.get('facebookk_link'),
    image_link = request.form.get('image_link'),
    website_link = request.form.get('website_link'),
    seeking_talent = request.form.get('seeking_talent'),
    seeking_description = request.form.get('seeking_description')
  )
  update_model('Venue', venue)
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  artist = Artist(
    name = request.form.get('name'),
    city = request.form.get('city'),
    state = request.form.get('state'),
    phone = request.form.get('phone'),
    genres = request.form.getlist('genres'),
    facebook_link = request.form.get('facebook_link'),
    image_link = request.form.get('image_link'),
    website_link = request.form.get('website_link'),
    #seeking_venue = request.form.get('seeking_venue'),
    seeking_description = request.form.get('seeking_description')
  )
  insert_model('Artist', artist)
  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[{
    "venue_id": show.venue_id,
    "venue_name": show.venue.name,
    "artist_id": show.artist_id,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link,
    "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
  } for show in Show.query.join(Artist).join(Venue)
  ]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  show = Show(
    artist_id = request.form.get('artist_id'),
    venue_id = request.form.get('venue_id'),
    start_time = request.form.get('start_time')
  )
  insert_model('Show', show)
  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

def insert_model(type, model):

  # set error flag
  error = False
  if type != 'Show': 
    model_name = model.name
  else:
    model_name = ''#db.session.query(Artist.name).filter(Artist.id==model.artist_id).first() + db.session.query(Venue.name).filter(Venue.id==model.venue_id).first()
  # insert model into db
  try:
    db.session.add(model)
    db.session.commit()  

  except:
    # in case of an error, rollback changes, toggle error flag
    db.session.rollback()
    error = True
    #print(sys.exc_info())
    
  finally:
    db.session.close()

  # handle error message
  if error:
      flash('Error: '+type + model_name + ' could not be listed!')
  else:
      flash('Success: ' + type + ' ' + model_name + ' was successfully listed!')

def update_model(type, model):
  
  # set error flag
  error = False

  if type != 'Show': 
    model_name = model.name
  else:
    model_name = ''#model.artist.name+" @"+model.venue.name

  # commit edited model to db
  try:
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())  
  finally:
    db.session.close()

  # check for error and notify user
  if error:
      flash('Error: '+type +' ' + model_name + ' could not be updated!')
  else:
      flash('Success: ' + type + ' ' + model_name + ' was successfully updated!')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
