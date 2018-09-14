import numpy as np


def geodetic2geocentric(theta, alt):
    """
    Conversion from geodetic to geocentric coordinates by using the WGS84 spheroid.
    :param theta: colatitude (float, rad)
    :param alt: altitude (float, km)
    :return gccolat: geocentric colatitude (float, rad)
            gclon: geocentric longitude (float, rad)
            r: geocentric radius (float, km)
    """
    ct = np.cos(theta)
    st = np.sin(theta)
    a2 = 40680631.6
    b2 = 40408296.0
    one = a2 * st * st
    two = b2 * ct * ct
    three = one + two
    rho = np.sqrt(three)
    r = np.sqrt(alt * (alt + 2.0 * rho) + (a2 * one + b2 * two) / three)
    cd = (alt + rho) / r
    sd = (a2 - b2) / rho * ct * st / r
    one = ct
    ct = ct * cd - st * sd
    st = st * cd + one * sd
    gccolat = np.arctan2(st, ct)
    gclon = np.arctan2(sd, cd)
    return gccolat, gclon, r


def geocentric2cartesian(lat, lon, rho):
    """
    Conversion from geocentric to cartesian coordinates.
    :param lat: (float, rad)
    :param lon: (float, rad)
    :param rho: (float, km)
    :return: x: (float, km)
             y: (float, km)
             z: (float, km)
    """
    x = rho*np.cos(lat)*np.cos(lon)
    y = rho*np.cos(lat)*np.sin(lon)
    z = rho*np.sin(lat)
    return x, y, z


def cartesian2geocentric(x, y, z):
    """
    Conversion from geocentric to cartesian coordinates.
    :param x: (float, km)
    :param y: (float, km)
    :param z: (float, km)
    :return lat: (float, rad)
            lon: (float, rad)
            rho: (float, km)
    """
    rho = np.sqrt(x*x+y*y+z*z)
    lon = np.arctan2(y, x)
    lat = np.arctan2(z, np.sqrt(x*x+y*y))
    return lat, lon, rho


def rotateVector(vec, alpha, beta):
    """
    Rotate Vector from spherical coordinate to cartesian coordinate.
    :param vec: [north, east, down] (list(float))
    :param alpha: azimuth angle with anticlockwise (float, rad)
    :param beta: elevating angle (float, rad)
    :return vec: [x, y, z] (list(float))
    """
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    cb = np.cos(beta)
    sb = np.sin(beta)
    spanMat = np.array([[-sb*ca, -sa, -cb*ca],
                       [-sb*sa,   ca,     -cb*sa],
                       [cb,        0,  -sb]])
    return np.dot(spanMat, vec)
