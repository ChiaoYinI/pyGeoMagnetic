from goto import with_goto
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import apex
import igrf
import dipLat

FACT = 180./np.pi


@with_goto
def igrf12synOld(isv, date, itype, alt, colat, elong):
    """
     This is a synthesis routine for the 12th generation IGRF as agreed
     in December 2014 by IAGA Working Group V-MOD. It is valid 1900.0 to
     2020.0 inclusive. Values for dates from 1945.0 to 2010.0 inclusive are
     definitive, otherwise they are non-definitive.
    INPUT
     isv   = 0 if main-field values are required
     isv   = 1 if secular variation values are required
     date  = year A.D. Must be greater than or equal to 1900.0 and
             less than or equal to 2025.0. Warning message is given
             for dates greater than 2020.0. Must be double precision.
     itype = 1 if geodetic (spheroid)
     itype = 2 if geocentric (sphere)
     alt   = height in km above sea level if itype = 1
           = distance from centre of Earth in km if itype = 2 (>3485 km)
     colat = colatitude (0-180)
     elong = east-longitude (0-360)
     alt, colat and elong must be double precision.
    OUTPUT
     x     = north component (nT) if isv = 0, nT/year if isv = 1
     y     = east component (nT) if isv = 0, nT/year if isv = 1
     z     = vertical component (nT) if isv = 0, nT/year if isv = 1
     f     = total intensity (nT) if isv = 0, rubbish if isv = 1
     To get the other geomagnetic elements (D, I, H and secular
     variations dD, dH, dI and dF) use routines ptoc and ptocsv.
     Adapted from 8th generation version to include new maximum degree for
     main-field models for 2000.0 and onwards and use WGS84 spheroid instead
     of International Astronomical Union 1966 spheroid as recommended by IAGA
     in July 2003. Reference radius remains as 6371.2 km - it is NOT the mean
     radius (= 6371.0 km) but 6371.2 km is what is used in determining the
     coefficients. Adaptation by Susan Macmillan, August 2003 (for
     9th generation), December 2004, December 2009  \ December 2014.
     Coefficients at 1995.0 incorrectly rounded (rounded up instead of
     to even) included as these are the coefficients published in Excel
     spreadsheet July 2005.
    """

    p, q, cl, sl = [0.] * 105, [0.] * 105, [0.] * 13, [0.] * 13
    gh = igrf.loadCoeffs('igrf12coeffs.txt')

    # set initial values
    x, y, z = 0., 0., 0.

    if (date<1900.0 or date > 2025.0):
        f = 1.0
        print('This subroutine will not work with a date of ' + str(date))
        print('Date must be in the range 1900.0 <= date <= 20205.0')
        print('On return f = 1.0, x = y = z = 0')
        return x, y, z, f
    if (date > 2020.0):
        # not adapt for the model but can calculate
        print('This version of the IGRF is intended for use up to 2020.0.')
        print('values for ' + str(date) + ' will be computed but may be of reduced accuracy')
    if (date >= 2015.0):
        goto .a1
    t = 0.2 * (date - 1900.0)
    ll = int(t)
    t = t - ll
    #
    #     SH models before 1995.0 are only to degree 10
    #
    if (date<1995.0):
        nmx = 10
        nc = nmx * (nmx + 2)
        ll = nc * ll
        kmx = (nmx + 1) * (nmx + 2) / 2
    else:
        nmx = 13
        nc = nmx * (nmx + 2)
        ll = round(0.2 * (date - 1995.0))
        #
        #     19 is the number of SH models that extend to degree 10
        #
        ll = 120 * 19 + nc * ll
        kmx = (nmx + 1) * (nmx + 2) / 2

    tc = 1.0 - t
    if (isv == 1):
        tc = -0.2
        t = 0.2

    goto .a2
    #
    label .a1
    t = date - 2015.0
    tc = 1.0
    if (isv == 1):
        t = 1.0
        tc = 0.0

    #
    #     pointer for last coefficient in pen-ultimate set of MF coefficients...
    #
    ll = 3060
    nmx = 13
    nc = nmx * (nmx + 2)
    kmx = (nmx + 1) * (nmx + 2) / 2
    label .a2
    r = alt
    one = colat * 0.017453292
    ct = np.cos(one)
    st = np.sin(one)
    one = elong * 0.017453292
    cl[0] = np.cos(one)
    sl[0] = np.sin(one)
    cd = 1.0
    sd = 0.0
    l = 1
    m = 1
    n = 0
    if (itype == 2):
        goto .a3
    #
    #     conversion from geodetic to geocentric coordinates
    #     (using the WGS84 spheroid)
    #
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
    #
    label .a3
    ratio = 6371.2 / r
    rr = ratio * ratio
    #
    #     computation of Schmidt quasi-normal coefficients p and x(=q)
    #
    p[0] = 1.0
    p[2] = st
    q[0] = 0.0
    q[2] = ct

    for k in range(2, int(kmx)+1):
        if (n >= m):
            goto .a4
        m = 0
        n = n + 1
        rr = rr * ratio
        fn = n
        gn = n - 1
        label .a4
        fm = m
        if (m != n):
            goto .a5
        if (k == 3):
            goto .a6
        one = np.sqrt(1.0 - 0.5 / fm)
        j = k - n - 1
        p[k-1] = one * st * p[j-1]
        q[k-1] = one * (st * q[j-1] + ct * p[j-1])
        cl[m-1] = cl[m - 2] * cl[0] - sl[m - 2] * sl[0]
        sl[m-1] = sl[m - 2] * cl[0] + cl[m - 2] * sl[0]
        goto .a6
        label .a5
        gmm = m * m
        one = np.sqrt(fn * fn - gmm)
        two = np.sqrt(gn * gn - gmm) / one
        three = (fn + gn) / one
        i = k - n
        j = i - n + 1
        p[k-1] = three * ct * p[i-1] - two * p[j-1]
        q[k-1] = three * (ct * q[i-1] - st * p[i-1]) - two * q[j-1]
        #
        #     synthesis of x, y and z in geocentric coordinates
        #
        label .a6
        lm = ll + l
        # print('g', n, m, k, gh[int(lm-1)], gh[int(lm + nc-1)])
        one = (tc * gh[int(lm-1)] + t * gh[int(lm + nc-1)]) * rr
        if (m == 0):
            goto .a9
        # print('h', n, m, k, gh[int(lm)], gh[int(lm + nc)])
        two = (tc * gh[int(lm)] + t * gh[int(lm + nc)]) * rr
        three = one * cl[m-1] + two * sl[m-1]
        x = x + three * q[k-1]
        z = z - (fn + 1.0) * three * p[k-1]
        if (st == 0.0):
            goto .a7
        y = y + (one * sl[m-1] - two * cl[m-1]) * fm * p[k-1] / st
        goto .a8
        label .a7
        y = y + (one * sl[m-1] - two * cl[m-1]) * q[k-1] * ct
        label .a8
        l = l + 2
        goto .a10
        label .a9
        x = x + one * q[k-1]
        z = z - (fn + 1.0) * one * p[k-1]
        l = l + 1
        label .a10
        m = m+1
    #
    #     conversion to coordinate system specified by itype
    #
    one = x
    x = x * cd + z * sd
    z = z * cd - one * sd
    f = np.sqrt(x * x + y * y + z * z)
    #
    return x, y, z, f


def testIgrf12():
    DATE = 2005.
    ITYPE = 2
    ALT = 6357.43492487
    CLT, XLN = 79.6803854769, -71.805

    # print(test.igrf12synOld(0, 1800.0, ITYPE, ALT, 90-CLT, XLN))
    # print(igrf12syn(0, 1800.0, ITYPE, ALT, CLT, XLN))
    # print(test.igrf12synOld(0, 2017.0, ITYPE, ALT, 90-CLT, XLN))
    # print(igrf12syn(0, 2017.0, ITYPE, ALT, CLT, XLN))
    # print(test.igrf12synOld(0, 2023.0, ITYPE, ALT, 90-CLT, XLN))
    # print(igrf12syn(0, 2023.0, ITYPE, ALT, CLT, XLN))
    # print(test.igrf12synOld(0, 2046.0, ITYPE, ALT, 90-CLT, XLN))
    # print(igrf12syn(0, 2046.0, ITYPE, ALT, CLT, XLN))
    print(igrf12synOld(0, 2005.0, ITYPE, ALT, 90 - CLT, XLN))
    print(igrf.igrf12syn(0, 2005.0, ITYPE, ALT, CLT, XLN))


def sphere(center, radius, ax):
    # data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]

    # surface plot
    ax.plot_surface(x, y, z, rstride=4, cstride=4, color='b')


def draw(trace):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # center and radius
    center = [0, 0, 0]
    radius = 6371.2
    sphere(center, radius, ax)
    ax.plot([x[0] for x in trace], [x[1] for x in trace], [x[2] for x in trace])
    ax.set_zlabel('Z')
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()


def testApex():
    trace = apex.findApex(20, 0, 0)
    draw(trace)


def testDipLat():
    lat = 7.7
    lon = 116
    alt = 0
    year = 2005
    print(dipLat.dipLat(lat, lon, alt, year))


if __name__ == '__main__':
    testDipLat()
