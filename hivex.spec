Name:           hivex
Version:        1.2.0
Release:        2%{?dist}
Summary:        Read and write Windows Registry binary hive files

Group:          Development/Libraries
License:        LGPLv2
URL:            http://libguestfs.org/
Source0:        http://libguestfs.org/download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-libintl
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
BuildRequires:  readline-devel
BuildRequires:  libxml2-devel

# This library used to be part of libguestfs.  It won't install alongside
# the old version of libguestfs that included this library:
Conflicts:      libguestfs <= 1:1.0.84


%description
Hive files are the undocumented binary blobs that Windows uses to
store the Windows Registry on disk.  Hivex is a library that can read
and write to these files.

'hivexsh' is a shell you can use to interactively navigate a hive
binary file.

'hivexml' can be used to convert a hive file to a more useful XML
format.

In order to get access to the hive files themselves, you can copy them
from a Windows machine.  They are usually found in
%%systemroot%%\system32\config.  For virtual machines we recommend
using libguestfs or guestfish to copy out these files.  libguestfs
also provides a useful high-level tool called 'virt-win-reg' (based on
hivex technology) which can be used to query specific registry keys in
an existing Windows VM.

For Perl bindings, see 'perl-hivex'.

For OCaml bindings, see 'ocaml-hivex-devel'.


%package devel
Summary:        Development tools and libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig


%description devel
%{name}-devel contains development tools and libraries
for %{name}.


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


%package -n perl-%{name}
Summary:       Perl bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description -n perl-%{name}
perl-%{name} contains Perl bindings for %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove unwanted libtool *.la file:
rm $RPM_BUILD_ROOT%{_libdir}/libhivex.la

# Remove unwanted Perl files:
find $RPM_BUILD_ROOT -name perllocal.pod -delete
find $RPM_BUILD_ROOT -name .packlist -delete
find $RPM_BUILD_ROOT -name '*.bs' -delete

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
%{_bindir}/hivexsh
%{_libdir}/libhivex.so.*
%{_mandir}/man1/hivexget.1*
%{_mandir}/man1/hivexml.1*
%{_mandir}/man1/hivexsh.1*


%files devel
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/libhivex.so
%{_mandir}/man3/hivex.3*
%{_includedir}/hivex.h
%{_libdir}/pkgconfig/hivex.pc


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


%files -n perl-%{name}
%defattr(-,root,root,-)
%{perl_vendorarch}/*
%{_mandir}/man3/Win::Hivex.3pm*


%changelog
* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-2
- New upstream version 1.2.0.
- This includes OCaml and Perl bindings, so add these as subpackages.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-3
- Missing Epoch in conflicts version fixed.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-2
- Add Conflicts libguestfs <= 1.0.84.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-1
- Initial Fedora RPM.
