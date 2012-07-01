#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Client for Cisco's AnyConnect SSL VPN
Summary(pl.UTF-8):	Klient Cisco AnyConnect SSL VPN
Name:		openconnect
Version:	4.02
Release:	1
License:	LGPL v2.1
Group:		Applications/Networking
Source0:	ftp://ftp.infradead.org/pub/openconnect/%{name}-%{version}.tar.gz
# Source0-md5:	3743cbf10dbcfd0d28ba270528a2eef2
Patch0:		%{name}-am.patch
URL:		http://www.infradead.org/openconnect.html
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
BuildRequires:	libproxy-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Suggests:	vpnc-script
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenConnect is a client for Cisco's AnyConnect SSL VPN.

%description -l pl.UTF-8
OpenConnect jest klientem Cisco AnyConnect SSL VPN.

%package devel
Summary:	Development files for OpenConnect library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki OpenConnect
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libproxy-devel
Requires:	libxml2-devel >= 2.0
Requires:	openssl-devel
Requires:	zlib-devel

%description devel
Development files for OpenConnect library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki OpenConnect.

%package static
Summary:	Static OpenConnect library
Summary(pl.UTF-8):	Statyczna biblioteka OpenConnect
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenConnect library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenConnect.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-vpnc-script=/usr/bin/vpnc-script
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libopenconnect.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS TODO
%attr(755,root,root) %{_sbindir}/openconnect
%attr(755,root,root) %{_libdir}/libopenconnect.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenconnect.so.2
%{_mandir}/man8/openconnect.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenconnect.so
%{_includedir}/openconnect.h
%{_pkgconfigdir}/openconnect.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libopenconnect.a
%endif
