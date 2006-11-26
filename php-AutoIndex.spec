%define		_appname AutoIndex
Summary:	A Website Directory Indexer and File Manager (AutoIndex PHP Script)
Summary(pl):	Webowy indeks zawarto¶ci katagów i zarz±dca plików (AutoIndex PHP Script)
Name:		php-AutoIndex
Version:	2.2.0
Release:	0.2
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/autoindex/%{_appname}-%{version}.tar.gz
# Source0-md5:	1b3e545baa79218d261a3f64389b38f3
Source1:	%{name}.php
Patch0:		%{name}-config.patch
URL:		http://autoindex.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.221
Requires:	php-common >= 4:5.0.0
Requires:	webserver = apache
Requires:	webserver(php)
Obsoletes:	AutoIndex
Obsoletes:	php4-AutoIndex
Conflicts:	apache1 < 1.3.33-2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{_appname}
%define		_appdir		%{_datadir}/%{_appname}

%description
A Website Directory Indexer and File Manager (AutoIndex PHP Script).

%description -l pl
Webowy indeks zawarto¶ci katalogów i zarz±dca plików (AutoIndex PHP
Script).

%prep
%setup -q -n %{_appname}
%patch0 -p1
rm -f license.html # GPL

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}

cp -a *.php classes index_icons languages templates $RPM_BUILD_ROOT%{_appdir}
cp -a hidden_files $RPM_BUILD_ROOT%{_sysconfdir}

cat <<'EOF'> $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
Alias /AutoIndex %{_appdir}

<Directory %{_appdir}>
	<IfModule mod_access.c>
	order allow,deny
	allow from all
	</IfModule>
</Directory>
# vim: filetype=apache ts=4 sw=4 et
EOF

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{_appname}.conf.php

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<EOF
- To use AutoIndex in your website, call it from php script:
  require '%{_appdir}/index.php';
  and copy (or symlink) %{_sysconfdir}/%{_appname}.conf.php to the
  script dir.

- For opening config file generation screen, open URL:
  http://yoursite.example.org/AutoIndex/

EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%apache_config_install -v 1 -c %{_sysconfdir}/apache.conf

%triggerun -- apache1 < 1.3.37-3, apache1-base
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc *.html
%attr(751,root,http) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hidden_files
%{_appdir}
