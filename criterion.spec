# TODO:
# - system boxfort (when released): https://github.com/diacritic/BoxFort
# - system libcsptr (when some post-2017 release made): https://github.com/Snaipe/libcsptr
Summary:	A cross-platform C and C++ unit testing framework for the 21th century
Summary(pl.UTF-8):	Wieloplatformowy szkielet do testów jednostkowych dla C i C++ w XXI wieku
Name:		criterion
Version:	2.3.3
Release:	4
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/Snaipe/Criterion/releases
Source0:	https://github.com/Snaipe/Criterion/releases/download/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	0305dbb5e00f04fd65b22e9ad82ba952
Patch0:		%{name}-libdir.patch
URL:		https://github.com/Snaipe/Criterion
BuildRequires:	cmake >= 2.8.0
BuildRequires:	dyncall >= 1.0
BuildRequires:	nanomsg-devel >= 1.0.0
BuildRequires:	rpmbuild(macros) >= 1.605
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

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1

%build
install -d build
cd build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang Criterion

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig


%files -f Criterion.lang
%defattr(644,root,root,755)
%doc ChangeLog doc/*.txt
%attr(755,root,root) %{_libdir}/libcriterion.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcriterion.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcriterion.so
%{_includedir}/criterion
%{_pkgconfigdir}/criterion.pc
