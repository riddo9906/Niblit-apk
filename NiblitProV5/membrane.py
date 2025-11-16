# membrane.py - device interface abstraction
class Membrane:
    def __init__(self):
        print('[Membrane] device abstraction initialized.')

    def camera_capture(self):
        return {'path': None, 'timestamp': None}

    def get_location(self):
        return {'lat': None, 'lon': None}