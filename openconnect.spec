Summary:	Client for Cisco's AnyConnect SSL VPN
Summary(pl.UTF-8):	Klient Cisco AnyConnect SSL VPN
Name:		openconnect
Version:	3.02
Release:	1
License:	LGPL v2
Group:		Applications
Source0:	ftp://ftp.infradead.org/pub/openconnect/%{name}-%{version}.tar.gz
# Source0-md5:	c12688474f432a6d590958cc1c1ff076
Patch0:		%{name}-Makefile.patch
URL:		http://www.infradead.org/openconnect.html
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
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcppflags} %{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install install-lib \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README.DTLS README.SecurID TODO
%attr(755,root,root) %{_bindir}/openconnect
%{_mandir}/man8/openconnect.8*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libopenconnect.a
%{_includedir}/openconnect.h
%{_pkgconfigdir}/openconnect.pc
