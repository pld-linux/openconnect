#
# Conditional build:
%bcond_without	java		# JNI bindings
%bcond_without	kerberos5	# GSSAPI support
%bcond_with	openssl		# OpenSSL instead of GnuTLS (incompatible with some versions)
%bcond_without	oath		# OATH-based one-time password authentication
%bcond_without	pcsc		# Yutoken support via PCSC Lite
%bcond_without	stoken		# Software Token authentication
%bcond_without	static_libs	# static library
#

%{?with_java:%{?use_default_jdk}}

Summary:	Client for Cisco's AnyConnect SSL VPN and Pulse Connect Secure
Summary(pl.UTF-8):	Klient Cisco AnyConnect SSL VPN i Pulse Connect Secure
Name:		openconnect
Version:	9.12
Release:	1
License:	LGPL v2.1
Group:		Applications/Networking
Source0:	ftp://ftp.infradead.org/pub/openconnect/%{name}-%{version}.tar.gz
# Source0-md5:	39060dcb58ebfb261bb6faf17755b98b
Patch0:		%{name}-am.patch
Patch1:		missing-includes.patch
URL:		http://www.infradead.org/openconnect.html
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
%{!?with_openssl:BuildRequires:	gnutls-devel >= 3.6.13}
BuildRequires:	groff
%{?with_kerberos5:BuildRequires:	heimdal-devel}
%{?with_java:%buildrequires_jdk}
%{?with_openssl:BuildRequires:	libp11-devel >= 0.4.8}
BuildRequires:	libproxy-devel
%{!?with_openssl:BuildRequires:	libtasn1-devel}
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	lz4-devel >= 1:1.7
%{?with_oath:BuildRequires:	oath-toolkit-devel >= 2.2.0}
%{?with_openssl:BuildRequires:	openssl-devel}
BuildRequires:	p11-kit-devel
%{?with_pcsc:BuildRequires:	pcsc-lite-devel}
BuildRequires:	pkgconfig >= 1:0.27
BuildRequires:	python >= 2
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.021
%{?with_stoken:BuildRequires:	stoken-devel}
%{!?with_openssl:BuildRequires:	tpm2-tss-devel}
%{!?with_openssl:BuildRequires:	trousers-devel}
BuildRequires:	zlib-devel
%{!?with_openssl:Requires:	gnutls >= 3.6.13}
%{?with_oath:Requires:	oath-toolkit >= 2.2.0}
Suggests:	vpnc-script
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenConnect is a client for Cisco's AnyConnect SSL VPN and Pulse
Connect Secure.

%description -l pl.UTF-8
OpenConnect jest klientem Cisco AnyConnect SSL VPN i Pulse Connect
Secure.

%package devel
Summary:	Development files for OpenConnect library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki OpenConnect
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_openssl:Requires:	gnutls-devel >= 3.6.13}
Requires:	libproxy-devel
Requires:	libxml2-devel >= 2.0
%{?with_oath:Requires:	oath-toolkit-devel >= 2.2.0}
%{?with_openssl:Requires:	openssl-devel}
%{!?with_openssl:Requires:	p11-kit-devel}
%{?with_stoken:Requires:	stoken-devel}
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

%package -n java-openconnect
Summary:	JNI wrapper for OpenConnect library
Summary(pl.UTF-8):	Interfejs JNI do biblioteki OpenConnect
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description -n java-openconnect
JNI wrapper for OpenConnect library.

%description -n java-openconnect -l pl.UTF-8
Interfejs JNI do biblioteki OpenConnect.

%package -n bash-completion-openconnect
Summary:	Bash completion for openconnect arguments
Summary(pl.UTF-8):	Bashowe dopełnianie argumentów polecenia openconnect
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-openconnect
Bash completion for openconnect arguments.

%description -n bash-completion-openconnect -l pl.UTF-8
Bashowe dopełnianie argumentów polecenia openconnect.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{?with_java:export JAVA_HOME="%{java_home}"}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	%{!?with_kerberos5:--without-gssapi} \
	%{?with_java:--with-java} \
	%{!?with_pcsc:--without-libpcsclite} \
	%{!?with_oath:--without-libpskc} \
	%{!?with_stoken:--without-stoken} \
	--with-system-cafile=/etc/certs/ca-certificates.crt \
	--with-vpnc-script=/usr/bin/vpnc-script \
	%{?with_openssl:--without-gnutls}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libopenconnect.la
# JNI module
%if %{with java}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libopenconnect-wrapper.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libopenconnect-wrapper.a
%endif
%endif

# uses non-Linux /system/bin/sh
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/openconnect/hipreport-android.sh

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n java-openconnect -p /sbin/ldconfig
%postun	-n java-openconnect -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS TODO
%attr(755,root,root) %{_sbindir}/openconnect
%attr(755,root,root) %{_libdir}/libopenconnect.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenconnect.so.5
%dir %{_libexecdir}/openconnect
%attr(755,root,root) %{_libexecdir}/openconnect/csd-post.sh
%attr(755,root,root) %{_libexecdir}/openconnect/csd-wrapper.sh
%attr(755,root,root) %{_libexecdir}/openconnect/hipreport.sh
%attr(755,root,root) %{_libexecdir}/openconnect/tncc-emulate.py
%attr(755,root,root) %{_libexecdir}/openconnect/tncc-wrapper.py
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

%if %{with java}
%files -n java-openconnect
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenconnect-wrapper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenconnect-wrapper.so.0
%attr(755,root,root) %{_libdir}/libopenconnect-wrapper.so
%endif

%files -n bash-completion-openconnect
%defattr(644,root,root,755)
%{bash_compdir}/openconnect
