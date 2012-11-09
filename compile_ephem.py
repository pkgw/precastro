#! /usr/bin/env python
#
# Copyright 2012 Peter Williams
# Licensed under the GNU General Public License, version 3 or higher.

"""
Compile an ASCII JPL ephemeris table to the binary format
used by NOVAS and JPL's FORTRAN code.

This is based off of asc2eph.f from JPL but was written essentially
from scratch.
"""

import sys, os, struct


def die (fmt, *args):
    print >>sys.stderr, 'error:', fmt % args
    sys.exit (1)


def compile (header, data, output):
    # Read in the header ...

    l = header.readline ()
    ksize = int (l[6:12])

    curgroup = 0
    titles = None
    spaninfo = None
    nconstnames = None
    constnames = None
    nconstvalues = None
    constvalues = None
    interpvals = None

    for l in header:
        a = l.strip ().split ()
        if not len (a):
            continue

        if l.startswith ('GROUP   '):
            curgroup = int (a[1])
            continue

        if curgroup == 1010:
            if titles is None:
                titles = []
            titles.append (l)
        elif curgroup == 1030:
            if spaninfo is not None:
                die ('expected exactly one data line in group 1030')
            if len (a) != 3:
                die ('expected exactly three items in group 1030')
            spaninfo = [float (x.replace ('D', 'e')) for x in a]
        elif curgroup == 1040:
            if nconstnames is None:
                if len (a) != 1:
                    die ('expected one int on first line of group 1040')
                nconstnames = int (a[0])
                constnames = []
            else:
                constnames += a
        elif curgroup == 1041:
            if nconstvalues is None:
                if len (a) != 1:
                    die ('expected one int on first line of group 1041')
                nconstvalues = int (a[0])
                constvalues = []
            else:
                constvalues += [float (x.replace ('D', 'e')) for x in a]
        elif curgroup == 1050:
            if interpvals is None:
                interpvals = []
            if len (a) != 13:
                die ('expect 13 entries in each line of group 1050')
            interpvals.append ([int (x) for x in a])
        else:
            die ('unexpected data in group %d', curgroup)

    # Verify header parameters

    if curgroup != 1070:
        die ('expected to finish header in group 1070')

    if titles is None or len (titles) != 3:
        die ('expected to find exactly 3 titles')

    for t in titles:
        if len (t) > 84:
            die ('each title must be less than 85 characters long')

    if spaninfo is None:
        die ('didn\'t find span info (group 1030)')

    if nconstnames is None:
        die ('didn\'t find constant name info (group 1040)')

    if len (constnames) != nconstnames:
        die ('claimed and actual number of constant names disagree')

    if nconstnames > 400:
        die ('too many constants')

    for c in constnames:
        if len (c) > 6:
            die ('each constant name must be less than 7 characters long')

    if nconstvalues is None:
        die ('didn\'t find constant value info (group 1041)')

    if len (constvalues) != nconstvalues:
        die ('claimed and actual number of constant values disagree')

    if nconstvalues != nconstnames:
        die ('number of constant names and values disagree')

    if interpvals is None:
        die ('didn\'t find interpolation value info (group 1050)')

    if len (interpvals) != 3:
        die ('expected to find exactly three lines of interpolation value info')

    try:
        au = constvalues[constnames.index ('AU')]
        emrat = constvalues[constnames.index ('EMRAT')]
        denum = constvalues[constnames.index ('DENUM')]
    except ValueError:
        die ('missing constant AU, EMRAT, or DENUM')

    # Write the header

    intsz = struct.calcsize ('=i')
    floatsz = struct.calcsize ('=f')
    dblsz = struct.calcsize ('=d')
    blocksz = ksize * floatsz
    n = 0

    output.write (titles[0].ljust (84))
    output.write (titles[1].ljust (84))
    output.write (titles[1].ljust (84))
    n += 84 * 3

    for i in xrange (nconstnames):
        output.write (constnames[i].ljust (6))
    output.write (' ' * (6 * (400 - nconstnames)))
    n += 400 * 6

    output.write (struct.pack ('=3d', *spaninfo))
    n += 3 * dblsz

    output.write (struct.pack ('=i', nconstnames))
    n += intsz

    output.write (struct.pack ('=dd', au, emrat))
    n += 2 * dblsz

    for i in xrange (12):
        output.write (struct.pack ('=3i', interpvals[0][i],
                                   interpvals[1][i], interpvals[2][i]))
    n += 3 * 12 * intsz

    output.write (struct.pack ('=i', denum))
    n += intsz

    output.write (struct.pack ('=3i', interpvals[0][12],
                               interpvals[1][12], interpvals[2][12]))
    n += 3 * intsz

    assert n <= blocksz
    output.write ('\0' * (blocksz - n))

    n = 0
    for i in xrange (nconstnames):
        output.write (struct.pack ('=d', constvalues[i]))
    output.write ('\0' * (dblsz * (400 - nconstnames)))
    n += 400 * dblsz
    assert n <= blocksz
    output.write ('\0' * (blocksz - n))

    # Read and write the main ephemeris data. Unlike the JPL version, we just
    # totally ignore the JD bounds.

    newrec = True

    for l in data:
        a = l.strip ().split ()
        if not len (a):
            continue

        if newrec:
            recnum = int (a[0])
            ncoeff = int (a[1])

            if 2 * ncoeff != ksize:
                die ('number of data coefficients doesn\'t match header: mismatched files?')

            block = []
            newrec = False
        else:
            block += [float (x.replace ('D', 'e')) for x in a]

            if len (block) >= ncoeff:
                newrec = True

                for i in xrange (ncoeff):
                    output.write (struct.pack ('=d', block[i]))


if __name__ == '__main__':
    compile (open (sys.argv[1]), open (sys.argv[2]), sys.stdout)
