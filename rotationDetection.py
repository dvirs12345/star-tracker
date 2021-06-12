import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import math

SValue = 12000000


def calc_distance(x1, x2, y1, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))  # Distance between two points formula


def get_distances(df, myid):
    """ returns the distance between a star and all the others"""
    mystar = df[df["id"] == myid]
    others = df[df["id"] != myid]
    distdict = {}
    for index, row in others.iterrows():
        distdict[row["id"]] = calc_distance(row['x'], mystar['x'], row['y'], mystar['y'])

    print(distdict)
    return distdict


def update_distance(df):
    """ Updates the df with the distances"""
    df["Pdistances"] = None
    for index, row in df.iterrows():
        df["Pdistances"][index] = get_distances(df, row["id"])

    return df


def load_detection_result(filename):
    """ Loads the data and returns the df with all the info """
    file1 = open(filename, 'r')
    Lines = file1.readlines()

    df = pd.DataFrame(None, columns=['x', 'y', 'type'])
    for line in Lines:
        split1 = line.split('\n')  # Remove \n
        split2 = split1[0].split(",")
        for i in range(len(split2)):  # Remove whitespaces and turns string into float
            split2[i] = float(split2[i].strip())

        myseries = pd.Series(split2, index=df.columns)
        df = df.append(myseries, ignore_index=True)

    df["id"] = range(df.shape[0])

    return df


def load_star_data(filename, max_visible):
    """ Loads the Yale star dataset and remove unneeded values """
    mycsv = pd.read_csv(filename)
    mycsv = mycsv[["id", "ra", "proper", "dec", "x", "y", "z", "mag"]]  # Have only the vars for distance calculation
    mycsv = mycsv[mycsv["mag"] <= max_visible]  # Remove the stars that we can't see with the naked eye = 6
    mycsv = mycsv[mycsv["id"] != 0]  # Remove the sun
    print(mycsv.head())
    print(mycsv.shape)
    return mycsv


def calc_AD(stardf, id1, id2):
    """ calculates AD of two stars """
    dec1 = stardf.loc[stardf["id"] == id1, "dec"]
    dec2 = stardf.loc[stardf["id"] == id2, "dec"]
    ra1 = stardf.loc[stardf["id"] == id1, "ra"]
    ra2 = stardf.loc[stardf["id"] == id2, "ra"]

    return math.sin(dec1) * math.sin(dec2) + math.cos(dec1) * math.cos(dec2) * math.cos(ra1 - ra2)  # formula for AD


def calc_SPD(S, AD):
    """ Calculates StarPixelDistance """
    return S * AD


def update_angular_distance(stardf):
    """ Updates the angular distance for a star with all the others in pixels (stardf) """
    stardf["pdistances"] = None
    for index, row in stardf.iterrows():
        stardf["pdistances"][index] = get_star_distances(stardf, row['id'])

    return stardf


def get_star_distances(stardf, myid):
    """ Returns the angular distance between a star and all the others """
    mystar = stardf[stardf["id"] == myid]
    others = stardf[stardf["id"] != myid]
    distdict = {}
    for index, row in others.iterrows():
        distdict[row["id"]] = calc_SPD(SValue, calc_AD(stardf, myid, row["id"]))

    return distdict


def search_distances(stardf, dist):
    possiblities = []
    for index, row in stardf.iterrows():
        temp = row["pdistances"]
        for key in temp:
            if temp[key] == dist:
                possiblities.append(key)

    return possiblities


def main():
    mypic1 = cv2.imread('pic1.jpg')

    Original_Image = Image.open("pic1.jpg")

    rotated_image1 = Original_Image.rotate(90)
    plt.imshow(rotated_image1)
    # plt.show()
    rotated_image1.save("pic1r.jpg")

    df = load_detection_result("pic1.jpg_res.txt")
    df = update_distance(df)
    # print(df.head())

    load_star_data("hygdata_v3.csv", 6)


main()
