Summary:	A cross-platform C and C++ unit testing framework for the 21th century
Name:		criterion
Version:	2.3.3
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://github.com/Snaipe/Criterion/releases/download/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	0305dbb5e00f04fd65b22e9ad82ba952
URL:		https://github.com/Snaipe/Criterion
BuildRequires:	cmake >= 2.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A dead-simple, yet extensible, C and C++ unit testing framework.

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

%build
install -d build
cd build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if "%{_lib}" != "lib"
	install -d $RPM_BUILD_ROOT%{_libdir}
	mv $RPM_BUILD_ROOT{%{_prefix}/lib/*,%{_libdir}}
%endif

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
%{_npkgconfigdir}/criterion.pc
