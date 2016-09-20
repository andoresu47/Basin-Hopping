from Atom import Atom
import random
import math


def distance(atom1, atom2):
    dist = math.sqrt(math.pow(atom1.x_coordinate - atom2.x_coordinate, 2) +
                     math.pow(atom1.y_coordinate - atom2.y_coordinate, 2) +
                     math.pow(atom1.z_coordinate - atom2.z_coordinate, 2))
    return dist


class AtomicStructure:
    # This class generates a structure with free coordinates, with the first atom centered
    # at the origin.
    def __init__(self, number_of_atoms, separation_lower_bound, separation_upper_bound):
        self.atoms = []
        self.number_of_atoms = int(number_of_atoms)
        self.separation_lower_bound = float(separation_lower_bound)
        self.separation_upper_bound = float(separation_upper_bound)

        self.randomize()

    def randomize(self):
        for i in range(0, self.number_of_atoms):
            self.atoms.append(self.generate_atom())

    # Generates random positioned atom and validates its respective distance with
    # previously positioned atoms
    def generate_atom(self):
        condition = 0
        if not self.atoms:
            atom = Atom("n", 0, 0, 0)
        else:
            atom_temp = None
            while condition == 0:
                theta = random.uniform(0, 2 * math.pi)
                phi = random.uniform(0, 2 * math.pi)
                r = random.uniform(self.separation_lower_bound, self.separation_upper_bound)

                random_list_index = random.randint(0, len(self.atoms) - 1)

                x = self.atoms[random_list_index].x_coordinate + (r * math.cos(theta) * math.sin(phi))
                y = self.atoms[random_list_index].y_coordinate + (r * math.sin(theta) * math.sin(phi))
                z = self.atoms[random_list_index].z_coordinate + (r * math.cos(phi))

                atom_temp = Atom("n", x, y, z)

                for atm in self.atoms:
                    dist = distance(atom_temp, atm)

                    # if dist < self.separation or dist > "empirical factor of 3d likeness":
                    if dist < 1.2 or dist > (self.number_of_atoms + 1) * random.uniform(0.2,
                                                                                  0.4) * self.separation_lower_bound:
                        condition = 0
                        break
                    else:
                        condition = 1

            atom = atom_temp

        return atom

    # Method that returns the minimum z coordinate value of the
    # generated cluster.
    def get_min_z(self):
        minimum = self.atoms[0].z_coordinate
        for atm in self.atoms:
            current = atm.z_coordinate
            if current < minimum:
                minimum = current
        return minimum

    # Method that returns the maximum z coordinate value of the
    # generated cluster.
    def get_max_z(self):
        maximum = self.atoms[0].z_coordinate
        for atm in self.atoms:
            current = atm.z_coordinate
            if current > maximum:
                maximum = current
        return maximum

    # Method that returns the minimum y coordinate value of the
    # generated cluster.
    def get_min_y(self):
        minimum = self.atoms[0].y_coordinate
        for atm in self.atoms:
            current = atm.y_coordinate
            if current < minimum:
                minimum = current
        return minimum

    # Method that returns the maximum y coordinate value of the
    # generated cluster.
    def get_max_y(self):
        maximum = self.atoms[0].y_coordinate
        for atm in self.atoms:
            current = atm.y_coordinate
            if current > maximum:
                maximum = current
        return maximum

    # Method that returns the minimum z coordinate value of the
    # generated cluster.
    def get_min_x(self):
        minimum = self.atoms[0].x_coordinate
        for atm in self.atoms:
            current = atm.x_coordinate
            if current < minimum:
                minimum = current
        return minimum

    # Method that returns the maximum z coordinate value of the
    # generated cluster.
    def get_max_x(self):
        maximum = self.atoms[0].x_coordinate
        for atm in self.atoms:
            current = atm.x_coordinate
            if current > maximum:
                maximum = current
        return maximum

    # Method that returns the relative size of the cluster at the x coordinate
    def get_size_x(self):
        return self.get_max_x() - self.get_min_x()

    # Method that returns the relative size of the cluster at the y coordinate
    def get_size_y(self):
        return self.get_max_y() - self.get_min_y()

    # Method that returns the relative size of the cluster at the z coordinate
    def get_size_z(self):
        return self.get_max_z() - self.get_min_z()
