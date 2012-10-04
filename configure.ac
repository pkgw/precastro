dnl Copyright 2012 Peter Williams
dnl Licensed under the GNU General Public License version 3 or higher. 

AC_INIT([palp], [0.0])
AC_CONFIG_SRCDIR([sofa/src/c2ixy.c])
AC_CONFIG_AUX_DIR([build-aux])
AC_CONFIG_MACRO_DIR([build-aux])
AM_INIT_AUTOMAKE([foreign silent-rules -Wall])
LT_INIT([disable-static])

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

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_FILES([Makefile])
AC_OUTPUT
