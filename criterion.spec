# TODO:
# - system boxfort (when released): https://github.com/diacritic/BoxFort
# - system nanopb (0.4.7 bundled)
# - system libcsptr (when some post-2017 release made): https://github.com/Snaipe/libcsptr
#
# Conditional build:
%bcond_without	tests		# testing
%bcond_without	system_nanopb	# system nanopb
#
Summary:	A cross-platform C and C++ unit testing framework for the 21th century
Summary(pl.UTF-8):	Wieloplatformowy szkielet do testów jednostkowych dla C i C++ w XXI wieku
Name:		criterion
Version:	2.4.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/Snaipe/Criterion/releases
Source0:	https://github.com/Snaipe/Criterion/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	20affc64bb0d00953826eba4c93bf8ab
Patch0:		x32.patch
Patch1:		%{name}-shared-nanopb.patch
URL:		https://github.com/Snaipe/Criterion
BuildRequires:	dyncall >= 1.0
BuildRequires:	libffi-devel
BuildRequires:	libgit2-devel
BuildRequires:	meson >= 0.55.0
BuildRequires:	nanomsg-devel >= 1.0.0
%{?with_system_nanopb:BuildRequires:	nanopb-devel >= 0.4.7}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A dead-simple, yet extensible, C and C++ unit testing framework.

%description -l pl.UTF-8
Bardzo prosty, ale rozszerzalny szkielet testów jednostkowych dla C i
C++.

%package devel
Summary:	Header files for criterion library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki criterion
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for criterion library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki criterion.

%package static
Summary:	Static criterion libraries
Summary(pl.UTF-8):	Statyczne biblioteki criterion
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static criterion libraries.

%description static -l pl.UTF-8
Statyczne biblioteki criterion.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%if %{without system_nanopb}
%{__sed} -i -e '/dependency.*nanopb/ s/nanopb::protobuf-nanopb/notfound::protobuf-nanopb/' meson.build
%endif

%build
%meson build \
	-Dtests=%{__true_false tests}

%ninja_build -C build

%{?with_tests:%ninja_test -C build}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang criterion

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f criterion.lang
%defattr(644,root,root,755)
%doc ChangeLog doc/*.txt
%attr(755,root,root) %{_libdir}/libcriterion.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcriterion.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcriterion.so
%{_includedir}/criterion
%{_pkgconfigdir}/criterion.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcriterion.a
%if %{without system_nanopb}
%{_libdir}/libprotobuf_nanopb_static.a
%endif
