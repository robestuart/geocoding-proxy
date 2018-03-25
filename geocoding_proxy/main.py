import rest_server as rs
import time


def main():
    ''' Runs the geocode RESTful service and provides a command line tool to stop it
    '''
    server = rs.GeoCodeServer
    server.start()
    time.sleep(2)  # gives time for server to start up

    text = ''
    while not text == 'exit':
        text = raw_input("type in exit to stop server:\n").strip()

    server.stop()


if __name__ == '__main__':
    main()
