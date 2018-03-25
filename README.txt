Running service:

To run the service execute main.py.  This will launch a local server in a separate thread on port 8000.
To stop the service type "exit" into the console and the server will be stopped.


Using the service:

With the server running you can send queries by sending GET requests:
http://127.0.0.1:8000/geocode/json
?address=2727%Milvia%St,%Berkeley,%CA%94703

The response will return a JSON object with latitude and longitude or null if no records are found.
{"lat": 37.85958, "lng": -122.26939}
