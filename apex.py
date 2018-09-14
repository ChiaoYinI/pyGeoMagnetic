import numpy as np

from coordinate import cartesian2geocentric, geocentric2cartesian, geodetic2geocentric, rotateVector
from igrf import igrf12syn, getCoeffs


FACT = 180./np.pi
R = 6371.2


def itrace(Y, YOLD, YAPX, YP, BX, BY, BZ, BB, SGN, DS, NSTP):
    """
    Follow a geomagnetic field line until passing its apex
    Cartesian component magnetic field (partial) derivitives steer the trace

    This uses the 4-point Adams formula after initialization.
    First 7 iterations advance point by 3 steps.

    INPUTS:
     YAPX  = Matrix of cartesian coordinates of the three points
             about the apex.  Set in itrace.

    FLDCOMD has geomagnetic field at current trace point:
     BX    = X component (nT)
     BY    = Y component (nT)
     BZ    = Z component (nT)
     BB    = Magnitude   (nT)

    itrace has field line tracing variables determined in findApex:
     NSTP  = Step count.
     Y     = Array containing current tracing point cartesian coordinates.
     YOLD  = Array containing previous tracing point cartesian coordinates.
     SGN   = Determines direction of trace.
     DS    = Step size (arc length in km).

    REFERENCES:
     Stassinopoulos E. G. , Mead Gilbert D., X-841-72-17 (1971) GSFC,
     Greenbelt, Maryland
    --------------------------------------------------------------------
    # HISTORY:
    # Oct 1973: Initial version completed on the 29th by W. Clark, NOAA ERL
    #          Laboratory.
    # Feb 1988: Revised by H. Passi, NCAR.
    # Apr 2004: Replace computed GO TO with if blocks because some compilers
    #          are threatening to remove this old feature

    """
    YP[0][3] = SGN * BX / BB
    YP[1][3] = SGN * BY / BB
    YP[2][3] = SGN * BZ / BB
    D2 = DS / 2.
    D6 = DS / 6.
    D12 = DS / 12.
    D24 = DS / 24.
    if NSTP <= 7:
        for I in range(0, 3):
            if NSTP == 1:
                YP[I][0] = YP[I][3]
                YOLD[I] = Y[I]
                YAPX[I][0] = Y[I]
                Y[I] = YOLD[I] + DS * YP[I][0]
            elif NSTP == 2:
                YP[I][1] = YP[I][3]
                Y[I] = YOLD[I] + D2 * (YP[I][1] + YP[I][0])
            elif NSTP == 3:
                Y[I] = YOLD[I] + D6 * (2. * YP[I][3] + YP[I][1] + 3. * YP[I][0])
            elif NSTP == 4:
                YP[I][1] = YP[I][3]
                YAPX[I][1] = Y[I]
                YOLD[I] = Y[I]
                Y[I] = YOLD[I] + D2 * (3.0 * YP[I][1] - YP[I][0])
            elif NSTP == 5:
                Y[I] = YOLD[I] + D12 * (5. * YP[I][3] + 8. * YP[I][1] - YP[I][0])
            elif NSTP == 6:
                YP[I][2] = YP[I][3]
                YOLD[I] = Y[I]
                YAPX[I][2] = Y[I]
                Y[I] = YOLD[I] + D12 * (23. * YP[I][2] - 16. * YP[I][1] + 5. * YP[I][0])
            elif NSTP == 7:
                YAPX[I][0] = YAPX[I][1]
                YAPX[I][1] = YAPX[I][2]
                Y[I] = YOLD[I] + D24 * (9. * YP[I][3] + 19. * YP[I][2] - 5. * YP[I][1] + YP[I][0])
                YAPX[I][2] = Y[I]

        if NSTP == 6 or NSTP == 7:  # signal if apex passed
            RC = np.sqrt(YAPX[0][2]**2 + YAPX[1][2]**2 + YAPX[2][2]**2)
            RP = np.sqrt(YAPX[0][1]**2 + YAPX[1][1]**2 + YAPX[2][1]**2)
            if RC < RP:
                return True
    else:  # NSTP > 7
        for I in range(0, 3):
            YAPX[I][0] = YAPX[I][1]
            YAPX[I][1] = Y[I]
            YOLD[I] = Y[I]
            Y[I] = YOLD[I] + D24 * (55. * YP[I][3] - 59. * YP[I][2] + 37. * YP[I][1] - 9. * YP[I][0])
            YAPX[I][2] = Y[I]
            for J in range(0, 3):
                YP[I][J] = YP[I][J + 1]
        RC = np.sqrt(Y[0]**2 + Y[1]**2 + Y[2]**2)
        RP = np.sqrt(YOLD[0]**2 + YOLD[1]**2 + YOLD[2]**2)
        if RC < RP:
            return True
    return False


def northPole(date):
    """
    Calculate the position of north pole at the first order approximation.
    :param date: years(float year)
    :return: lat(float deg) lon(float deg)
    """
    g, h = getCoeffs(date)
    colat = np.arccos(g[1][0]/np.sqrt(g[1][0]**2 + g[1][1]**2 + h[1][1]**2))
    elong = np.arctan2(h[1][1], g[1][1])
    return colat*FACT-90, elong*FACT-180


def findApex(lat, lon, alt, date=2005.):
    """
    Follow a geomagnetic field line until passing its apex.
    :param lat: latitude of start position(float deg)
    :param lon: longitude of start position(float deg)
    :param alt: altitude of start position(float deg)
    :param date: years(year)
    :return: trace: dots of the field line(list([float, float, float]) km)
    """
    nlat, nlon = northPole(date)
    nlat, nlon = nlat/FACT, nlon/FACT
    ctp = np.cos(np.pi/2-nlat)
    stp = np.sin(np.pi/2-nlat)

    gccolat, plon, gcrho = geodetic2geocentric(np.pi/2-lat/FACT, alt)
    gclat, gclon = np.pi/2-gccolat, lon/FACT
    x0, y0, z0 = geocentric2cartesian(gclat, gclon, gcrho)
    bx, by, bz, bb = igrf12syn(0, date, 2, gcrho, gclat * FACT, gclon * FACT)

    sgn = -np.sign(bz)
    trace = [[x0, y0, z0]]
    YAPX = np.array([[0.]*3]*3)
    step = 0
    arrive = False
    Y = [x0, y0, z0]
    YOLD = [0, 0, 0]
    YP = [[0., 0., 0., 0.],
          [0., 0., 0., 0.],
          [0., 0., 0., 0.]]
    while not arrive and step < 100:
        stngml = ctp*np.sin(gclat)+stp*np.cos(gclat)*np.cos(gclon-nlon)
        cgml2 = max(1-stngml**2, 0.25)
        DS = gcrho*0.06/cgml2-370

        bx, by, bz, bb = igrf12syn(0, date, 2, gcrho, gclat * FACT, gclon * FACT)
        Bx, By, Bz = rotateVector([bx, by, bz], gclon, gclat)

        arrive = itrace(Y, YOLD, YAPX, YP, Bx, By, Bz, bb, sgn, DS, step)
        step += 1
        gclat, gclon, gcrho = cartesian2geocentric(Y[0], Y[1], Y[2])
        trace.append(Y[:])
    return trace
