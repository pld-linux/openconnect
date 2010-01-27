Summary:	Client for Cisco's AnyConnect SSL VPN
Name:		openconnect
Version:	2.21
Release:	1
License:	LGPL v2
Group:		Applications
Source0:	ftp://ftp.infradead.org/pub/openconnect/%{name}-%{version}.tar.gz
# Source0-md5:	4aeac75e3b58075ae0ed55e4c4c02864
Patch0:		%{name}-Makefile.patch
URL:		http://www.infradead.org/openconnect.html
BuildRequires:	GConf2-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenConnect is a client for Cisco's AnyConnect SSL VPN.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man8

%{__make} install \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

install openconnect.8 $RPM_BUILD_ROOT%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README.DTLS README.SecurID TODO
%attr(755,root,root) %{_bindir}/openconnect
%attr(755,root,root) %{_libdir}/nm-openconnect-auth-dialog
%{_mandir}/man8/openconnect.8*
