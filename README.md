## PG Channels

Python wrapper for PostgreSQL NOTIFY and LISTEN commands.


#### Installation

```
pip install pg_channels
```


#### Usage

First, establish a connection to the PostgreSQL database:

```python
import pg_channels

pgc = pg_channels.connect(host='localhost', database='mydb')
```

Sending notification events:

```python
pgc.notify('channel_one', 'Some data')
```

Subscribing to a channel and and handling notification events:

```python
# Subscribe (listen) to a specific channel
pgc.listen('channel_two')

# Iterate over any notification events
for event in pgc.events():
	some_func(event.payload)
```