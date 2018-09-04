from goto import with_goto
import numpy as np

FACT = 180./np.pi

# @with_goto
# def igrf12():
#     #
#     #     This is a program for synthesising geomagnetic field values from the
#     #     International Geomagnetic Reference Field series of models as agreed
#     #     in December 2014 by IAGA Working Group V-MOD.
#     #     It is the 12th generation IGRF, ie the 11th revision.
#     #     The main-field models for 1900.0, 1905.0,..1940.0 and 2015.0 are
#     #     non-definitive, those for 1945.0, 1950.0,...2010.0 are definitive and
#     #     the secular-variation model for 2015.0 to 2020.0 is non-definitive.
#     #
#     #     Main-field models are to degree and order 10 (ie 120 coefficients)
#     #     for 1900.0-1995.0 and to 13 (ie 195 coefficients) for 2000.0 onwards.
#     #     The predictive secular-variation model is to degree and order 8 (ie 80
#     #     coefficients).
#     #
#     #     Options include values at different locations at different
#     #     times (spot), values at same location at one year intervals
#     #     (time series), grid of values at one time (grid); geodetic or
#     #     geocentric coordinates, latitude  \ longitude entered as decimal
#     #     degrees or degrees  \ minutes (not in grid), choice of main field
#     #     or secular variation or both (grid only).
#     # Recent history of code:
#     #     Aug 2003:
#     #     Adapted from 8th generation version to include new maximum degree for
#     #     main-field models for 2000.0 and onwards and use WGS84 spheroid instead
#     #     of International Astronomical Union 1966 spheroid as recommended by IAGA
#     #     in July 2003. Reference radius remains as 6371.2 km - it is NOT the mean
#     #     radius (= 6371.0 km) but 6371.2 km is what is used in determining the
#     #     coefficients.
#     #     Dec 2004:
#     #     Adapted for 10th generation
#     #     Jul 2005:
#     #     1995.0 coefficients as published in igrf9coeffs.xls and igrf10coeffs.xls
#     #     now used in code - (Kimmo Korhonen spotted 1 nT difference in 11 coefficients)
#     #     Dec 2009:
#     #     Adapted for 11th generation
#     #     Dec 2014:
#     #     Adapted for 12th generation
#     #
#     IA = ''
#     TYPE = ''
#     NAME = ''
#     FNM = ''
#     DTMN, DTMX = 1900.0, 2025.0
#     print("""
#
#     ******************************************************
#     *              IGRF SYNTHESIS PROGRAM                *
#     *                                                    *
#     * A program for the computation of geomagnetic       *
#     * field elements from the International Geomagnetic  *
#     * Reference Field (12th generation) as revised in    *
#     * December 2014 by the IAGA Working Group V-MOD.     *
#     *                                                    *
#     * It is valid for dates from 1900.0 to 2020.0,       *
#     * values up to 2025.0 will be computed but with      *
#     * reduced accuracy. Values for dates before 1945.0   *
#     * and after 2010.0 are non-definitive, otherwise the *
#     * values are definitive.                             *
#     *                                                    *
#     * Susan Macmillan          British Geological Survey *
#     *                           IAGA Working Group V-MOD *
#     ******************************************************
#
#     Enter name of output file
#     or press "Return" for output to screen
#
#     """)
#     FNM = input()
#     label .a991
#     # FORMAT(A30)
#     # if (ICHAR(FNM(1 : 1))==32):
#     #     IU = 6
#     # else:
#     #     IU = 2
#     #     OPEN (UNIT = IU, FILE = FNM, STATUS = 'NEW')
#
#     FACT = 180.0 / np.pi
#     NCOUNT = 0
#     #
#     label .a10
#     print('Enter value for coordinate system:')
#     print('1 - geodetic (shape of Earth is approximated by a spheroid)')
#     print('2 - geocentric (shape of Earth is approximated by a sphere)')
#     ITYPE = int(input())
#
#     if (ITYPE < 1 or ITYPE > 2):
#         goto.a10
#     if (ITYPE == 1):
#         TYPE = ' geodetic  '
#     if (ITYPE == 2):
#         TYPE = ' geocentric'
#     #
#     label.a20
#     print('Choose an option:')
#     print('1 - values at one or more locations  \ dates')
#     print('2 - values at yearly intervals at one location')
#     print('3 - values on a latitude/longitude grid at one date')
#     IOPT = int(input())
#     if (IOPT < 1 or IOPT > 3):
#         goto.a20
#     if (IOPT == 3):
#         goto.a150
#     #
#     label.a30
#     print('Enter value for format of latitudes and longitudes:')
#     print('1 - in degrees  \ minutes')
#     print('2 - in decimal degrees')
#     IDM = int(input())
#     if (IDM < 1 or IDM > 2):
#         goto.a30
#     if (NCOUNT == 0):
#         goto.a50
#     #
#     label.a40
#     print('Do you want values for another date  \ position? (y/n)')
#     IA = input()
#     if (IA != 'Y' and IA != 'y' and IA != 'N' and IA != 'n'):
#         goto.a40
#     if (IA == 'N' or IA == 'n'):
#         print(
#             """
#                  D is declination (+ve east)
#                  I is inclination (+ve down)
#                  H is horizontal intensity
#                  X is north component
#                  Y is east component
#                  Z is vertical component (+ve down)
#                  F is total intensity
#             """
#         )
#         print(
#             """
#                 SV is secular variation (annual rate of change)
#             """
#         )
#         if ITYPE == 2:
#             print('These elements are relative to the geocentric coordinate system')
#         else:
#             print()
#
#         return 'end'
#
#     #
#     label.a50
#     NCOUNT = 1
#     if IOPT != 2:
#         print('Enter date in years A.D.')
#         DATE = float(input())
#         if DATE < DTMN or DATE > DTMX:
#             goto.a209
#
#     if ITYPE == 1:
#         print('Enter altitude in km')
#     else:
#         print('Enter radial distance in km (>3485 km)')
#
#     ALT = float(input())
#     if (ITYPE == 2 and ALT <= 3485.0):
#         goto.a210
#     #
#     if IDM == 1:
#         print('Enter latitude  \ longitude in degrees  \ minutes')
#         print('(if either latitude or longitude is between -1')
#         print('and 0 degrees, enter the minutes as negative).')
#         print('Enter 4 integers')
#
#         LTD = int(input())
#         LTM = int(input())
#         LND = int(input())
#         LNM = int(input())
#         if LTD < -90 or LTD > 90 or LTM <= -60 or LTM >= 60:
#             goto.a204
#         if LND < -360 or LND > 360 or LNM <= -60 or LNM >= 60:
#             goto.a205
#         if LTM < 0 and LTD != 0:
#             goto.a204
#         if LNM < 0 and LND != 0:
#             goto.a205
#         XLT = DMDDEC(LTD, LTM)
#         XLN = DMDDEC(LND, LNM)
#     else:
#         print('Enter latitude  \ longitude in decimal degrees')
#         XLT = float(input())
#         XLN = float(input())
#         if (XLT < -90.0  or XLT > 90.0):
#             goto .a202
#         if (XLN < -360.0  or XLN > 360.0):
#             goto .a203
#
#     #
#     print('Enter place name (20 characters maximum)')
#     NAME = input()
#     CLT = 90.0 - XLT
#     if CLT < 0.0  or CLT > 180.0:
#         goto .a204
#     if XLN <= -360.0  or XLN >= 360.0:
#         goto .a205
#     if IOPT == 2:
#         goto .a60
#     #
#     X, Y, Z, F = igrf12syn(0, DATE, ITYPE, ALT, CLT, XLN)
#     D = FACT * np.arctan2(Y, X)
#     H = np.sqrt(X * X + Y * Y)
#     S = FACT * np.arctan2(Z, H)
#     IDEC, IDECM = DDECDM(D)
#     INC, INCM = DDECDM(S)
#     #
#     DX, DY, DZ, F1 = igrf12syn(1, DATE, ITYPE, ALT, CLT, XLN)
#     DD = (60.0 * FACT * (X * DY - Y * DX)) / (H * H)
#     DH = (X * DX + Y * DY) / H
#     DS = (60.0 * FACT * (H * DZ - Z * DH)) / (F * F)
#     DF = (H * DH + Z * DZ) / F
#     #
#     if IDM == 1:
#         print()
#         # WRITE(IU, 930) DATE, LTD, LTM, TYPE, LND, LNM, ALT, NAME
#         # 930  FORMAT (1X, F8.3, ' Lat', 2I4, A11, ' Long ', 2I4, F10.3, ' km ', A20)
#     else:
#         print()
#         # WRITE(IU, 931) DATE, XLT, TYPE, XLN, ALT, NAME
#         # 931  FORMAT (1X, F8.3, ' Lat', F8.3, A11, ' Long ', F8.3, F10.3, ' km ', A20)
#
#     #
#     IDD = NINT(DD)
#     WRITE(IU, 937) IDEC, IDECM, IDD
#     937 FORMAT (15X, 'D =', I5, ' deg', I4, ' min', 4X, 'SV =', I8, ' min/yr')
#     #
#     IDS = NINT(DS)
#     WRITE(IU, 939) INC, INCM, IDS
#     939 FORMAT (15X, 'I =', I5, ' deg', I4, ' min', 4X, 'SV =', I8, ' min/yr')
#     #
#     IH = NINT(H)
#     IDH = NINT(DH)
#     WRITE(IU, 941) IH, IDH
#     941 FORMAT (15X, 'H =', I8, ' nT     ', 5X, 'SV =', I8, ' nT/yr')
#     #
#     IX = NINT(X)
#     IDX = NINT(DX)
#     WRITE(IU, 943) IX, IDX
#     943 FORMAT (15X, 'X =', I8, ' nT     ', 5X, 'SV =', I8, ' nT/yr')
#     #
#     IY = NINT(Y)
#     IDY = NINT(DY)
#     WRITE(IU, 945) IY, IDY
#     945 FORMAT (15X, 'Y =', I8, ' nT     ', 5X, 'SV =', I8, ' nT/yr')
#     #
#     IZ = NINT(Z)
#     IDZ = NINT(DZ)
#     WRITE(IU, 947) IZ, IDZ
#     947 FORMAT (15X, 'Z =', I8, ' nT     ', 5X, 'SV =', I8, ' nT/yr')
#     #
#     NF = NINT(F)
#     IDF = NINT(DF)
#     WRITE(IU, 949) NF, IDF
#     949 FORMAT (15X, 'F =', I8, ' nT     ', 5X, 'SV =', I8, ' nT/yr'/)
#     #
#     goto .a40
#     #
#     label .a60
#     CONTINUE
#     #
#     #     SERIES OF VALUES AT ONE LOCATION...
#     #
#     if IDM == 1:
#         pass
#         # WRITE(IU, 932) LTD, LTM, TYPE, LND, LNM, ALT, NAME
#         # 932  FORMAT ('Lat', 2I4, A11, '  Long ', 2I4, F10.3, ' km ', A20)
#     else:
#         pass
#         # WRITE(IU, 933) XLT, TYPE, XLN, ALT, NAME
#         # 933  FORMAT ('Lat', F8.3, A11, '  Long ', F8.3, F10.3, ' km ', A20)
#
#     WRITE (IU, 934)
#     934 FORMAT (3X, 'DATE', 7X, 'D', 3X, 'SV', 6X, 'I', 2X, 'SV', 6X, 'H', 4X, 'SV',  \
#             7X, 'X', 4X, 'SV', 7X, 'Y', 4X, 'SV', 7X, 'Z', 4X, 'SV', 6X, 'F', 4X, 'SV')
#     IMX = DTMX - DTMN - 5
#     DO 70 I = 1, IMX
#         DATE = DTMN - 0.5 + I
#         CALL IGRF12SYN (0, DATE, ITYPE, ALT, CLT, XLN, X, Y, Z, F)
#         D = FACT * ATAN2(Y, X)
#         H = SQRT(X * X + Y * Y)
#         S = FACT * ATAN2(Z, H)
#         IH = NINT(H)
#         IX = NINT(X)
#         IY = NINT(Y)
#         IZ = NINT(Z)
#         NF = NINT(F)
#         #
#         CALL IGRF12SYN (1, DATE, ITYPE, ALT, CLT, XLN, DX, DY, DZ, F1)
#         DD = (60.0 * FACT * (X * DY - Y * DX)) / (H * H)
#         DH = (X * DX + Y * DY) / H
#         DS = (60.0 * FACT * (H * DZ - Z * DH)) / (F * F)
#         DF = (H * DH + Z * DZ) / F
#         IDD = NINT(DD)
#         IDH = NINT(DH)
#         IDS = NINT(DS)
#         IDX = NINT(DX)
#         IDY = NINT(DY)
#         IDZ = NINT(DZ)
#         IDF = NINT(DF)
#         #
#         WRITE(IU, 935) \
#                 DATE, D, IDD, S, IDS, IH, IDH, IX, IDX, IY, IDY, IZ, IDZ, NF, IDF
#         935 FORMAT(1X, F6.1, F8.2, I5, F7.2, I4, I7, I6, 3(I8, I6), I7, I6)
#     70 CONTINUE
#     ifL = 2
#     goto .a158
#     #
#     #     GRID OF VALUES...
#     #
#     label .a150
#     print('Enter value for MF/SV flag:')
#     print('0 for main field (MF)')
#     print('1 for secular variation (SV)')
#     print('2 for both')
#     print('9 to quit')
#     READ (5, *) ifL
#     if (ifL == 9):
#         STOP
#     if (ifL != 0.AND.ifL != 1.AND.ifL != 2):
#         goto .a150
#     #
#     print('Enter initial value, final value  \ increment or')
#     print('decrement of latitude, in degrees  \ decimals')
#     READ (5, *) XLTI, XLTF, XLTD
#     LTI = NINT(1000.0 * XLTI)
#     LTF = NINT(1000.0 * XLTF)
#     LTD = NINT(1000.0 * XLTD)
#     print('Enter initial value, final value  \ increment or')
#     print('decrement of longitude, in degrees  \ decimals')
#     READ (5, *) XLNI, XLNF, XLND
#     LNI = NINT(1000.0 * XLNI)
#     LNF = NINT(1000.0 * XLNF)
#     LND = NINT(1000.0 * XLND)
#     if (LTI < -90000  or LTI > 90000):
#         goto .a206
#     if (LTF < -90000  or LTF > 90000):
#         goto .a206
#     if (LNI < -360000  or LNI > 360000):
#         goto .a207
#     if (LNF < -360000  or LNF > 360000):
#         goto .a207
#     label .a98
#     print('Enter date in years A.D.')
#     READ (5, *) DATE
#     if (DATE < DTMN  or DATE > DTMX):
#         goto .a 209
#     if (ITYPE == 1) :
#         print('Enter altitude in km')
#     else:
#         print('Enter radial distance in km (>3485 km)')
#
#     READ (5, *) ALT
#     if (ITYPE == 2.AND.ALT <= 3485.0) goto .a 210
#     WRITE(IU, 958) DATE, ALT, TYPE
#     958 FORMAT (' Date =', F9.3, 5X, 'Altitude =', F10.3, ' km', 5X, A11// \
#             '      Lat     Long', 7X, 'D', 7X, 'I', 7X, 'H', 7X, 'X', 7X, 'Y',  \
#             7X, 'Z', 7X, 'F')
#     #
#     LT = LTI
#     151 XLT = LT
#     XLT = 0.001 * XLT
#     CLT = 90.0 - XLT
#     if (CLT < -0.001  or CLT > 180.001) goto .a 202
#     LN = LNI
#     152 XLN = LN
#     XLN = 0.001 * XLN
#     if (XLN <= -360.0) XLN = XLN + 360.0
#     if (XLN >= 360.0) XLN = XLN - 360.0
#     CALL IGRF12SYN (0, DATE, ITYPE, ALT, CLT, XLN, X, Y, Z, F)
#     D = FACT * ATAN2(Y, X)
#     H = SQRT(X * X + Y * Y)
#     S = FACT * ATAN2(Z, H)
#     IH = NINT(H)
#     IX = NINT(X)
#     IY = NINT(Y)
#     IZ = NINT(Z)
#     NF = NINT(F)
#     if (ifL == 0) GOTO 153
#     CALL IGRF12SYN (1, DATE, ITYPE, ALT, CLT, XLN, DX, DY, DZ, F1)
#     IDX = NINT(DX)
#     IDY = NINT(DY)
#     IDZ = NINT(DZ)
#     DD = (60.0 * FACT * (X * DY - Y * DX)) / (H * H)
#     IDD = NINT(DD)
#     DH = (X * DX + Y * DY) / H
#     IDH = NINT(DH)
#     DS = (60.0 * FACT * (H * DZ - Z * DH)) / (F * F)
#     IDS = NINT(DS)
#     DF = (H * DH + Z * DZ) / F
#     IDF = NINT(DF)
#     #
#     153 CONTINUE
#     if (ifL == 0) WRITE(IU, 959) XLT, XLN, D, S, IH, IX, IY, IZ, NF
#     if (ifL == 1) WRITE(IU, 960) XLT, XLN, IDD, IDS, IDH, IDX, IDY, IDZ, IDF
#     if (ifL == 2) :
#         WRITE(IU, 959) XLT, XLN, D, S, IH, IX, IY, IZ, NF
#         WRITE(IU, 961) IDD, IDS, IDH, IDX, IDY, IDZ, IDF
#
#     959 FORMAT (2F9.3, 2F8.2, 5I8)
#     960 FORMAT (2F9.3, 7I8)
#     961 FORMAT (14X, 'SV: ', 7I8)
#     #
#     154 LN = LN + LND
#     if (LND < 0) goto .a 156
#     if (LN <= LNF) goto .a 152
#     155 LT = LT + LTD
#     if (LTD < 0) goto .a 157
#     if (LT - LTF) 151, 151, 158
#     156 if (LN - LNF) 155, 152, 152
#     157 if (LT >= LTF) goto .a 151
#     158 CONTINUE
#     if (ifL == 0  or ifL == 2) :
#         WRITE(IU, 962)
#         962  FORMAT (/' D is declination in degrees (+ve east)'/ \
#                 ' I is inclination in degrees (+ve down)'/ \
#                 ' H is horizontal intensity in nT'/ \
#                 ' X is north component in nT'/ \
#                 ' Y is east component in nT'/ \
#                 ' Z is vertical component in nT (+ve down)'/ \
#                 ' F is total intensity in nT')
#         if (ifL != 0) WRITE(IU, 963)
#         963  FORMAT (' SV is secular variation (annual rate of change)'/ \
#                 ' Units for SV: minutes/yr (D  \ I); nT/yr (H,X,Y,Z  \ F)')
#         if (ITYPE == 2) WRITE(IU, *) \
#                 'These elements are relative to the geocentric coordinate system'
#     else:
#         WRITE(IU, 964)
#         964  FORMAT (/' D is SV in declination in minutes/yr (+ve east)'/ \
#                 ' I is SV in inclination in minutes/yr (+ve down)'/ \
#                 ' H is SV in horizontal intensity in nT/yr'/ \
#                 ' X is SV in north component in nT/yr'/ \
#                 ' Y is SV in east component in nT/yr'/ \
#                 ' Z is SV in vertical component in nT/yr (+ve down)'/ \
#                 ' F is SV in total intensity in nT/yr')
#         if (ITYPE == 2) WRITE(IU, *) \
#                 'These elements are relative to the geocentric coordinate system'
#
#     159 STOP
#     #
#     209 WRITE(6, 972) DATE
#     972 FORMAT (' ***** Error *****'/' DATE =', F9.3,  \
#             ' - out of range')
#     STOP
#     #
#     210 WRITE(6, 973) ALT, ITYPE
#     973 FORMAT (' ***** Error *****'/' A value of ALT =', F10.3,  \
#             ' is not allowed when ITYPE =', I2)
#     STOP
#     #
#     202 WRITE(6, 966) XLT
#     966 FORMAT (' ***** Error *****'/' XLT =', F9.3,  \
#             ' - out of range')
#     STOP
#     #
#     203 WRITE(6, 967) XLN
#     967 FORMAT (' ***** Error *****'/' XLN =', F10.3,  \
#             ' - out of range')
#     STOP
#     #
#     204 WRITE(6, 968) LTD, LTM
#     968 FORMAT (' ***** Error *****'/' Latitude out of range',  \
#             ' - LTD =', I6, 5X, 'LTM =', I4)
#     STOP
#     #
#     205 WRITE(6, 969) LND, LNM
#     969 FORMAT (' ***** Error *****'/' Longitude out of range',  \
#             ' - LND =', I8, 5X, 'LNM =', I4)
#     STOP
#     #
#     206 WRITE(6, 970) LTI, LTF
#     970 FORMAT (' ***** Error *****'/ \
#             ' Latitude limits of table out of range - LTI =',  \
#             I6, 5X, ' LTF =', I6)
#     STOP
#     #
#     207 WRITE(6, 971) LNI, LNF
#     971 FORMAT (' ***** Error *****'/ \
#             ' Longitude limits of table out of range - LNI =',  \
#             I8, 5X, ' LNF =', I8)
#     STOP


def DMDDEC (I, M):
    DE = I
    EM = M
    if I < 0:
        EM = -EM
    X = DE + EM / 60.0
    return X


def DDECDM (X):
    # IMPLICIT DOUBLE PRECISION (A-H, O-Z)
    SIG = np.sign(X)*1.1
    DR = abs(X)
    I = int(DR)
    T = I
    M = round(60. * (DR - T))
    if M == 60:
        M = 0
        I = I + 1
    ISIG = int(SIG)
    if I != 0:
        I = I * ISIG
    else:
        if M != 0:
            M = M * ISIG
    return I, M


def igrf12syn(isv, date, itype, alt, colat, elong):
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
    gh = loadCoeffs('igrf12coeffs.txt')

    # set initial values
    x, y, z = 0., 0., 0.

    # pointer for different years
    if date < 1900.0 or date > 2025.0:
        # error return if date out of bounds
        f = 1.0
        print('This subroutine will not work with a date of ' + str(date))
        print('Date must be in the range 1900.0 <= date <= 20205.0')
        print('On return f = 1.0, x = y = z = 0')
        return x, y, z, f
    elif date >= 2015.0:
        # future calculate for the model
        if date > 2020.0:
            # not adapt for the model but can calculate
            print('This version of the IGRF is intended for use up to 2020.0.')
            print('values for ' + str(date) + ' will be computed but may be of reduced accuracy')
        t = date - 2015.0
        tc = 1.0
        if isv == 1:
            t = 1.0
            tc = 0.0

        #  pointer for last coefficient in pen-ultimate set of MF coefficients...
        ll = 3060
        nmx = 13
        nc = nmx * (nmx + 2)
        kmx = (nmx + 1) * (nmx + 2) / 2
    else:
        t = 0.2 * (date - 1900.0)
        ll = t
        one = ll
        t = t - one
        # SH models before 1995.0 are only to degree 10
        if date < 1995.0:
            nmx = 10
            nc = nmx * (nmx + 2)
            ll = nc * ll
            kmx = (nmx + 1) * (nmx + 2) / 2
        else:
            nmx = 13
            nc = nmx * (nmx + 2)
            ll = 0.2 * (date - 1995.0)
            # 19 is the number of SH models that extend to degree 10
            ll = 120 * 19 + nc * ll
            kmx = (nmx + 1) * (nmx + 2) / 2

        tc = 1.0 - t
        if isv == 1:
            tc = -0.2
            t = 0.2

    # reset alt lat lon
    r = alt
    one = colat/FACT
    ct = np.cos(one)
    st = np.sin(one)
    one = elong/FACT
    cl[0] = np.cos(one)
    sl[0] = np.sin(one)
    cd = 1.0
    sd = 0.0
    l = 1
    m = 1
    n = 0
    if itype == 1:
        # conversion from geodetic to geocentric coordinates
        # (using the WGS84 spheroid)
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
    ratio = 6371.2 / r
    rr = ratio * ratio

    # computation of Schmidt quasi-normal coefficients p and x(=q)
    p[0] = 1.0
    p[2] = st
    q[0] = 0.0
    q[2] = ct

    for k in range(2, int(kmx)):
        if n >= m:
            fm = m
            if m != n:
                gmm = m * m
                one = np.sqrt(fn * fn - gmm)
                two = np.sqrt(gn * gn - gmm) / one
                three = (fn + gn) / one
                i = k - n
                j = i - n + 1
                p[k - 1] = three * ct * p[i - 1] - two * p[j - 1]
                q[k - 1] = three * (ct * q[i - 1] - st * p[i - 1]) - two * q[j - 1]
            else:
                if k != 3:
                    one = np.sqrt(1.0 - 0.5 / fm)
                    j = k - n - 1
                    p[k - 1] = one * st * p[j - 1]
                    q[k - 1] = one * (st * q[j - 1] + ct * p[j - 1])
                    cl[m - 1] = cl[m - 2] * cl[0] - sl[m - 2] * sl[0]
                    sl[m - 1] = sl[m - 2] * cl[0] + cl[m - 2] * sl[0]
            lm = ll + l
            one = (tc * gh[int(lm) - 1] + t * gh[int(lm + nc) - 1]) * rr
            if m == 0:
                x = x + one * q[k - 1]
                z = z - (fn + 1.0) * one * p[k - 1]
                l = l + 1
                m = m + 1
            two = (tc * gh[int(lm)] + t * gh[int(lm + nc)]) * rr
            three = one * cl[m - 1] + two * sl[m - 1]
            x = x + three * q[k - 1]
            z = z - (fn + 1.0) * three * p[k - 1]
            if st == 0.0:
                y = y + (one * sl[m - 1] - two * cl[m - 1]) * q[k - 1] * ct
            else:
                y = y + (one * sl[m - 1] - two * cl[m - 1]) * fm * p[k - 1] / st
            l = l + 2
            m = m + 1
        else:
            m = 0
            n = n + 1
            rr = rr * ratio
            fn = n
            gn = n - 1
            m = m + 1
    # conversion to coordinate system specified by itype
    one = x
    x = x * cd + z * sd
    z = z * cd - one * sd
    f = np.sqrt(x * x + y * y + z * z)

    return x, y, z, f


def loadCoeffs(filename):
    gh = []
    gh2arr = []
    with open(filename) as f:
        text = f.readlines()
        for a in text:
            if a[:2] == 'g ' or a[:2] == 'h ':
                b = a.split()[3:]
                b = [float(x) for x in b]
                gh2arr.append(b)
        gh2arr = np.array(gh2arr).transpose()
        N = len(gh2arr)
        for i in range(N):
            if i < 19:
                for j in range(120):
                    gh.append(gh2arr[i][j])
            else:
                for p in gh2arr[i]:
                    gh.append(p)
        gh.append(0)
        print(len(gh))
        return gh

if __name__ == '__main__':
    DATE = 2005
    ITYPE = 1
    ALT = 300
    CLT = 40
    XLN = 116
    print(igrf12syn(1, DATE, ITYPE, ALT, CLT, XLN))
