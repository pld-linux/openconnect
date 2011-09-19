Summary:	Client for Cisco's AnyConnect SSL VPN
Summary(pl.UTF-8):	Klient Cisco AnyConnect SSL VPN
Name:		openconnect
Version:	3.12
Release:	1
License:	LGPL v2
Group:		Applications
Source0:	ftp://ftp.infradead.org/pub/openconnect/%{name}-%{version}.tar.gz
# Source0-md5:	2f4fceb3f921ca8deb3a7cbd19a5e008
URL:		http://www.infradead.org/openconnect.html
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
BuildRequires:	libproxy-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenConnect is a client for Cisco's AnyConnect SSL VPN.

%description -l pl.UTF-8
OpenConnect jest klientem Cisco AnyConnect SSL VPN.

%package devel
Summary:	Development files for OpenConnect
Summary(pl.UTF-8):	Pliki programistyczne dla OpenConnect
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libproxy-devel
Requires:	libxml2-devel
Requires:	openssl-devel
Requires:	zlib-devel

%description devel
Development files for OpenConnect.

%description devel -l pl.UTF-8
Pliki programistyczne dla OpenConnect.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make} \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcppflags} %{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS TODO
%attr(755,root,root) %{_bindir}/openconnect
%attr(755,root,root) %{_libdir}/libopenconnect.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenconnect.so.1
%{_mandir}/man8/openconnect.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenconnect.so
%{_includedir}/openconnect.h
%{_pkgconfigdir}/openconnect.pc
