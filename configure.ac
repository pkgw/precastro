dnl Copyright 2012 Peter Williams
dnl Licensed under the GNU General Public License version 3 or higher. 

AC_INIT([palp], [0.0])
AC_CONFIG_SRCDIR([sofa/src/c2ixy.c])
AC_CONFIG_AUX_DIR([build-aux])
AC_CONFIG_MACRO_DIR([build-aux])
AM_INIT_AUTOMAKE([foreign silent-rules -Wall])
LT_INIT([disable-static])

AC_SUBST([PALP_SHORTVERSION],[0.0]) dnl used in Sphinx docs
AC_SUBST([PALP_COPYRIGHT],["2012 Peter Williams"])

AC_LANG([C])

AX_CHECK_COMPILE_FLAG([-fno-strict-aliasing],[ dnl for Python
  AM_CFLAGS="$AM_CFLAGS -fno-strict-aliasing"
])

AX_CHECK_COMPILE_FLAG([-fvisibility=hidden],[
  AM_CFLAGS="$AM_CFLAGS -fvisibility=hidden"
])

AX_CHECK_COMPILE_FLAG([-Wall],[
  AM_CFLAGS="$AM_CFLAGS -Wall"
])

AX_CHECK_COMPILE_FLAG([-Wstrict-prototypes],[
  AM_CFLAGS="$AM_CFLAGS -Wstrict-prototypes"
])

AC_SUBST([AM_CFLAGS])

AM_PATH_PYTHON(2.4)
AM_CHECK_PYTHON_HEADERS(,AC_MSG_ERROR([could not find Python headers]))

AM_PROG_AR dnl for "linking libtool libraries with a non-POSIX archiver"

AC_PATH_PROG(SWIG, swig, :)
if test x"$SWIG" = x: ; then
   AC_MSG_ERROR([the program 'swig' was not found])
fi
AC_SUBST(SWIG)

AC_PATH_PROG(WGET, wget, :)
if test x"$WGET" = x: ; then
   AC_MSG_ERROR([the program 'wget' was not found (needed for downloading JPL ephemeris data)])
fi
AC_SUBST(WGET)

AC_PATH_PROG(SPHINXBUILD, sphinx-build, :)
if test x"$SPHINXBUILD" = x: ; then
   AC_MSG_WARN([The program 'sphinx-build' wasn't found on your system! Documentation won't be built.])
   build_docs=false
   docs_desc="no; no 'sphinx-build' found"
else
   build_docs=true
   docs_desc="yes"
fi

AM_CONDITIONAL([BUILD_DOCS], $build_docs)

if $build_docs ; then
   AC_CONFIG_FILES([doc/conf.py])
fi

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_FILES([Makefile])
AC_OUTPUT

echo "Configuration summary:"
echo "                   Install prefix: " $prefix
echo "                    Building docs? " $docs_desc
