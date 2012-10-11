# Copyright 2012 Peter Williams
# Licensed under the GNU General Public License, version 3 or higher.

"""precastro - precision astronomy time and coordinate routines

"""

import _precastro
from astutil import *

__all__ = ('PrecAstroError NovasError SofaError UnsupportedTimescaleError '
           'Time now Object').split ()

_oktimescales = frozenset ('TAI UTC UT1 TT TCG TCB TDB'.split ())


class PrecAstroError (Exception):
    def __init__ (self, fmt, *args):
        if len (args):
            self.pamessage = fmt % args
        else:
            self.pamessage = str (fmt)

    def __str__ (self):
        return self.pamessage


class NovasError (PrecAstroError):
    def __init__ (self, func, code):
        self.func = func
        self.code = code

    def __str__ (self):
        return 'NOVAS error code #%d in function %s' % (self.code, self.func)


class SofaError (PrecAstroError):
    def __init__ (self, func, code):
        self.func = func
        self.code = code

    def __str__ (self):
        return 'SOFA error code #%d in function %s' % (self.code, self.func)


class UnsupportedTimescaleError (PrecAstroError):
    def __init__ (self, timescale):
        self.timescale = timescale

    def __str__ (self):
        return 'operation not supported with timescale ' + self.timescale


def _checktimescale (timescale):
    if timescale not in _oktimescales:
        raise ValueError ('illegal timescale name "%s"' % timescale)


def _checksofacode (func, code, dubiousok):
    if code == 1 and not dubiousok:
        raise SofaError (func, code)
    elif code:
        raise SofaError (func, code)


class Time (object):
    """A precisely-measured time and its associated timescale.

Times are stored in the IAU SOFA format: as two double-precision
floating point numbers specifying a Julian Date. Each time is also
associated with a named timescale, for which 'UTC' and 'TT' are
currently well-supported.

UTC does not have well-defined behavior regarding leapseconds. SOFA's
implementation is such that UTC times on days with leapseconds will
progress at a different rate than on other days. Any kind of precise
measurement, and any math with :class:`Time` objects, should avoid UTC
at all costs. The only way to safely interchange UTC times is in
broken-down calendar format, so that leapseconds can be expressed as
(e.g.) HH:MM:60.375.
"""

    jd1 = None
    """The first Julian Date component."""

    jd2 = None
    """The second Julian Date component."""

    timescale = None
    """The timescale in which this time is measured. 'UTC' and 'TT'
    are somewhat implemented; additional support for TAI, UT1, TCG,
    TCB, and TDB is possible but not yet exposed in the Python."""

    def fromNow (self):
        """Set the object to represent the current time according
to the computer clock. The associated timescale is UTC.

:returns: *self*

There (bizarrely) seems to be no way to get the current time that
avoids the leapsecond ambiguity inherent in the POSIX time system,
so this value has ~1-second precision on leapsecond days. Things
should be better on non-leapsecond days, though of course the
accuracy of the system clock is a limitation.

As of summer 2012 there was apparently interest in the Linux community
in adding a CLOCK_TAI clockid_t for ``clock_gettime`` that would make
this all so much easier. It is possible that using the tzdata
"right/UTC" timezone would get things right, but that just seems
impossible to test, and not worth doing unless I can be sure that it's
actually right. Another source references ``ntp_adjtime(3)`` as a
possibility for querying the leapsecond subsystem to get this right.
"""
        from time import time
        self.fromPOSIX (time ())
        return self


    def fromPOSIX (self, time):
        """Set the object to represent the given POSIX time. The
associated timescale is UTC.

:arg time: a POSIX/Unix time
:type time: convertable to :class:`float`
:returns: *self*

It really seems as if we just can't do anything about the leapsecond
ambiguity: the "TAI minus 10" standard is appealing but apparently not
honored. We only really need this function to implement fromNow(), so
if I ever find a way to get the current time in a way that's
leapsecond-safe, then this becomes a lot less pressing.

Note while both UTC and POSIX time are problematic regarding
leapseconds, they are problematic in different and non-canceling ways.
"""
        self.jd1 = 2440587.5
        self.jd2 = float (time / 86400.)
        self.timescale = 'UTC'
        return self


    def fromJD (self, jd, timescale):
        """Set the object to represent the given Julian Date and
timescale.

:arg jd: a Julian date
:type jd: convertable to :class:`float`
:arg timescale: the timescale being used (see :class:`Time` docs)
:type timescale: :class:`str`
:returns: *self*

Storing a JD as a single float limits precision to about 20.1
microseconds, according to Kaplan, Bartlett, & Harris (2011, USNO-AA
Tech Note 2011-02).
"""
        _checktimescale (timescale)
        self.jd1 = float (jd)
        self.jd2 = 0.0
        self.timescale = timescale
        return self


    def fromMJD (self, mjd, timescale):
        """Set the object to represent the given modified Julian Date and
timescale.

:arg mjd: a modified Julian date
:type mjd: convertable to :class:`float`
:arg timescale: the timescale being used (see :class:`Time` docs)
:type timescale: :class:`str`
:returns: *self*

JD = MJD + 2400000.5. This will offer some precision gains over a
double-precision representation of an full, un-modified Julian Date, but
they're probably not too large. Maybe mentioned in Kaplan et al (2011)?
"""
        _checktimescale (timescale)
        self.jd1 = 2400000.5
        self.jd2 = mjd
        self.timescale = timescale
        return self


    def fromCalendar (self, year, month, day, hour, minute, second, timescale,
                      dubiousok=False):
        """Set the object to represent the given Gregorian calendar
date in the given timescale.

:arg year: the year
:type year: convertable to :class:`int`
:arg month: the month
:type month: convertable to :class:`int`, range 1 to 12
:arg day: the day
:type day: convertable to :class:`int`, range 1 to 31
:arg hour: the hour
:type hour: convertable to :class:`int`, range 0 to 23
:arg minute: the minute
:type minute: convertable to :class:`int`, range 0 to 59
:arg second: the second
:type second: convertable to :class:`float`, range 0 to 60.99999...
:arg timescale: the timescale being used (see :class:`Time` docs)
:type timescale: :class:`str`
:arg dubiousok: whether to accept extreme years
:type dubiousok: :class:`bool`
:returns: *self*
:raises: :exc:`SofaError` for bad inputs

Uses the Gregorian calendar system, which has the 100- and 400-year
leap day rules. SOFA docs say that the algorithm is valid to -4799
January 1 and uses the "proleptic Gregorian calendar" without paying
attention to, say, when the Gregorian calendar was actually adopted.

This is currently the only way to set a UTC date that can properly
account for leapseconds. But I know of no way to get the current
computer time in this broken-down format without going through POSIX
time, so that's not actually helpful.
"""
        _checktimescale (timescale)
        code, self.jd1, self.jd2 = _precastro.iauDtf2d (timescale, year, month, day,
                                                        hour, minute, second)
        _checksofacode ('dtf2d', code, dubiousok)
        self.timescale = timescale
        return self


    def asJD (self):
        """Return the time as a Julian Date.

:returns: the time as a Julian Date
:rtype: :class:`float`

The one-value representation limits precision to about 20
microseconds.
"""
        return self.jd1 + self.jd2


    def asMJD (self):
        """Return the time as a modified Julian Date.

:returns: the time as a modified Julian Date
:rtype: :class:`float`

The precision may be somewhat superior to that given by :meth:`asJD`,
but the difference will probably be minor.
"""
        return (self.jd1 - 2400000.5) + self.jd2


    def asTT (self, dubiousok=False):
        """Return a :class:`Time` object equivalent to this one, but
in the TT timescale.

:arg dubiousok: whether to accept extreme dates
:type dubiousok: :class:`bool`
:returns: an equivalent time in the TT timescale
:rtype: :class:`Time`
:raises: :exc:`SofaError` if extrapolating to an unacceptably extreme date
:raises: :exc:`UnsupportedTimescaleError` if there's no implementation
  to convert *self* to TT.

If the timescale of *self* is a TT, a copy is returned. Right now the
only other supported timescales are TAI and UTC. Other conversions can
be implemented as the need arises.
"""
        res = Time ()
        res.timescale = 'TT'

        if self.timescale == 'TT':
            res.jd1, res.jd2 = self.jd1, self.jd2
        elif self.timescale == 'TAI':
            code, res.jd1, res.jd2 = _precastro.iauTaitt (self.jd1, self.jd2)
            _checksofacode ('taitt', code, dubiousok)
        elif self.timescale == 'UTC':
            code, res.jd1, res.jd2 = _precastro.iauUtctai (self.jd1, self.jd2)
            _checksofacode ('utctai', code, dubiousok)
            code, res.jd1, res.jd2 = _precastro.iauTaitt (res.jd1, res.jd2)
            _checksofacode ('taitt', code, dubiousok)
        else:
            raise UnsupportedTimescaleError (self.timescale)

        return res


    def fmtCalendar (self, precision=0, dubiousok=False):
        """Format the time as a calendar date/time.

:arg precision: how many decimal places of precision in the second
  component to use (default: 0, range: > -4)
:type precision: :class:`int`
:arg dubiousok: whether to accept extreme dates
:type dubiousok: :class:`bool`
:returns: the time formatted as a calendar date/time
:rtype: :class:`str`
:raises: :exc:`SofaError` if using an unacceptably extreme date

The returned string takes the form 'YYYY/MM/DD HH:MM:SS.SSSS', where
the number of decimal places used for the seconds varies. If *precision*
is less than one, the decimal point and fractional parts are omitted.
If precision is less than zero, the reported values are rounded as
appropriate but trailing zeros are still present in the string.
"""
        info = _precastro.iauD2dtf_tweak (self.timescale, precision, self.jd1, self.jd2)
        _checksofacode ('d2dtf', info[0], dubiousok)
        ymdhmsf = list (info[1:])

        if precision < 1:
            ymdhmsf[6] = ''
        else:
            ymdhmsf[6] = '.%0*d' % (precision, ymdhmsf[6])

        return '%d/%02d/%02d %02d:%02d:%02d%s' % tuple (ymdhmsf)


def now ():
    """Get the current time.

:returns: the current time from the system clock
:rtype: :class:`Time`

Shorthand for ``Time().fromNow()``.
"""
    return Time ().fromNow ()


class Object (object):
    """A celestial object
"""

    def __init__ (self, ra=None, dec=None):
        self._handle = _precastro.novas_cat_entry ()

        if ra is not None:
            if isinstance (ra, basestring):
                self.ra = parsehours (ra)
            else:
                self.ra = ra

        if dec is not None:
            if isinstance (dec, basestring):
                self.dec = parsedeglat (dec)
            else:
                self.dec = dec

        self.promoepoch = 2451545.0 # J2000 epoch; unpatched NOVAS's assumption


    def _get_ra (self):
        return self._handle.ra * H2R

    def _set_ra (self, rarad):
        self._handle.ra = rarad * R2H

    ra = property (_get_ra, _set_ra, doc='object\'s ICRS right ascension in radians')

    def _get_dec (self):
        return self._handle.dec * D2R

    def _set_dec (self, decrad):
        self._handle.dec = decrad * R2D

    dec = property (_get_dec, _set_dec, doc='object\'s ICRS declination in radians')

    def setradec (self, rarad, decrad):
        self.ra = rarad
        self.dec = decrad
        return self

    def fmtradec (self, **kwargs):
        return fmtradec (self.ra, self.dec, **kwargs)


    def _get_promora (self):
        return self._handle.promora

    def _set_promora (self, promora_masperyr):
        self._handle.promora = promora_masperyr

    promora = property (_get_promora, _set_promora,
                        doc='object\'s ICRS RA proper motion in mas per year')

    def _get_promodec (self):
        return self._handle.promodec

    def _set_promodec (self, promodec_masperyr):
        self._handle.promodec = promodec_masperyr

    promodec = property (_get_promodec, _set_promodec,
                        doc='object\'s ICRS declination proper motion in mas per year')

    def setpromo (self, promora_masperyr, promodec_masperyr):
        self.promora = promora_masperyr
        self.promodec = promodec_masperyr
        return self


    def _get_parallax (self):
        return self._handle.parallax

    def _set_parallax (self, parallax_mas):
        self._handle.parallax = parallax_mas

    parallax = property (_get_parallax, _set_parallax,
                         doc='object\'s parallax in milliarcseconds')


    def _get_vradial (self):
        return self._handle.radialvelocity

    def _set_vradial (self, vradial_kmpers):
        self._handle.radialvelocity = vradial_kmpers

    vradial = property (_get_vradial, _set_vradial,
                        doc='object\'s radial velocity in km per second')


    def _get_promoepoch (self):
        return self._handle.promoepoch

    def _set_promoepoch (self, promoepoch_jdtdb):
        self._handle.promoepoch = promoepoch_jdtdb

    promoepoch = property (_get_promoepoch, _set_promoepoch,
                           doc='TDB JD for which effect of proper motion is zero')


    def setpecal (self, year, month, day, hour=0, minute=0, second=0,
                  timescale='UTC', **kwargs):
        """Set the proper-motion epoch to a calendar date.

:arg year: the year
:arg month: the month
:arg day: the day
:arg hour: the hour (defaults to 0)
:arg minute: the minute (defaults to 0)
:arg second: the second (defaults to 0)
:arg timescale: the timescale to use (defaults to 'UTC')
:arg kwargs: extra keywords to pass to :meth:`Time.fromCalendar`
:returns: *self*

Set the "proper-motion epoch" to the given date. Because the date does not
often need to be precise, *hour*, *minute*, and *second* default to zero
for convenience, and likewise *timescale* defaults to "UTC".

The epoch thus generated is converted to the TT timescale, while the
timescale used for proper-motion calculations by NOVAS is TDB. My
understanding is that the difference between these is almost always
insignificant. If this becomes a problem, we can add a flag to override
this behavior, or you can set :attr:`Object.promoepoch` manually.
"""
        self.promoepoch = Time ().fromCalendar (year, month, day, hour, minute,
                                                second, **kwargs).asTT ().asJD ()
        return self


    def fromSesame (self, ident):
        from urllib2 import urlopen
        from urllib import quote

        url = 'http://cdsweb.u-strasbg.fr/cgi-bin/nph-sesame?' + quote (ident)

        for line in urlopen (url):
            if line.startswith ('#!'):
                raise PrecAstroError ('Simbad/Sesame lookup failed: ' + line[3:].strip ())

            a = line.strip ().split ()
            if not len (a):
                continue

            # The units for our fields are coincidentally the same as
            # those used by Simbad, for the most part ...

            if a[0] == '%J':
                self.ra = float (a[1]) * D2R
                self.dec = float (a[2]) * D2R
            elif a[0] == '%P':
                self.promora = float (a[1])
                self.promodec = float (a[2])
            elif a[0] == '%X':
                self.parallax = float (a[1])
            elif a[0] == '%V':
                self.vradial = float (a[2])

        return self


    def describe (self):
        '''Return a human-friendly string describing the object's properties

:returns: a multiline string describing the object's properites
:rtype: :class:`str`
'''
        s = ['ICRS J2000: ' + self.fmtradec ()]
        s.append ('Proper motion: %+.2f %+.2f mas/yr' % (self.promora, self.promodec))
        s.append ('Parallax: %.2f mas' % self.parallax)
        s.append ('Radial velocity: %+.2f km/s' % self.vradial)
        s.append ('Proper-motion epoch: %s [TDB]' %
                  Time ().fromJD (self.promoepoch, 'TDB').fmtCalendar ())
        return '\n'.join (s)


    def astropos (self, jd_tt, lowaccuracy=False):
        if isinstance (jd_tt, Time):
            jd_tt = jd_tt.asTT ().asJD ()

        code, ra, dec = _precastro.astro_star (jd_tt, self._handle, int (lowaccuracy))
        if code:
            raise NovasError ('astro_star', code)

        return ra * H2R, dec * D2R
