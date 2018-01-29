from setuptools import setup

setup(
	name = 'pg_channels',
	packages = ['pg_channels'],
	version = '0.1',
	license='MIT',
	description = 'Python wrapper for PostgreSQL NOTIFY and LISTEN commands.',
	author = 'Nick Moore',
	author_email = 'nickdmoore@gmail.com',
	url = 'https://github.com/nickdmoore/pg_channels',
	keywords = ['PostgreSQL', 'NOTIFY', 'LISTEN', 'channels'],
	install_requires=[
		'psycopg2>=2.7.3.2'
	],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.6'
	]
)