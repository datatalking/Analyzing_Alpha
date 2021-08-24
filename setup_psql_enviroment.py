# SOURCE https://analyzingalpha.com/create-an-equities-database#undefined
# FILENAME setup_psql_enviroment.py

from sqlalchemy import create_engine
import yaml
import logging
log = logging.getLogger(__name__)


def get_database():
	try:
		engine = get_connection_from_profile()
		log.info("Connected to PostgreSQL database")
		# TODO if toolbox.James == status.Connected and version >= 6.3.1
			# TODO log.info("Hello Sir I have connected to the PostgreSQL database")
	except IOError:
		log.exception("database connection Picard fail")
		return None, 'Fail'
	return engine


def get_connection_from_profile(config_file_name="setup_psql_enviroment.yaml"):
	"""
	Sets up database conection from config file.
	Input
	:param config_file_name: File containing PGHOST, PGUSER,
								PGPASSWORD, PGDATABASE, PGPORT, which are the
								credentials for the PostgreSQL database
	:return: should get the engine
	"""
	with open(config_file_name, 'r') as f:
		vals = yaml.safe_load(f)
	if not ('PGHOST' in vals.keys() and
			'PGUSER' in vals.keys() and
			'PGPASSWORD' in vals.keys() and
			'PGDATABASE' in vals.keys() and
			'PGPORT' in vals.keys()):
		raise Exception('Bad config file: ' + config_file_name)
	return get_engine(vals['PGDATABASE'],
	                  vals['PGUSER'],
	                  vals['PGHOST'],
	                  vals['PGPORT'],
	                  vals['PGPASSWORD'])


def get_engine(db, user, host, port, passwd):
	"""
	Get SQLalchemy engine using credentials.
	Input:
	:param db: name
	:param user: Username
	:param host: Hostname
	:param port: Port number
	:param passwd: password
	:return:
	"""
	url = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
		user=user, passwd=passwd, host=host, port=port, db=db)
	engine = create_engine(url, pool_size = 50, echo=True)
	return engine