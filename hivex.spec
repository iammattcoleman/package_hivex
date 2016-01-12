# Conditionalize Ocaml support.  This looks ass-backwards, but it's not.
%ifarch %{ocaml_native_compiler}
%bcond_without ocaml
%else
%bcond_with ocaml
%endif

Name:           hivex
Version:        1.3.13
Release:        3%{?dist}
Summary:        Read and write Windows Registry binary hive files

License:        LGPLv2
URL:            http://libguestfs.org/

Source0:        http://libguestfs.org/download/hivex/%{name}-%{version}.tar.gz

BuildRequires:  perl
BuildRequires:  %{_bindir}/pod2html
BuildRequires:  %{_bindir}/pod2man
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(IO::Stringy)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
%if %{with ocaml}
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
%endif
BuildRequires:  python-devel
BuildRequires:  ruby-devel
BuildRequires:  rubygem-rake
BuildRequires:  rubygem(minitest)
BuildRequires:  readline-devel
BuildRequires:  libxml2-devel

# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Packages_granted_exceptions
Provides:      bundled(gnulib)


%description
Hive files are the undocumented binary files that Windows uses to
store the Windows Registry on disk.  Hivex is a library that can read
and write to these files.

'hivexsh' is a shell you can use to interactively navigate a hive
binary file.

'hivexregedit' (in perl-hivex) lets you export and merge to the
textual regedit format.

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
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig


%description devel
%{name}-devel contains development tools and libraries
for %{name}.


%package static
Summary:        Statically linked library for %{name}
Requires:       %{name} = %{version}-%{release}


%description static
%{name}-static contains the statically linked library
for %{name}.


%if %{with ocaml}
%package -n ocaml-%{name}
Summary:       OCaml bindings for %{name}
Requires:      %{name} = %{version}-%{release}


%description -n ocaml-%{name}
ocaml-%{name} contains OCaml bindings for %{name}.

This is for toplevel and scripting access only.  To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel.


%package -n ocaml-%{name}-devel
Summary:       OCaml bindings for %{name}
Requires:      ocaml-%{name} = %{version}-%{release}


%description -n ocaml-%{name}-devel
ocaml-%{name}-devel contains development libraries
required to use the OCaml bindings for %{name}.
%endif


%package -n perl-%{name}
Summary:       Perl bindings for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description -n perl-%{name}
perl-%{name} contains Perl bindings for %{name}.


%package -n python-%{name}
Summary:       Python bindings for %{name}
Requires:      %{name} = %{version}-%{release}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description -n python-%{name}
python-%{name} contains Python bindings for %{name}.


%package -n ruby-%{name}
Summary:       Ruby bindings for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      ruby(release)
Requires:      ruby
Provides:      ruby(hivex) = %{version}

%description -n ruby-%{name}
ruby-%{name} contains Ruby bindings for %{name}.


%prep
%setup -q


%build
%configure
make V=1 INSTALLDIRS=vendor %{?_smp_mflags}


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
make install DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor

# Remove unwanted libtool *.la file:
rm $RPM_BUILD_ROOT%{_libdir}/libhivex.la

# Remove unwanted Perl files:
find $RPM_BUILD_ROOT -name perllocal.pod -delete
find $RPM_BUILD_ROOT -name .packlist -delete
find $RPM_BUILD_ROOT -name '*.bs' -delete

# Remove unwanted Python files:
rm $RPM_BUILD_ROOT%{python_sitearch}/libhivexmod.la

%find_lang %{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%doc README LICENSE
%{_bindir}/hivexget
%{_bindir}/hivexml
%{_bindir}/hivexsh
%{_libdir}/libhivex.so.*
%{_mandir}/man1/hivexget.1*
%{_mandir}/man1/hivexml.1*
%{_mandir}/man1/hivexsh.1*


%files devel
%doc LICENSE
%{_libdir}/libhivex.so
%{_mandir}/man3/hivex.3*
%{_includedir}/hivex.h
%{_libdir}/pkgconfig/hivex.pc


%files static
%doc LICENSE
%{_libdir}/libhivex.a


%if %{with ocaml}
%files -n ocaml-%{name}
%doc README
%{_libdir}/ocaml/hivex
%exclude %{_libdir}/ocaml/hivex/*.a
%exclude %{_libdir}/ocaml/hivex/*.cmxa
%exclude %{_libdir}/ocaml/hivex/*.cmx
%exclude %{_libdir}/ocaml/hivex/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files -n ocaml-%{name}-devel
%{_libdir}/ocaml/hivex/*.a
%{_libdir}/ocaml/hivex/*.cmxa
%{_libdir}/ocaml/hivex/*.cmx
%{_libdir}/ocaml/hivex/*.mli
%endif


%files -n perl-%{name}
%{perl_vendorarch}/*
%{_mandir}/man3/Win::Hivex.3pm*
%{_mandir}/man3/Win::Hivex::Regedit.3pm*
%{_bindir}/hivexregedit
%{_mandir}/man1/hivexregedit.1*


%files -n python-%{name}
%{python_sitearch}/hivex/*.py
%{python_sitearch}/hivex/*.pyc
%{python_sitearch}/hivex/*.pyo
%{python_sitearch}/*.so


%files -n ruby-%{name}
%doc ruby/doc/site/*
%{ruby_vendorlibdir}/hivex.rb
%{ruby_vendorarchdir}/_hivex.so


%changelog
* Tue Jan 12 2016 Vít Ondruch <vondruch@redhat.com> - 1.3.13-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Thu Oct 29 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.13-2
- New upstream version 1.3.13.
- Drop ancient 'Conflicts' rule.
- Drop Perl patch for setting INSTALLDIRS.
- Depend on pod2html, pod2man binaries explicitly.

* Mon Oct  5 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.12-1
- New upstream version 1.3.12.
- Drop patches which are now upstream.
- Use OCaml macros to test if OCaml native compiler is available.
- Use autoreconf --force option.

* Thu Aug 27 2015 Petr Šabata <contyk@redhat.com> - 1.3.11-13
- Correcting the perl build time dependency list
  Switching to virtual perl()-style symbols
  Dropping unused dependencies and adding some new to fix the FTBFS

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.11-12
- OCaml 4.02.3 rebuild.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.11-11
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.11-10
- ocaml-4.02.2 rebuild.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.11-8
- Perl 5.22 rebuild

* Mon Mar  2 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.11-7
- Move hivexregedit to perl-hivex subpackage, since otherwise hivex
  and hence libguestfs depends on perl (RHBZ#1194158).

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.11-6
- ocaml-4.02.1 rebuild.

* Sun Jan 18 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.11-5
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Thu Nov 20 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.11-4
- Increase HIVEX_MAX_SUBKEYS.
- Don't leak errno E2BIG to callers.

* Fri Nov 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.11-2
- Pull in a couple of upstream fixes:
  * Fix memory leak in _hivex_get_children.
  * Increase HIVEX_MAX_VALUE_LEN.

* Thu Oct 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.11-1
- New upstream version 1.3.11.
- Python objects are now placed in a hivex/ subdirectory.

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.10-12
- Perl 5.20 rebuild

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-11
- ocaml-4.02.0 final rebuild.

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.10-10
- Perl 5.20 rebuild

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-9
- ocaml-4.02.0+rc1 rebuild.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-7
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-6
- OCaml 4.02.0 beta rebuild.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Vít Ondruch <vondruch@redhat.com> - 1.3.10-4
- Remove the ruby(release) version. It is not needed.

* Fri May 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-3
- Rebuild to fix Ruby dependencies problem.

* Thu Apr 24 2014 Vít Ondruch <vondruch@redhat.com> - 1.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Wed Apr 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.10-1
- New upstream version 1.3.10.
- Fix ruby test failures (RHBZ#1090407).

* Fri Jan 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.9-2
- New upstream version 1.3.9.
- Remove patches which are now upstream.

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.8-4
- OCaml 4.01.0 rebuild.

* Tue Sep 10 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.8-3
- Include various upstream patches to fix endianness problems on ppc64.

* Sun Sep  8 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.8-2
- Bump and rebuild, since ARM package still appears to depend on Perl 5.16.

* Thu Jul 25 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.8-1
- New upstream version 1.3.8.
- Fixes handling of keys which use ri-records, for both reading and
  writing (RHBZ#717583, RHBZ#987463).
- Remove upstream patch.
- Rebase dirs patch against new upstream sources.
- Rebase ruby patch against new upstream sources.
- Modernize the RPM spec file.
- Fix .gitignore.

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.3.7-8
- Perl 5.18 rebuild

* Wed Mar 13 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.7-7
- Rebuild for Ruby 2.0.0.
- Change ruby(abi) to ruby(release).

* Fri Feb 15 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.7-6
- Fix for latest Ruby in Rawhide.  Fixes build failure identified
  by mass rebuild yesterday.
- Do not ignore error from running autoreconf.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.7-2
- Rebuild for OCaml 4.00.1.

* Thu Oct 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.7-1
- New upstream version 1.3.7.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 1.3.6-2
- Perl 5.16 rebuild

* Tue Jun 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.6-1
- New upstream version 1.3.6.
- Enable Ocaml bindings on ppc64.

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.5-9
- Rebuild for OCaml 4.00.0.

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.3.5-8
- Perl 5.16 rebuild

* Fri May 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.5-7
- "blobs" -> "files" in the description.

* Tue May 15 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.5-6
- Bundled gnulib (RHBZ#821763).

* Fri Mar 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.5-5
- Don't need to rerun the generator (thanks Dan Horák).

* Tue Mar 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.5-4
- New upstream version 1.3.5.
- Remove upstream patch.
- Depend on automake etc. for the patch.

* Thu Feb  9 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-8
- ruby(abi) 1.9.1.

* Wed Feb  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-7
- Bump and rebuild for Ruby update.
- Add upstream patch to fix bindings for Ruby 1.9.
- Add non-upstream patch to pass --vendor flag to extconf.rb

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-3
- Rebuild for OCaml 3.12.1.

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
