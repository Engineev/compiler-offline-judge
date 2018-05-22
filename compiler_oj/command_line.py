import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="the path to the config file", type=str)
    parser.parse_args()
    