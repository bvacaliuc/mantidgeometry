#!/usr/bin/env python

from helper import INCH_TO_METRE, DEG_TO_RAD, MantidGeom
from rectangle import Rectangle, Vector, getEuler, makeLocation
from lxml import etree as le # python-lxml on rpm based systems
from math import cos, sin, radians, pi
import numpy as np
from sns_ncolumn import readFile

# 2nd option Gen-2R (462 x 32, 770mm x 380mm)
x_extent = 462*.00167
y_extent = 32*.01188

# number of pixels in each direction
x_num2 = 462
y_num2 = 32

# primary flight path - negative b/c it is upstream
L1 = -60.0

def readPositionsRight(filename):
    positions = readFile(filename)
    del positions['Position']
    del positions['DetectorNum']

    x = np.array(list(map(float, positions['X'])))
    y = np.array(list(map(float, positions['Elevation'])))
    z = np.array(list(map(float, positions['Z']))) - 60.
    positions['bank'] = np.array(list(map(int, positions['bank'])))

    positions['position'] = []
    for x_i,y_i,z_i in zip(x,y,z):
        positions['position'].append(Vector(x_i, y_i, z_i))

    del positions['X']
    del positions['Elevation']
    del positions['Z']

    columnnames = {'SA':1, 'SB':2, 'SC':3, 'SD':4, 'SE':5, 'SF':6,
                   'SG':7, 'SH':8, 'SI':9, 'SJ':10, 'SK':11, 'SL':12}

    banks = {}
    for i, (column, row, bank, position) in enumerate(zip(positions['column'], positions['row'], positions['bank'], positions['position'])):
        i = i%4
        if i == 0:
            one = position
        elif i == 1:
            two = position
        elif i == 2:
            three = position
        elif i == 3:
            four = position
        else:
            raise ValueError("Inconceivable! i = %d" % i)

        if i == 3:
            column = 'Column%d' % columnnames[column]
            banks[int(bank)] = (column, Rectangle(four, one, two, three, tolerance_len=0.002))

    return banks

def readPositionsLeft(filename):
    positions = readFile(filename)
    x = np.array(list(map(float, positions['X'])))
    y = np.array(list(map(float, positions['Elevation'])))
    z = np.array(list(map(float, positions['Z'])))
    positions['position'] = []
    for x_i,y_i,z_i in zip(x,y,z):
        positions['position'].append(Vector(x_i, y_i, z_i))

    del positions['X']
    del positions['Elevation']
    del positions['Z']

    names = {'D596':79,
             'D579':76,
             'D261':73,
             'DNI3':71,
             'D585':70,
             'D586':67,
             'DNG3':65,
             'D573':64,
             'D571':61,
             'D574':58,
             'D225':55,
             'D565':52,
             'D551':48,
             'DNA3':44,
             'D594':43}
    columnnames = {43:13, 44:13, 48:14, 52:15, 55:16, 58:17, 61:18, 64:19, 65:19, 67:20, 70:21, 71:21, 73:22, 76:23, 79:24}
    banks = {}
    for i, (det, position) in enumerate(zip(positions['Detector'], positions['position'])):
        bank = names[det[:4]]
        i = i%4
        if i == 0:
            three = position
        elif i == 1:
            four = position
        elif i == 2:
            one = position
        elif i == 3:
            two = position
        else:
            raise ValueError("Inconceivable! i = %d" % i)

        if i == 3:
            column = 'Column%d' % columnnames[bank]
            banks[bank] = (column, Rectangle(four, one, two, three, tolerance_len=0.002))

    return banks

if __name__ == "__main__":
    inst_name = "NOWD"
    xml_outfile = inst_name+"_Definition.xml"
    authors = ["Peter Peterson",
               "Stuart Campbell",
               "Vickie Lynch",
               "Janik Zikovsky"]

    # boiler plate stuff
    instr = MantidGeom(inst_name,
                       comment="Created by " + ", ".join(authors),
                       valid_from="2025-05-20 00:00:01")
    instr.addComment("DEFAULTS")
    instr.addSnsDefaults()
    instr.addComment("SOURCE")
    instr.addModerator(L1)
    instr.addComment("SAMPLE")
    instr.addSamplePosition()

    # monitors
    instr.addComment("MONITORS")
    instr.addMonitors(distance=[-1.5077], names=["monitor1"])
    #instr.addMonitors([L1+59., L1+62.5, L1+64], ["monitor1", "monitor2", "monitor3"])

    # choppers - copied verbatium from TS-geometry
    """
    chopper1 = Component("chopper1", "NXchopper")
    chopper1.setComment("CHOPPERS")
    chopper1.setHelper("ParameterCopy")
    chopper1.addParameter("distance", "6.647418", units="metre")
    instrument.addComponent(chopper1)
    chopper2 = Component("chopper2", "NXchopper")
    chopper2.setHelper("ParameterCopy")
    chopper2.addParameter("distance", "7.899603", units="metre")
    instrument.addComponent(chopper2)
    chopper3 = Component("chopper3", "NXchopper")
    chopper3.setHelper("ParameterCopy")
    chopper3.addParameter("distance", "49.975666", units="metre")
    instrument.addComponent(chopper3)
    """

    # apertures - copied verbatium from TS-geometry
    """
    aperture1=Component("aperture1", "NXaperture")
    aperture1.setComment(" APERTURES ")
    aperture1.setHelper("CenteredRectangle")
    aperture1.addVariable("cenDistance", "slit1Sam")
    aperture1.addVariable("xExtent", "s1width")
    aperture1.addVariable("yExtent", "s1height")
    instrument.addComponent(aperture1)
    """

    # guides - not even copying the text

    # read in detectors
    banks = readPositionsRight("SNS/POWGEN/NOWD_geom_2025A.csv")
    banksL = readPositionsLeft("SNS/POWGEN/NOWD_geom_left_2025A.csv")
    for bank in banksL.keys():
        banks[bank] = banksL[bank]
    del banksL

    # delete the banks that are no longer installed
    # South Banks
    for bank in [1,5,6,10,28,31,32,34,35,37,38,40]:
        try:
            del banks[bank]
        except KeyError:
            pass
    # North Banks (Gen2 are 44,65,71)
    for bank in [41,42,45,46,47,49,50,51,53,54,56,57,59]:
        try:
            del banks[bank]
        except KeyError:
            pass
    for bank in [60,62,63,66,68,69,72,74,75,77,78,80]:
        try:
            del banks[bank]
        except KeyError:
            pass

    # create north and south sides
    sides = {'North':['Column%d' % i for i in range(13,25)],
             'South':['Column%d' % i for i in range(1,13)]}
    # add the empty components
    for name in sides.keys():
        group = instr.addComponent(name)
    # add the columns to the groups
    for side in sides.keys():
        group = instr.makeTypeElement(side)

        for column in sides[side]:
            instr.addComponent(column, root=group)

    # create an ordered list of all columns
    columns = set()
    for name in banks.keys():
        column, _ =  banks[name]
        columns.add(column)
    columns = list(columns)
    columns.sort()

    createdcolumns = dict()
    for name in banks.keys():
        offset = (int(name)-1) * 15000
        column, rect =  banks[name]
        name = 'bank'+str(name)

        # create the column if it doesn't already exist
        if column in createdcolumns:
            col = createdcolumns[column]
        else:
            col = instr.makeTypeElement(str(column))
            createdcolumns[column] = col

        extra_attrs={"idstart":offset, 'idfillbyfirst':'y', 'idstepbyrow':y_num2}
        det = instr.makeDetectorElement('panel_g2', root=col, extra_attrs=extra_attrs)
        rect.makeLocation(instr, det, name)

    # add the panel shape
    instr.addComment(f" Gen2 Detector Panel ({y_num2}x{x_num2})")
    x_delta2 = x_extent/float(x_num2)
    x_offset2 = x_delta2*(1.-float(x_num2))/2.
    y_delta2 = y_extent/float(y_num2)
    y_offset2 = y_delta2*(1.-float(y_num2))/2.
    det = instr.makeTypeElement("panel_g2",
                                extra_attrs={"is":"rectangular_detector", "type":"pixel_g2",
                                             "xpixels":x_num2, "xstart":x_offset2, "xstep":x_delta2,
                                             "ypixels":y_num2, "ystart":y_offset2, "ystep":y_delta2
                                             })
    le.SubElement(det, "properties")

    # shape for monitors
    instr.addComment(" Shape for Monitors")
    instr.addComment(" TODO: Update to real shape ")
    instr.addDummyMonitor(0.01, .03)

    # shape for detector pixels
    instr.addComment(f" Pixel for Gen2 Detectors ({y_num2}x{x_num2})")
    instr.addCuboidPixel("pixel_g2",
                         [-.5*x_delta2, -.5*y_delta2,  0.0],
                         [-.5*x_delta2,  .5*y_delta2,  0.0],
                         [-.5*x_delta2, -.5*y_delta2, -0.0001],
                         [ .5*x_delta2, -.5*y_delta2,  0.0],
                         shape_id="pixel-shape")

    # monitor ids
    instr.addComment("MONITOR IDs")
    instr.addMonitorIds([-1]) # TODO [-1,-2,-3]

    # write out the file
    instr.writeGeom(xml_outfile)
    #instr.showGeom()
