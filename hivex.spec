# conditionalize Ocaml support
%ifarch ppc64 sparc64 s390 s390x
%bcond_with ocaml
%else
%bcond_without ocaml
%endif

Name:           hivex
Version:        1.3.3
Release:        2%{?dist}
Summary:        Read and write Windows Registry binary hive files

Group:          Development/Libraries
License:        LGPLv2
URL:            http://libguestfs.org/
Source0:        http://libguestfs.org/download/hivex/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-IO-stringy
BuildRequires:  perl-libintl
%if %{with ocaml}
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
%endif
BuildRequires:  python-devel
BuildRequires:  ruby-devel
BuildRequires:  rubygem-rake
BuildRequires:  readline-devel
BuildRequires:  libxml2-devel

# This library used to be part of libguestfs.  It won't install alongside
# the old version of libguestfs that included this library:
Conflicts:      libguestfs <= 1:1.0.84

# Fix Perl directory install path.
Patch0:         %{name}-1.2.3-dirs.patch


%description
Hive files are the undocumented binary blobs that Windows uses to
store the Windows Registry on disk.  Hivex is a library that can read
and write to these files.

'hivexsh' is a shell you can use to interactively navigate a hive
binary file.

'hivexregedit' lets you export and merge to the textual regedit
format.

'hivexml' can be used to convert a hive file to a more useful XML
format.

In order to get access to the hive files themselves, you can copy them
from a Windows machine.  They are usually found in
%%systemroot%%\system32\config.  For virtual machines we recommend
using libguestfs or guestfish to copy out these files.  libguestfs
also provides a useful high-level tool called 'virt-win-reg' (based on
hivex technology) which can be used to query specific registry keys in
an existing Windows VM.

For OCaml bindings, see 'ocaml-hivex-devel'.

For Perl bindings, see 'perl-hivex'.

For Python bindings, see 'python-hivex'.

For Ruby bindings, see 'ruby-hivex'.


%package devel
Summary:        Development tools and libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig


%description devel
%{name}-devel contains development tools and libraries
for %{name}.


%package static
Summary:        Statically linked library for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description static
%{name}-static contains the statically linked library
for %{name}.


%if %{with ocaml}
%package -n ocaml-%{name}
Summary:       OCaml bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}


%description -n ocaml-%{name}
ocaml-%{name} contains OCaml bindings for %{name}.

This is for toplevel and scripting access only.  To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel.


%package -n ocaml-%{name}-devel
Summary:       OCaml bindings for %{name}
Group:         Development/Libraries
Requires:      ocaml-%{name} = %{version}-%{release}


%description -n ocaml-%{name}-devel
ocaml-%{name}-devel contains development libraries
required to use the OCaml bindings for %{name}.
%endif


%package -n perl-%{name}
Summary:       Perl bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description -n perl-%{name}
perl-%{name} contains Perl bindings for %{name}.


%package -n python-%{name}
Summary:       Python bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description -n python-%{name}
python-%{name} contains Python bindings for %{name}.


%package -n ruby-%{name}
Summary:       Ruby bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Requires:      ruby(abi) = 1.8
Requires:      ruby
Provides:      ruby(hivex) = %{version}

%{!?ruby_sitelib: %global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

%description -n ruby-%{name}
ruby-%{name} contains Ruby bindings for %{name}.


%prep
%setup -q

%patch0 -p1 -b .dirs


%build
%configure
make %{?_smp_mflags}


%check
make check

%if !%{with ocaml}
# Delete OCaml files, in case the user had OCaml installed and it was
# picked up by the configure script.
# XXX Add ./configure --disable-ocaml upstream.
rm -rf $RPM_BUILD_ROOT%{_libdir}/ocaml/hivex
rm -f  $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*hivex*
%endif


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove unwanted libtool *.la file:
rm $RPM_BUILD_ROOT%{_libdir}/libhivex.la

# Remove unwanted Perl files:
find $RPM_BUILD_ROOT -name perllocal.pod -delete
find $RPM_BUILD_ROOT -name .packlist -delete
find $RPM_BUILD_ROOT -name '*.bs' -delete

# Remove unwanted Python files:
rm $RPM_BUILD_ROOT%{python_sitearch}/libhivexmod.la

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README LICENSE
%{_bindir}/hivexget
%{_bindir}/hivexml
%{_bindir}/hivexregedit
%{_bindir}/hivexsh
%{_libdir}/libhivex.so.*
%{_mandir}/man1/hivexget.1*
%{_mandir}/man1/hivexml.1*
%{_mandir}/man1/hivexregedit.1*
%{_mandir}/man1/hivexsh.1*


%files devel
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/libhivex.so
%{_mandir}/man3/hivex.3*
%{_includedir}/hivex.h
%{_libdir}/pkgconfig/hivex.pc


%files static
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/libhivex.a


%if %{with ocaml}
%files -n ocaml-%{name}
%defattr(-,root,root,-)
%doc README
%{_libdir}/ocaml/hivex
%exclude %{_libdir}/ocaml/hivex/*.a
%exclude %{_libdir}/ocaml/hivex/*.cmxa
%exclude %{_libdir}/ocaml/hivex/*.cmx
%exclude %{_libdir}/ocaml/hivex/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files -n ocaml-%{name}-devel
%defattr(-,root,root,-)
%{_libdir}/ocaml/hivex/*.a
%{_libdir}/ocaml/hivex/*.cmxa
%{_libdir}/ocaml/hivex/*.cmx
%{_libdir}/ocaml/hivex/*.mli
%endif


%files -n perl-%{name}
%defattr(-,root,root,-)
%{perl_vendorarch}/*
%{_mandir}/man3/Win::Hivex.3pm*
%{_mandir}/man3/Win::Hivex::Regedit.3pm*


%files -n python-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/*.py
%{python_sitearch}/*.pyc
%{python_sitearch}/*.pyo
%{python_sitearch}/*.so


%files -n ruby-%{name}
%defattr(-,root,root,-)
%doc ruby/doc/site/*
%{ruby_sitelib}/hivex.rb
%{ruby_sitearch}/_hivex.so


%changelog
* Thu Dec  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-2
- Disable OCaml on ppc64.
- Ensure OCaml files are deleted when not packaged.

* Tue Nov 29 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-1
- New upstream version 1.3.3.
- Rebased gnulib to work around RHBZ#756981.
- Remove patches which are now upstream.

* Mon Oct 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.2-3
- New upstream version 1.3.2.
- Add upstream patch to fix building of hivexsh, hivexget.

* Fri Aug 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-2
- New upstream version 1.3.1.
- Remove patch, now upstream.
- Don't need hack for making an unversioned Python module.

* Mon Aug 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.0-3
- New upstream version 1.3.0.
- This version adds Ruby bindings, so there is a new subpackage 'ruby-hivex'.
- Add upstream patch to fix Ruby tests.
- Remove epoch macro in ruby-hivex dependency.

* Fri Aug 12 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.8-1
- New upstream version 1.2.8.
- Remove 4 upstream patches.

* Fri Jul 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.7-9
- Add upstream patch to fix Perl CCFLAGS for Perl 5.14 on i686.
- Enable 'make check'.

* Thu Jul 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.7-6
- i686 package is broken, experimentally rebuild it.

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.7-5
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.7-4
- Perl 5.14 mass rebuild

* Tue May 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.7-3
- New upstream version 1.2.7.
- Removed patch which is now upstream.
- Add upstream patches to fix ocaml install rule.

* Thu May 12 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.6-2
- New upstream version 1.2.6.
- Removed patch which is now upstream.
- Add upstream patch to fix ocaml tests.

* Thu Apr 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-2
- Fix Python bindings on 32 bit arch with upstream patch.

* Wed Apr 13 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-1
- New upstream version 1.2.5.
- This version fixes a number of important memory issues found by
  valgrind and upgrading to this version is recommended for all users.
- Remove patch now upstream.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-6
- Fix multilib conflicts in *.pyc and *.pyo files.
- Only install unversioned *.so file for Python bindings.

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-4
- Rebuild against OCaml 3.12.0.

* Thu Dec 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-3
- Backport upstream patch to fix segfault in Hivex.value_value binding.

* Thu Dec  2 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-1
- New upstream version 1.2.4.
- This adds Python bindings (python-hivex subpackage).
- Fix Source0.

* Fri Nov 19 2010 Dan Horák <dan[at]danny.cz> - 1.2.3-3
- fix built with recent perl

* Tue Sep  7 2010 Dan Horák <dan[at]danny.cz> - 1.2.3-2
- conditionalize ocaml support

* Fri Aug 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-1
- New upstream version 1.2.3.

* Wed Aug 25 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-3
- Create a hivex-static subpackage.

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2.2-2
- Mass rebuild with perl-5.12.0

* Wed Apr 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-1
- New upstream version 1.2.2.

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-1
- New upstream version 1.2.1.
- Includes new tool for exporting and merging in regedit format.

* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-2
- New upstream version 1.2.0.
- This includes OCaml and Perl bindings, so add these as subpackages.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-3
- Missing Epoch in conflicts version fixed.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-2
- Add Conflicts libguestfs <= 1.0.84.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-1
- Initial Fedora RPM.
