import psycopg2
from select import select


class PGChannels:
	'''
	Simple wrapper utilizing PostgreSQL's LISTEN and NOTIFY
	commands to make implentation easier.
	'''


	def __init__(self, connection=None, **kwargs):
		'''
		Constructor that accepts a Psycopg2 connection or
		dan key word args to construct one.
		'''

		if connection:
			self.conn = connection
		else:
			self.conn = psycopg2.connect(**kwargs)
		self.conn.autocommit = True
		self.channels = []


	def listen(self, channel):
		'''
		Subscribes to the specified channel.
		'''

		if channel not in self.channels:
			with self.conn.cursor() as cur:
				cur.execute(f"LISTEN {channel};")
			self.channels.append(channel)


	def unlisten(self, channel):
		'''
		Unsubscribe to the specified channel.
		'''

		if channel in self.channels:
			with self.conn.cursor() as cur:
				cur.execute(f"UNLISTEN {channel};")
			self.channels.remove(channel)


	def unlisten_all(self):
		'''
		Unsubscribe to all subscribed to channels.
		'''

		for channel in self.channels:
			self.unlisten(channel)
		self.channels = []


	def notify(self, channel, payload=None):
		'''
		Send a notification event with optional payload.
		'''

		with self.conn.cursor() as cur:
			if payload:
				payload = payload if isinstance(payload, str) else str(payload)
				cur.execute("SELECT pg_notify(%s, %s);", (channel, payload))
			else:
				cur.execute(f"NOTIFY {channel};")


	def notify_many(self, channels, payload=None):
		'''
		Sends a notification event to each specified channel
		with optional payload.
		'''

		for channel in channels:
			self.notify(channel, payload)


	def notify_all(self, payload=None):
		'''
		Sends a notification event to every subscribed to channel
		with optional payload.
		'''

		for channel in self.channels:
			self.notify(channel, payload)


	def events(self, channel=None, timeout=0, loop=True):
		'''
		Yields notify events as they are received for the specified
		channel. If no channel is specified, yields notify events from
		all subscribed to channels. If loop argument is False, any
		available notify events are instead returned.
		'''

		while True:

			events = []

			if not select([self.conn], [], [], timeout) == ([], [], []):
				self.conn.poll()
				while self.conn.notifies:
					notify = self.conn.notifies[0]
					if notify.channel == channel or channel is None:
						events.append(notify)
						yield self.conn.notifies.pop(0)

			if not loop:
				return events



	def close(self):
		'''
		Closes the connection to the database.
		'''

		self.conn.close()


def connect(*args, **kwargs):
	'''
	Establishes a connection and returns an initialized
	PG Channels object.
	'''

	connection = psycopg2.connect(*args, **kwargs)
	connection.autocommit = True
	return PGChannels(connection)
