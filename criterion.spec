# TODO:
# - system boxfort (when released): https://github.com/diacritic/BoxFort
# - system libcsptr (when some post-2017 release made): https://github.com/Snaipe/libcsptr
#
# Conditional build:
%bcond_without	tests		# build without tests
#
Summary:	A cross-platform C and C++ unit testing framework for the 21th century
Summary(pl.UTF-8):	Wieloplatformowy szkielet do testów jednostkowych dla C i C++ w XXI wieku
Name:		criterion
Version:	2.4.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/Snaipe/Criterion/releases
Source0:	https://github.com/Snaipe/Criterion/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	93e91812837a68524d76339409ed2008
Patch0:		x32.patch
URL:		https://github.com/Snaipe/Criterion
BuildRequires:	dyncall >= 1.0
BuildRequires:	libffi-devel
BuildRequires:	libgit2-devel
BuildRequires:	meson >= 0.51.0
BuildRequires:	nanomsg-devel >= 1.0.0
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define filterout_c -mbranch-protection=standard

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

%prep
%setup -q
%patch0 -p1

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
