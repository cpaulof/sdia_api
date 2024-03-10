import random


class DroneData:
    def __init__(self):
        self.lat = -2.53697577046641
        self.lng = -44.2792379196194
        self.alt = 10

        self.velocity_x = 4.2
        self.velocity_y = 0.1
        self.velocity_z = 0.0

        self.pitch = -15.3
        self.yaw = -55.2
        self.roll = 0.1
    
    def get_data(self):
        return {
            'lat': self.lat,
            'lng': self.lng,
            'alt': self.alt,
            'vel_x': self.velocity_x,
            'vel_y': self.velocity_y,
            'vel_z': self.velocity_z,
            'pitch': self.pitch,
            'roll': self.roll,
            'yaw': self.yaw
        }

    def update_data(self):
        self.lat += random.uniform(-0.000002, 0.000002)
        self.lng += random.uniform(-0.000002, 0.000002)


