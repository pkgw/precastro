"""precastro - precision astronomy time and coordinate routines

"""

import _precastro
from astutil import *

__all__ = ('PrecAstroError NovasError SofaError UnsupportedTimescaleError '
           'Time now Object').split ()

_oktimescales = frozenset ('TAI UTC UT1 TT TCG TCB TDB'.split ())


class PrecAstroError (Exception):
    pass

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
    jd1 = None
    jd2 = None
    timescale = None

    def fromNow (self):
        # There seems to be no way to get the current time
        # that avoids the leapsecond ambiguity ... ?!?
        from time import time
        self.fromPOSIX (time ())
        return self


    def fromPOSIX (self, time):
        # "TAI-10" standard is appealing but not honored, so there's a
        # leapsecond ambiguity and we just can't do anything about it.
        # Based on SOFA's convention for representing UTC as a JD, our
        # approach here will result in a constant slew across each day
        # that contains a leapsecond, while in theory we could get
        # full precision except during the leapseconds themselves,
        # when there'd be a +/- one-second ambiguity.
        self.jd1 = 2440587.5
        self.jd2 = time / 86400.
        self.timescale = 'UTC'
        return self


    def fromJD (self, jd, timescale):
        _checktimescale (timescale)
        self.jd1 = jd
        self.jd2 = 0.0
        self.timescale = timescale
        return self


    def fromMJD (self, mjd, timescale):
        _checktimescale (timescale)
        self.jd1 = 2400000.5
        self.jd2 = mjd
        self.timescale = timescale
        return self


    def fromCalendar (self, year, month, day, hour, minute, second, timescale,
                      dubiousok=False):
        _checktimescale (timescale)
        code, self.jd1, self.jd2 = _precastro.iauDtf2d (timescale, year, month, day,
                                                        hour, minute, second)
        _checksofacode ('dtf2d', code, dubiousok)
        self.timescale = timescale
        return self


    def asJD (self):
        return self.jd1 + self.jd2


    def asMJD (self):
        return (self.jd1 - 2400000.5) + self.jd2


    def asTT (self, dubiousok=False):
        res = Time ()
        res.timescale = 'TT'

        if self.timescale == 'TT':
            res.jd1, res.jd2 = self.jd1, self.jd2
        elif self.timescale == 'UTC':
            code, res.jd1, res.jd2 = _precastro.iauUtctai (self.jd1, self.jd2)
            _checksofacode ('utctai', code, dubiousok)
            code, res.jd1, res.jd2 = _precastro.iauTaitt (res.jd1, res.jd2)
            _checksofacode ('taitt', code, dubiousok)
        else:
            raise UnsupportedTimescaleError (self.timescale)

        return res


    def fmtCalendar (self, precision=0, dubiousok=False):
        info = _precastro.iauD2dtf_tweak (self.timescale, precision, self.jd1, self.jd2)
        _checksofacode ('d2dtf', info[0], dubiousok)
        ymdhmsf = list (info[1:])

        if precision < 1:
            ymdhmsf[6] = ''
        else:
            ymdhmsf[6] = '.%0*d' % (precision, ymdhmsf[6])

        return '%d/%02d/%02d %02d:%02d:%02d%s' % tuple (ymdhmsf)


def now ():
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


    def astropos (self, jd_tt, lowaccuracy=False):
        if isinstance (jd_tt, Time):
            jd_tt = jd_tt.asTT ().asJD ()

        code, ra, dec = _precastro.astro_star (jd_tt, self._handle, int (lowaccuracy))
        if code:
            raise NovasError ('astro_star', code)

        return ra * H2R, dec * D2R
