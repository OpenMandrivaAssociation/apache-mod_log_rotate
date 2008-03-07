#Module-Specific definitions
%define mod_name mod_log_rotate
%define mod_conf A83_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Automatic in-process rotation of transfer log
Name:		apache-%{mod_name}
Version:	1.00
Release:	%mkrel 5
Group:		System/Servers
License:	Apache License
URL:		http://www.hexten.net/mod_log_rotate/
Source0:	http://www.hexten.net/assets/apache2/mod_log_rotate.c
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Adds RotateLogs and supporting directives that allow logs to be rotated by the
server without having to pipe them through rotatelogs.

%prep

%setup -q -c -T -n %{mod_name}-%{version}

cp %{SOURCE0} %{mod_name}.c
cp %{SOURCE1} %{mod_conf}

%build
%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


