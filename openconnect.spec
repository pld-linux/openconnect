#
# Conditional build:
%bcond_with	openssl		# OpenSSL instead of GnuTLS (incompatible with some versions)
%bcond_without	oath		# OATH-based one-time password authentication
%bcond_without	stoken		# Software Token authentication
%bcond_without	static_libs	# static library
#
Summary:	Client for Cisco's AnyConnect SSL VPN
Summary(pl.UTF-8):	Klient Cisco AnyConnect SSL VPN
Name:		openconnect
Version:	5.00
Release:	1
License:	LGPL v2.1
Group:		Applications/Networking
Source0:	ftp://ftp.infradead.org/pub/openconnect/%{name}-%{version}.tar.gz
# Source0-md5:	b3677a4b15f8c530615f4c42dadce275
Patch0:		%{name}-am.patch
Patch1:		%{name}-link.patch
URL:		http://www.infradead.org/openconnect.html
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
%{!?with_openssl:BuildRequires:	gnutls-devel >= 2.12.16}
BuildRequires:	libproxy-devel
BuildRequires:	libxml2-devel >= 2.0
%{?with_oath:BuildRequires:	oath-toolkit-devel}
%{?with_openssl:BuildRequires:	openssl-devel}
%{!?with_openssl:BuildRequires:	p11-kit-devel}
BuildRequires:	pkgconfig >= 1:0.27
%{?with_stoken:BuildRequires:	stoken-devel}
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
%{?with_openssl:Requires:	gnutls-devel >= 2.12.16}
Requires:	libproxy-devel
Requires:	libxml2-devel >= 2.0
%{?with_openssl:Requires:	openssl-devel}
%{!?with_openssl:Requires:	p11-kit-devel}
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
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	%{!?with_oath:--without-liboath} \
	%{!?with_stoken:--without-stoken} \
	--with-vpnc-script=/usr/bin/vpnc-script \
	%{?with_openssl:--without-gnutls}
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
%{_docdir}/openconnect

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libopenconnect.a
%endif
