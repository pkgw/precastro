## Copyright 2012 Peter Williams
## Licensed under the GNU General Public License version 3 or higher. 

ACLOCAL_AMFLAGS = -I build-aux

python_PYTHON = precastro.py
pyexec_LTLIBRARIES = _precastro.la

_precastro_la_CPPFLAGS = -I$(srcdir)/novas -I$(srcdir)/sofa/src $(PYTHON_INCLUDES)
_precastro_la_LDFLAGS = -module -avoid-version
_precastro_la_SOURCES = \
 capi_wrap.c \
 novas/cio_file.c \
 novas/eph_manager.c \
 novas/eph_manager.h \
 novas/novas.c \
 novas/novas.h \
 novas/novascon.c \
 novas/novascon.h \
 novas/nutation.c \
 novas/nutation.h \
 novas/readeph0.c \
 novas/solarsystem.h \
 novas/solsys1.c \
 sofa/src/a2af.c \
 sofa/src/a2tf.c \
 sofa/src/af2a.c \
 sofa/src/anp.c \
 sofa/src/anpm.c \
 sofa/src/bi00.c \
 sofa/src/bp00.c \
 sofa/src/bp06.c \
 sofa/src/bpn2xy.c \
 sofa/src/c2i00a.c \
 sofa/src/c2i00b.c \
 sofa/src/c2i06a.c \
 sofa/src/c2ibpn.c \
 sofa/src/c2ixy.c \
 sofa/src/c2ixys.c \
 sofa/src/c2s.c \
 sofa/src/c2t00a.c \
 sofa/src/c2t00b.c \
 sofa/src/c2t06a.c \
 sofa/src/c2tcio.c \
 sofa/src/c2teqx.c \
 sofa/src/c2tpe.c \
 sofa/src/c2txy.c \
 sofa/src/cal2jd.c \
 sofa/src/cp.c \
 sofa/src/cpv.c \
 sofa/src/cr.c \
 sofa/src/d2dtf.c \
 sofa/src/d2tf.c \
 sofa/src/dat.c \
 sofa/src/dtdb.c \
 sofa/src/dtf2d.c \
 sofa/src/ee00.c \
 sofa/src/ee00a.c \
 sofa/src/ee00b.c \
 sofa/src/ee06a.c \
 sofa/src/eect00.c \
 sofa/src/eform.c \
 sofa/src/eo06a.c \
 sofa/src/eors.c \
 sofa/src/epb.c \
 sofa/src/epb2jd.c \
 sofa/src/epj.c \
 sofa/src/epj2jd.c \
 sofa/src/epv00.c \
 sofa/src/eqeq94.c \
 sofa/src/era00.c \
 sofa/src/fad03.c \
 sofa/src/fae03.c \
 sofa/src/faf03.c \
 sofa/src/faju03.c \
 sofa/src/fal03.c \
 sofa/src/falp03.c \
 sofa/src/fama03.c \
 sofa/src/fame03.c \
 sofa/src/fane03.c \
 sofa/src/faom03.c \
 sofa/src/fapa03.c \
 sofa/src/fasa03.c \
 sofa/src/faur03.c \
 sofa/src/fave03.c \
 sofa/src/fk52h.c \
 sofa/src/fk5hip.c \
 sofa/src/fk5hz.c \
 sofa/src/fw2m.c \
 sofa/src/fw2xy.c \
 sofa/src/gc2gd.c \
 sofa/src/gc2gde.c \
 sofa/src/gd2gc.c \
 sofa/src/gd2gce.c \
 sofa/src/gmst00.c \
 sofa/src/gmst06.c \
 sofa/src/gmst82.c \
 sofa/src/gst00a.c \
 sofa/src/gst00b.c \
 sofa/src/gst06.c \
 sofa/src/gst06a.c \
 sofa/src/gst94.c \
 sofa/src/h2fk5.c \
 sofa/src/hfk5z.c \
 sofa/src/ir.c \
 sofa/src/jd2cal.c \
 sofa/src/jdcalf.c \
 sofa/src/num00a.c \
 sofa/src/num00b.c \
 sofa/src/num06a.c \
 sofa/src/numat.c \
 sofa/src/nut00a.c \
 sofa/src/nut00b.c \
 sofa/src/nut06a.c \
 sofa/src/nut80.c \
 sofa/src/nutm80.c \
 sofa/src/obl06.c \
 sofa/src/obl80.c \
 sofa/src/p06e.c \
 sofa/src/p2pv.c \
 sofa/src/p2s.c \
 sofa/src/pap.c \
 sofa/src/pas.c \
 sofa/src/pb06.c \
 sofa/src/pdp.c \
 sofa/src/pfw06.c \
 sofa/src/plan94.c \
 sofa/src/pm.c \
 sofa/src/pmat00.c \
 sofa/src/pmat06.c \
 sofa/src/pmat76.c \
 sofa/src/pmp.c \
 sofa/src/pn.c \
 sofa/src/pn00.c \
 sofa/src/pn00a.c \
 sofa/src/pn00b.c \
 sofa/src/pn06.c \
 sofa/src/pn06a.c \
 sofa/src/pnm00a.c \
 sofa/src/pnm00b.c \
 sofa/src/pnm06a.c \
 sofa/src/pnm80.c \
 sofa/src/pom00.c \
 sofa/src/ppp.c \
 sofa/src/ppsp.c \
 sofa/src/pr00.c \
 sofa/src/prec76.c \
 sofa/src/pv2p.c \
 sofa/src/pv2s.c \
 sofa/src/pvdpv.c \
 sofa/src/pvm.c \
 sofa/src/pvmpv.c \
 sofa/src/pvppv.c \
 sofa/src/pvstar.c \
 sofa/src/pvu.c \
 sofa/src/pvup.c \
 sofa/src/pvxpv.c \
 sofa/src/pxp.c \
 sofa/src/rm2v.c \
 sofa/src/rv2m.c \
 sofa/src/rx.c \
 sofa/src/rxp.c \
 sofa/src/rxpv.c \
 sofa/src/rxr.c \
 sofa/src/ry.c \
 sofa/src/rz.c \
 sofa/src/s00.c \
 sofa/src/s00a.c \
 sofa/src/s00b.c \
 sofa/src/s06.c \
 sofa/src/s06a.c \
 sofa/src/s2c.c \
 sofa/src/s2p.c \
 sofa/src/s2pv.c \
 sofa/src/s2xpv.c \
 sofa/src/sepp.c \
 sofa/src/seps.c \
 sofa/src/sofa.h \
 sofa/src/sofam.h \
 sofa/src/sp00.c \
 sofa/src/starpm.c \
 sofa/src/starpv.c \
 sofa/src/sxp.c \
 sofa/src/sxpv.c \
 sofa/src/taitt.c \
 sofa/src/taiut1.c \
 sofa/src/taiutc.c \
 sofa/src/tcbtdb.c \
 sofa/src/tcgtt.c \
 sofa/src/tdbtcb.c \
 sofa/src/tdbtt.c \
 sofa/src/tf2a.c \
 sofa/src/tf2d.c \
 sofa/src/tr.c \
 sofa/src/trxp.c \
 sofa/src/trxpv.c \
 sofa/src/tttai.c \
 sofa/src/tttcg.c \
 sofa/src/tttdb.c \
 sofa/src/ttut1.c \
 sofa/src/ut1tai.c \
 sofa/src/ut1tt.c \
 sofa/src/ut1utc.c \
 sofa/src/utctai.c \
 sofa/src/utcut1.c \
 sofa/src/xy06.c \
 sofa/src/xys00a.c \
 sofa/src/xys00b.c \
 sofa/src/xys06a.c \
 sofa/src/zp.c \
 sofa/src/zpv.c \
 sofa/src/zr.c

EXTRA_DIST = \
 README.md \
 capi.i \
 novas/solsys2.c \
 novas/solsys3.c

BUILT_SOURCES = capi_wrap.c

capi_wrap.c: capi.i
	$(SWIG) -outcurrentdir -python -builtin $<
	-rm -f precastro.py


# Docs.
#
# We hack EXTRA_DIST to make sure the 'static' directory gets created.
#
# Want to see something terrible? In order for the Sphinx autodoc
# module to work, it needs to be able to import our Python module. But
# it imports a native extension module, which lives within .libs and
# won't be found by Python. My solution is to do a mini "make install"
# into a $DESTDIR in our build tree, because by definition that will
# give us our modules in the correct directory hierarchy with some
# relatively easy munging of $PYTHONPATH.

dist_noinst_DATA = \
 doc/index.txt

EXTRA_DIST += doc/static/.gitignore

sphinx-html.stamp: $(dist_noinst_DATA) precastro.py
	@eval `$(builddir)/libtool --config |$(GREP) ^shlibpath_var` && \
	rm -rf doc/module_staging && \
	$(MKDIR_P) doc/html doc/doctrees doc/module_staging && \
	dest=`cd doc/module_staging && pwd` && \
	eval "$$shlibpath_var=$$dest$(libdir):\$$$$shlibpath_var ; export $$shlibpath_var" && \
	echo ================ Begin scratch doc installation && \
	(cd $(builddir) && \
	 $(MAKE) install-pyexecLTLIBRARIES install-pythonPYTHON DESTDIR=$$dest) && \
	echo ================ End scratch doc installation && \
	PYTHONPATH=$$dest$(pyexecdir):$$dest$(pythondir):$$PYTHONPATH \
	  $(SPHINXBUILD) -d doc/doctrees -c doc -b html $(srcdir)/doc doc/html && \
	rm -rf doc/module_staging && \
	touch $@

if BUILD_DOCS
all-local: sphinx-html.stamp

clean-local:
	-rm -rf doc/doctrees doc/html
	-rm -f sphinx-html.stamp
endif

websitehost = cfa0
websitedir = /data/wdocs/pwilliam/www-docs/palp

pushdocs: sphinx-html.stamp
	ssh $(websitehost) rm -rf $(websitedir)/*
	tar cz -C html . |ssh $(websitehost) tar xz -C $(websitedir)

viewdocs: sphinx-html.stamp
	firefox file://`cd $(builddir) && pwd`/doc/html/index.html &
