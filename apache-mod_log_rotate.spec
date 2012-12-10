#Module-Specific definitions
%define mod_name mod_log_rotate
%define mod_conf A83_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Automatic in-process rotation of transfer log
Name:		apache-%{mod_name}
Version:	1.00
Release:	13
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

%description
Adds RotateLogs and supporting directives that allow logs to be rotated by the
server without having to pipe them through rotatelogs.

%prep

%setup -q -c -T -n %{mod_name}-%{version}

cp %{SOURCE0} %{mod_name}.c
cp %{SOURCE1} %{mod_conf}

%build
%{_bindir}/apxs -c %{mod_name}.c

%install

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

%files
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.00-13mdv2012.0
+ Revision: 772679
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.00-12
+ Revision: 678338
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.00-11mdv2011.0
+ Revision: 588023
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.00-10mdv2010.1
+ Revision: 516141
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.00-9mdv2010.0
+ Revision: 406610
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.00-8mdv2009.1
+ Revision: 325952
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.00-7mdv2009.0
+ Revision: 235021
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.00-6mdv2009.0
+ Revision: 215601
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1.00-5mdv2008.1
+ Revision: 181799
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.00-4mdv2008.0
+ Revision: 82609
- rebuild

* Fri Aug 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.00-3mdv2008.0
+ Revision: 61185
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.00-2mdv2007.1
+ Revision: 140713
- rebuild

* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.00-1mdv2007.1
+ Revision: 140529
- use the correct version
- bunzip the sources

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0-1mdv2007.1
+ Revision: 79455
- Import apache-mod_log_rotate

* Fri Aug 04 2006 Oden Eriksson <oeriksson@mandriva.com> 0-1mdv2007.0
- initial Mandriva package

