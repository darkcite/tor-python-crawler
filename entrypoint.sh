#!/bin/bash

# Start the Tor service
service tor start

# Wait for Tor to establish a connection
# This is a simple loop that waits for Tor to be ready
while ! curl --silent --socks5-hostname localhost:9050 --connect-timeout 5 http://check.torproject.org/api/ip; do
    echo "Waiting for Tor to start..."
    sleep 2
done

echo "Tor is ready."

# Then execute the command provided to the docker run, or default to the Python script
exec "$@"
