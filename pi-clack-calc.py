#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
https://www.youtube.com/watch?v=HEfHFsfGXjs
https://www.youtube.com/watch?v=abv4Fz7oNr0
"""

import sys
from decimal import *

class Object:
    def __init__(self, position, mass=None, velocity=Decimal(0), is_static=False):
        self.position = position
        self.mass = mass
        self.velocity = velocity

        self.is_static = is_static
        if is_static:
            self.mass = None
            self.velocity = Decimal(0)

    def collides_with_in(self, other):
        if self is other or self.is_static and other.is_static:
            return None

        if self.velocity > other.velocity and self.position < other.position:
            return (other.position - self.position) / (self.velocity - other.velocity)

        if self.velocity < other.velocity and self.position > other.position:
            return (self.position - other.position) / (other.velocity - self.velocity)

        return None

    def collide(self, other, t):
        # Theory:
        self.position += self.velocity * t
        other.position += other.velocity * t

        # Practice:
        # Due to precision issues, this ensures that collided objects are actually collided.
        if self.is_static:
            other.position = self.position
        else: # other.is_static or both or non-static.
            self.position = other.position

        if self.is_static:
            other.velocity = -other.velocity
        elif other.is_static:
            self.velocity = -self.velocity
        else:
            new_self_velocity = ((self.mass - other.mass) * self.velocity + Decimal(2) * other.mass * other.velocity) / (self.mass + other.mass)
            new_other_velocity = ((other.mass - self.mass) * other.velocity + Decimal(2) * self.mass * self.velocity) / (self.mass + other.mass)
            self.velocity = new_self_velocity
            other.velocity = new_other_velocity

def find_nearest_collision(objects):
    nearest_collision_time = None
    nearest_collision_object_1 = None
    nearest_collision_object_2 = None

    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            collision_time = objects[i].collides_with_in(objects[j])
            if not(collision_time is None) and (nearest_collision_time is None or collision_time < nearest_collision_time):
                nearest_collision_time = collision_time
                nearest_collision_object_1 = i
                nearest_collision_object_2 = j

    if nearest_collision_time is None:
        return None

    return (nearest_collision_time, objects[nearest_collision_object_1], objects[nearest_collision_object_2])

def main(n):
    wall = Object(position=Decimal(0), is_static=True)
    small_box = Object(mass=Decimal(1), position=Decimal(10))
    big_box = Object(mass=Decimal(100) ** n, position=Decimal(100), velocity=Decimal(-1))

    objects = [ wall, small_box, big_box ]

    collision_count = 0
    while True:
        nearest_collision = find_nearest_collision(objects)
        if nearest_collision is None:
            break

        collision_count = collision_count + 1
        nearest_collision_time, nearest_collision_object_1, nearest_collision_object_2 = nearest_collision
        nearest_collision_object_1.collide(nearest_collision_object_2, nearest_collision_time)

    print("collision_count: {}".format(collision_count))
    return 0

if "__main__" == __name__:
    n = Decimal(0)

    if 2 == len(sys.argv):
        n = Decimal(int(sys.argv[1]))
    elif 2 < len(sys.argv):
        print("Usage:\n\t{} N".format(sys.argv[0]))
        sys.exit(-1)

    # Maybe play with it.
    # getcontext().prec = 28
    sys.exit(main(n))
