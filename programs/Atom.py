class Atom:
    def __init__(self, a_type, x_coordinate, y_coordinate, z_coordinate):
        self.a_type = a_type
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.z_coordinate = z_coordinate

    # Returns current atomic coordinates
    def get_coordinates(self):
        return [self.x_coordinate, self.y_coordinate, self.z_coordinate]

    # Sets atomic coordinates
    def set_coordinates(self, coord_lst):
        self.x_coordinate = coord_lst[0]
        self.y_coordinate = coord_lst[1]
        self.z_coordinate = coord_lst[2]

    # Returns atomic information as string
    def to_string(self):
        atomic_info = str(self.a_type) + "\t" + str(self.x_coordinate) + "\t" + str(self.y_coordinate) + "\t" + str(self.z_coordinate) + "\n"
        return atomic_info
