
import argparse

parser = argparse.ArgumentParser(
    description="Manage basics operations on your databse")

parser.add_argument("dropTables", type=bool, default=True)

args = parser.parse_args()
