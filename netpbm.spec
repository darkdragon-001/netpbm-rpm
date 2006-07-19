Summary: A library for handling different graphics file formats.
Name: netpbm
Version: 10.34
Release: 2
License: freeware
Group: System Environment/Libraries
URL: http://netpbm.sourceforge.net/
Source0: netpbm-%{version}.tar.bz2
Source1: netpbmdoc-%{version}.tar.bz2
Patch0: netpbm-10.28-legal.patch
Patch1: netpbm-10.17-time.patch
Patch2: netpbm-9.24-strip.patch
Patch3: netpbm-10.19-message.patch
Patch4: netpbm-10.22-security2.patch
Patch5: netpbm-10.22-cmapsize.patch
Patch6: netpbm-10.23-security.patch
Patch7: netpbm-10.24-nodoc.patch
Patch8: netpbm-10.28-gcc4.patch
Patch9: netpbm-10.27-bmptopnm.patch
Patch10: netpbm-10.28-CAN-2005-2471.patch
Patch11: netpbm-10.29-pnmtopng.patch
Patch12: netpbm-10.30-rgbtxt.patch
Patch13: netpbm-10.31-xwdfix.patch
Patch14: netpbm-10.33-ppmtompeg.patch
Patch17: netpbm-10.33-multilib.patch
Buildroot: %{_tmppath}/%{name}-root
BuildRequires: libjpeg-devel, libpng-devel, libtiff-devel, perl, flex
BuildRequires: libX11-devel
Obsoletes: libgr

%description
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.

%package devel
Summary: Development tools for programs which will use the netpbm libraries.
Group: Development/Libraries
Requires: netpbm = %{version}-%{release}
Obsoletes: libgr-devel

%description devel
The netpbm-devel package contains the header files and static libraries,
etc., for developing programs which can handle the various graphics file
formats supported by the netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the
graphics file formats supported by the netpbm libraries.  You'll also need
to have the netpbm package installed.

%package progs
Summary: Tools for manipulating graphics files in netpbm supported formats.
Group: Applications/Multimedia
Requires: netpbm = %{version}-%{release}
Obsoletes: libgr-progs

%description progs
The netpbm-progs package contains a group of scripts for manipulating the
graphics files in formats which are supported by the netpbm libraries.  For
example, netpbm-progs includes the rasttopnm script, which will convert a
Sun rasterfile into a portable anymap.  Netpbm-progs contains many other
scripts for converting from one graphics file format to another.

If you need to use these conversion scripts, you should install
netpbm-progs.  You'll also need to install the netpbm package.

%prep
%setup -q
%patch0 -p1 -b .legal
%patch1 -p1 -b .time
%patch2 -p1 -b .strip
%patch3 -p1 -b .message
%patch4 -p1 -b .security2
%patch5 -p1 -b .cmapsize
%patch6 -p1 -b .security
%patch7 -p1 -b .nodoc
%patch8 -p1 -b .gcc4
%patch9 -p1 -b .bmptopnm
%patch10 -p1 -b .CAN-2005-2471
%patch11 -p1 -b .pnmtopng
%patch12 -p1 -b .rgbtxt
%patch13 -p1 -b .xwdfix
%patch14 -p1 -b .ppmtompeg
%patch17 -p1 -b .multilib

##mv shhopt/shhopt.h shhopt/pbmshhopt.h
##perl -pi -e 's|shhopt.h|pbmshhopt.h|g' `find -name "*.c" -o -name "*.h"` ./GNUmakefile

%build
./configure <<EOF



















EOF

TOP=`pwd`
make \
	CC=%{__cc} \
	CFLAGS="$RPM_OPT_FLAGS -fPIC" \
	LDFLAGS="-L$TOP/pbm -L$TOP/pgm -L$TOP/pnm -L$TOP/ppm" \
	LADD="-lm" \
	JPEGINC_DIR=%{_includedir} \
	PNGINC_DIR=%{_includedir} \
	TIFFINC_DIR=%{_includedir} \
	JPEGLIB_DIR=%{_libdir} \
	PNGLIB_DIR=%{_libdir} \
	TIFFLIB_DIR=%{_libdir} \
	LINUXSVGALIB="NONE" \
	X11LIB=%{_libdir}/libX11.so \
	XML2LIBS="NONE"

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT
make package pkgdir=$RPM_BUILD_ROOT/usr LINUXSVGALIB="NONE" XML2LIBS="NONE"

# Ugly hack to have libs in correct dir on 64bit archs.
mkdir -p $RPM_BUILD_ROOT%{_libdir}
if [ "%{_libdir}" != "/usr/lib" ]; then
  mv $RPM_BUILD_ROOT/usr/lib/lib* $RPM_BUILD_ROOT%{_libdir}
fi

cp -af lib/libnetpbm.a $RPM_BUILD_ROOT%{_libdir}/libnetpbm.a
ln -sf libnetpbm.so.10 $RPM_BUILD_ROOT%{_libdir}/libnetpbm.so

mkdir -p $RPM_BUILD_ROOT%{_mandir}
tar jxvf %{SOURCE1} -C $RPM_BUILD_ROOT%{_mandir}

# Don't ship man packages for non-existent binaries
for i in hpcdtoppm.1 pcdovtoppm.1 pnmtojbig.1 \
	 ppmsvgalib.1 vidtoppm.1 picttoppm.1 jbigtopnm.1; do
	rm -f $RPM_BUILD_ROOT%{_mandir}/man1/${i}
done

mv $RPM_BUILD_ROOT/usr/misc/*.map $RPM_BUILD_ROOT%{_libdir}
rm -rf $RPM_BUILD_ROOT/usr/README
rm -rf $RPM_BUILD_ROOT/usr/VERSION
rm -rf $RPM_BUILD_ROOT/usr/link
rm -rf $RPM_BUILD_ROOT/usr/misc
rm -rf $RPM_BUILD_ROOT/usr/man
rm -rf $RPM_BUILD_ROOT/usr/pkginfo
rm -rf $RPM_BUILD_ROOT/usr/config_template



%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc doc/COPYRIGHT.PATENT doc/GPL_LICENSE.txt doc/HISTORY README
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_mandir}/man3/*
%files progs
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.map
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Wed Jul 19 2006 Jindrich Novy <jnovy@redhat.com> 10.34-2
- fix double free corruption in ppmtompeg (#199409),
  thanks to Milan Zazrivec

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 10.34-1.1
- rebuild

* Thu Jun 22 2006 Jindrich Novy <jnovy@redhat.com> 10.34-1
- update to 10.34
- drop .ppmtogif, .nstring patches
- remove some overflow checks from .security patch, it's
  now resolved in the new upstream version
- don't use svgalib by default (don't compile/ship ppmsvgalib)
- don't compile svgtopam because of the libxml dependency
- add BuildRequires libX11-devel
- fix build on x86_64 and ppc64

* Mon Jun  5 2006 Jindrich Novy <jnovy@redhat.com> 10.33-3
- fix multilib conflict (#192735)
- remove jbigtopnm man page

* Thu Apr 14 2006 Jindrich Novy <jnovy@redhat.com> 10.33-2
- fix image corruption in ppmtogif, thanks to Gilles Detillieux (#188597)
- fix nsting.h to let pnmtopng and other utilities using seekable opening
  mode work on x86_64 (#188594)

* Wed Apr  5 2006 Jindrich Novy <jnovy@redhat.com> 10.33-1
- update to 10.33
- drop upstreamed .ppmdepth patch
- fix segfault in ppmtompeg when encoding jpeg images (#185970)

* Mon Apr  3 2006 Jindrich Novy <jnovy@redhat.com> 10.32-2
- fix broken symlink in upstream: pnmsdepth -> pamdepth  (#187667)

* Tue Feb 28 2006 Jindrich Novy <jnovy@redhat.com> 10.32-1
- update to 10.32
- drop .msbmp patch, applied upstream
- sync the rest of the patches
- regenerate man pages

* Mon Feb 20 2006 Jindrich Novy <jnovy@redhat.com> 10.31-5
- add missing flex BuildRequires
- fix anytopnm to recognize ms-bmp files (#182060)

* Tue Feb 14 2006 Jindrich Novy <jnovy@redhat.com> 10.31-4
- make xwdtopnm work on x86_64 (#181001)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 10.31-3.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Jindrich Novy <jnovy@redhat.com> 10.31-3
- fix segfault caused by usage of uninitialized variables while
  parsing cmdline arguments in pnmtopng (#179645)
- add validity check for date/time in pnmtopng
- fix unchecked sscanf reads

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 10.31-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Jindrich Novy <jnovy@redhat.com> 10.31-2
- rebuild to have greater version than in FC4 (#177698)

* Fri Dec 30 2005 Jindrich Novy <jnovy@redhat.com> 10.31-1
- update to 10.31
- update security patch
- regenerate man pages

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 29 2005 Jindrich Novy <jnovy@redhat.com> 10.30-2
- fix path to rgb.txt to fit modular X (#174128)

* Fri Oct 21 2005 Jindrich Novy <jnovy@redhat.com> 10.30-1
- update to 10.30
- update manpath, gcc4 patches
- update security patch - fixed length problem in rle_addhist
- update partly upstreamed bmptopnm, pnmtopng patches
- drop manpath patch
- regenerate man pages

* Thu Oct 06 2005 Jindrich Novy <jnovy@redhat.com> 10.29-2
- fix segfault in pnmtopng caused by referencing a NULL pointer (#169532)

* Tue Aug 16 2005 Jindrich Novy <jnovy@redhat.com> 10.29-1
- update to 10.29
- drop upstreamed .libpm, .pnmtojpeg, .pbmtolj patches
- update .CAN-2005-2471 patch

* Mon Aug 15 2005 Jindrich Novy <jnovy@redhat.com> 10.28-6
- link libnetpbm.so against -lm (#165980)

* Tue Aug 09 2005 Jindrich Novy <jnovy@redhat.com> 10.28-5
- fix CAN-2005-2471, unsafe gs calls from pstopnm (#165355)

* Thu Jul 21 2005 Jindrich Novy <jnovy@redhat.com> 10.28-4
- fix buffer overflow in pbmtolj (#163596)

* Mon Jun 27 2005 Jindrich Novy <jnovy@redhat.com> 10.28-3
- create symlink pnmtopnm -> pamtopnm, this works now in
  netpbm-10.28 (#161436)

* Tue Jun 21 2005 Jindrich Novy <jnovy@redhat.com> 10.28-2
- fix segfault in pbmtolj caused by unchecked assertions
  caused by definition of NDEBUG (#160429)
- drop hunk from .security patch causing dual inclusion
  of string.h in pbmtolj.c

* Fri Jun 10 2005 Jindrich Novy <jnovy@redhat.com> 10.28-1
- update to 10.28
- regenerated man pages
- sync .security, .security2, .badlink, .libpm, .gcc4 patches
- drop upstreamed .pngtopnm, .pnmcolormap patches

* Tue May 31 2005 Jindrich Novy <jnovy@redhat.com> 10.27-4
- fix segfault in pnmcolormap what makes latex2html/ppmquant
  unusable (#158665, #139111)

* Mon May 16 2005 Jindrich Novy <jnovy@redhat.com> 10.27-3
- fix ppmdither leak caused by bug in security patch (#157757)
- drop gcc34 patch

* Mon May 09 2005 Jindrich Novy <jnovy@redhat.com> 10.27-2
- fix invalid strcmp condition in bmptopnm, typo in pnmtojpeg
  (David Constanzo, #157106, #157118)
- proper read longs and shorts in libpm.c (David Constanzo, #157110)
- fix segfault in bmptopnm caused by freeing an uninitialized pointer

* Tue Mar 29 2005 Jindrich Novy <jnovy@redhat.com> 10.27-1
- update to the new 10.27 release
- update .security2, .security patch
- regenerate man pages
- remove jbig, hpcd
- remove config_template from /usr
- don't create symlink to pamtopnm

* Mon Mar 14 2005 Jindrich Novy <jnovy@redhat.com> 10.26.4-3
- fix overflow checking of integers with incompatible endianess
  causing problems using xwdtopnm (#147790)

* Mon Mar 09 2005 Jindrich Novy <jnovy@redhat.com> 10.26.4-2
- add .gcc4 patch to fix some missing declarations of headers,
  some pointer signedness mismatches, remove xmalloc2
- rebuilt with gcc4

* Thu Mar 03 2005 Jindrich Novy <jnovy@redhat.com> 10.26.4-1
- update to netpbm-10.26.4, remove jbig, hpcd
- this version fixes #149924
- regenerate man pages (don't include man pages without binaries - #146863)

* Wed Jan 05 2005 Jindrich Novy <jnovy@redhat.com> 10.26-1
- update to netpbm-10.26-1, remove jbig, hpcd
- regenerate man pages, remove man pages for non existent binaries
- update security patch, additional fixes
- drop upstreamed misc patch, merge malloc patch with security patch

* Mon Oct 25 2004 Jindrich Novy <jnovy@redhat.com> 10.25-3
- include man pages in troff format, thanks to Michal Jaegerman (#136959)
- drop bmpbpp patch, fixed upstream
- remove pcdovtoppm, ppmsvgalib, vidtoppm man pages because binaries
  for them are not present (#136471)

* Mon Oct 18 2004 Jindrich Novy <jnovy@redhat.com> 10.25-2
- avoid compile crash when "-msse" is in CFLAGS

* Mon Oct 18 2004 Jindrich Novy <jnovy@redhat.com> 10.25-1
- update to latest upstream 10.25
- drop initvar patch
- update security, misc patch
- add bmpbpp patch to use only appropriate bit depths for BMP (#135675)

* Thu Sep 23 2004 Jindrich Novy <jnovy@redhat.com> 10.24-3
- added patch to suppress installation of doc.url to /usr/bin #133346

* Wed Aug 18 2004 Jindrich Novy <jnovy@redhat.com> 10.24-2
- added patch to fix compile crash for 64bit machines
- various hacks related to .security patch

* Mon Aug 16 2004 Jindrich Novy <jnovy@redhat.com> 10.24-1
- updated to 10.24
- updated docs

* Thu Aug 05 2004 Jindrich Novy <jnovy@redhat.com> 10.23-2
- added pngtopnm patch
- added malloc patch

* Tue Aug 03 2004 Jindrich Novy <jnovy@redhat.com> 10.23-1
- updated to netpbm-10.23 upsteam (and removed jbig, hpcd)
- $TMPDIR patch removed, obsolete
- updated gcc34 patch
- removed nestedfunc patch, already applied in upstream version
- updated security patch to conform to 10.23 (mostly in ppmtompeg/frame.c)

* Fri Jul 02 2004 Phil Knirsch <pknirsch@redhat.com> 10.22-2
- Fixed Zero byte allocation error in bmptopnm (#123169)
- Honour the $TMPDIR in ppmfade (#117247)
- Fixed nested function bug (#117377)
- Fixed several uninitialized variables (#117377)

* Mon Jun 28 2004 Phil Knirsch <pknirsch@redhat.com> 10.22-1
- Update to latest upstream version 10.22 (also for docs).
- Removed jbig and hdcp code from tarball.

* Sat Jun 19 2004 Alan Cox <alan@redhat.com>
- merged fix for pnmrotate crash freeing wrong number of rows

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 30 2004 Harald Hoyer <harald@redhat.com> - 10.19-7
- fixed compilation with gcc34

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 17 2004 Phil Knirsch <pknirsch@redhat.com> 10.19-6
- Fixed problem in pnmquant with GetOptions() and args/ARGV (#115788).

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 10.19-5
- rebuilt

* Tue Feb 10 2004 Phil Knirsch <pknirsch@redhat.com> 10.19-4
- Fixed several tmp vulnerabilities in scripts and apps. Based on Debian
  security fix for netpbm-9.24.

* Mon Feb 09 2004 Phil Knirsch <pknirsch@redhat.com> 10.19-3
- Included doc tarball with manpages (#114755).
- Fixed small manpage incorrectness (#84922).
- Fixed message from giftopnm (#114756).

* Fri Jan 30 2004 Phil Knirsch <pknirsch@redhat.com> 10.19-2
- No need anymore to fix ppmfade and ppmshade.

* Thu Jan 29 2004 Phil Knirsch <pknirsch@redhat.com> 10.19-1
- Major update to latest upstream version 10.19.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 28 2003 Phil Knirsch <pknirsch@redhat.com> 9.24-11
- Updated Alan's patch.

* Wed Feb 19 2003 Phil Knirsch <pknirsch@redhat.com> 9.24-10
- Added big security patch by Alan Cox.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 9.24-9
- rebuilt

* Thu Dec 19 2002 Phil Knirsch <pknirsch@redhat.com> 9.24-8
- Removed print filters again as they are too dangerous.

* Mon Dec 16 2002 Elliot Lee <sopwith@redhat.com> 9.24-7
- Merge in hammer changes, rebuild

* Sun Sep 08 2002 Arjan van de Ven <arjanv@redhat.com>
- fix for x86-64

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 9.24-5
- Don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 09 2002 Phil Knirsch <pknirsch@redhat.com> 9.24-3
- Fixed a possible gcc compiler problem for inline struct parameters (#62181).
- Added missing .map files to progs files selection (#61625).

* Tue Apr 02 2002 Phil Knirsch <pknirsch@redhat.com> 9.24-2
- Fixed stupid dangling symlink problem (#62478)

* Tue Mar 12 2002 Phil Knirsch <pknirsch@redhat.com> 9.24-1
- Updated to netpbm version 9.24
- Hacked around a couple of library problems.

* Tue Nov 06 2001 Phil Knirsch <phil@redhat.de>
- Updated to netpbm version 9.20

* Fri Jun 22 2001 Philipp Knirsch <pknirsch@redhat.de>
- Updated to netpbm version 9.14
- Removed pnmtotiff resize patch as it is now part of the original package
- Removed pstopnm csh fix as it is now part of the original package
- Removed asciitopgm memcpy fix as it is now part of the original package
- Removed manpages patch as it is now part of the original package

* Mon Feb 12 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #26767 where the new glibc time and sys/time fixes needed
  to be done.

* Fri Feb  9 2001 Crutcher Dunnavant <crutcher@redhat.com>
- switched filters to printconf filters

* Wed Jan 24 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #21644 where few manpages had a small error.

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #19487 where asciitopgm dumped core on Alpha. Actually
  dumped core everywhere

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- update to 9.9
- Due to patent infringement problems removed the jbig support from the tarball
  (pnm/jbig + Makefile changes) and created a new tarball

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- include shared libraries missing from previous build

* Tue Oct 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 9.8
- make sure shhopt.h is included in the -devel package (#19672)
- rename shhopt.h to pbmshhopt.h because it's not the same as the normal
  shhopt.h that other things (like util-linux) expect

* Wed Aug  9 2000 Crutcher Dunnavant <crutcher@redhat.com>
- added a png-to-pnm.fpi filter

* Wed Aug  2 2000 Matt Wilson <msw@redhat.com>
- rebuilt against new libpng

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- move netpbm-progs to the Applications/Multimedia group
- reintroduce patches from the old libgr package

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jul  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 9.5

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 9.4

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- switch back to the netpbm tree, which is maintained again

* Mon Feb 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- make sure all man pages are included (#9328)
- fix pstopnm bomb when xres == yres (#9329)
- add libjpeg and libz because libtiff now needs them

* Wed Feb 02 2000 Nalin Dahyabhai <nalin@redhat.com>
- added/updated TIFF compression patch from jik@kamens.brookline.ma.us (#8826)

* Mon Dec 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- added TIFF resolution patch from jik@kamens.brookline.ma.us (#7589)

* Mon Sep 20 1999 Michael K. Johnson <johnsonm@redhat.com>
- added section 5 man pages

* Fri Jul 30 1999 Bill Nottingham <notting@redhat.com>
- fix tiff-to-pnm.fpi (#4267)

* Thu Jul 29 1999 Bill Nottingham <notting@redhat.com>
- add a pile of foo-to-bar.fpi filters (#4251)

* Mon Mar 23 1999 Michael Johnson <johnsonm@redhat.com>
- removed old png.h header file that was causing png utils to die
- build png in build instead of install section...

* Mon Mar 22 1999 Bill Nottingham <notting@redhat.com>
- patch for 24-bit .BMP files (from sam@campbellsci.co.uk)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 15)

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- clean up the spec file
- build for glibc 2.1
- patch to fix pktopbm

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Wed Jun 10 1998 Jeff Johnson <jbj@redhat.com>
- glibc2 defines random in <stdlib.h> (pbm/pbmplus.h problem #693)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu May 07 1998 Cristian Gafton <gafton@redhat.com>
- cleaned up the spec file a little bit
- validated mike's changes :-)

* Wed May 6 1998 Michael Maher <mike@redhat.com>
- added pnm-to-ps.fpi that was missing from previous packages

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- altered install so that the package installs now even if a previous
  version was not installed on the system 

* Thu Apr 16 1998 Erik Troan <ewt@redhat.com>
- built against libpng 1.0

* Thu Nov 06 1997 Donnie Barnes <djb@redhat.com>
- changed copyright from "distributable" to "freeware"
- added some missing scripts that existed in netpbm
- added some binaries that weren't getting built
- added patch to build tiff manipulation progs (requires libtiff)

* Wed Oct 15 1997 Donnie Barnes <djb@redhat.com>
- obsoletes netpbm now

* Tue Oct 14 1997 Erik Troan <ewt@redhat.com>
- mucked config.guess and Make.Rules to build on Alpha/Linux

* Tue Oct 07 1997 Donnie Barnes <djb@redhat.com>
- updated to 2.0.13
- dropped libjpeg and libtiff (those should come from home sources)
- removed glibc patch (new version appears to have it!)
- added i686 as a valid arch type to config.guess

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

