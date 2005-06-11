# TODO: 1. How to deal with generated via web AutoIndex.conf.php file? (now - manually ;)
#	2. Why %%apache_config_install macro doesn't restart (or reload)
#	apache when symlink is placed in /etc/httpd/httpd.conf/ directory?
#	(and package doesn't work after installation).
#	
Summary:	A Website Directory Indexer and File Manager (AutoIndex PHP Script)
Summary(pl):	Webowy indeks zawarto¶ci katagów i zarz±dca plików (AutoIndex PHP Script)
Name:		AutoIndex
Version:	2.1.0
Release:	0.1
License:	GPL
Group:		Applications/Networking
Source0:	http://kent.dl.sourceforge.net/sourceforge/autoindex/%{name}-%{version}.tar.gz
# Source0-md5:	f2fc376d4f40c7197d4d3ec036db649e
BuildRequires:	rpmbuild(macros) >= 1.221
Requires:	apache >= 1.3.33-2
Requires:	php > 5.0.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Website Directory Indexer and File Manager (AutoIndex PHP Script).

%description -l pl
Webowy indeks zawarto¶ci katalogów i zarz±dca plików (AutoIndex PHP
Script).

%define	_sysconfdir	/etc/%{name}
%define	_appdir		%{_datadir}/%{name}

%prep
%setup -q -n %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}

cp -a * $RPM_BUILD_ROOT%{_appdir}

echo "Alias /index %{_appdir}" > $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf
#%%: > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf.php
#ln -sf %{_sysconfdir}/%{name}.conf.php $RPM_BUILD_ROOT%{_appdir}/%{name}.conf.php

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%attr(750,root,http) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache-%{name}.conf
#%%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf.php
%{_appdir}
