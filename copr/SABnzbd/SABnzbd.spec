#global sabrc             RC2

Name:       SABnzbd
Version:    2.0.0
Release:    1%{?dist}
Summary:    An Open Source Binary Newsreader written in Python
Group:      Applications/Internet
License:    GPLv2
URL:        http://sabnzbd.org/

Source0:    https://github.com/sabnzbd/sabnzbd/releases/download/%{version}/SABnzbd-%{version}-src.tar.gz
Source1:    SABnzbd.sh
Source2:    SABnzbd.desktop
Source3:    SABnzbd.initd
Source4:    SABnzbd.sysconfig
Source5:    SABnzbd@.service

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:    desktop-file-utils

Requires:    nc
Requires:    par2cmdline
Requires:    python-cheetah
Requires:    python-yenc
Requires:    python-cryptography
Requires:    unrar
Requires:    unzip
Requires:    wget

%define usesystemd 0

%if 0%{?fedora} >= 19
%define usesystemd 1
%endif

%if 0%{?rhel} >= 7
%define usesystemd 1
%endif

%if %{usesystemd} == 1
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
%else
Requires(post):    chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun):  initscripts
%endif


%description
SABnzbd makes Usenet as simple and streamlined as possible by automating
everything it can. All you have to do is add an .nzb. SABnzbd takes over
from there, where it will be automatically downloaded, verified, repaired,
extracted and filed away with zero human interaction.


%prep
%setup -q -n SABnzbd-%{version}%{?sabrc}


%build
sed -i "s|@DATADIR@|%{_datadir}|g" %{SOURCE1} %{SOURCE2} %{SOURCE3}


%install
rm -rf %{buildroot}

#SABnzbd
%{__install} -d -m0755  %{buildroot}%{_datadir}/SABnzbd
for dir in email interfaces locale po util tools sabnzbd cherrypy SABnzbd.py* icons gntp;do
%{__cp} -a %{_builddir}/SABnzbd-%{version}%{?sabrc}/$dir %{buildroot}%{_datadir}/SABnzbd
done

#start script
%{__install} -d -m0755 %{buildroot}%{_bindir}
%{__install} -D -m0755 %{SOURCE1} %{buildroot}%{_bindir}/SABnzbd

#desktop file
%{__install} -d -m0755 %{buildroot}%{_datadir}/applications
desktop-file-install --vendor fedora --dir %{buildroot}%{_datadir}/applications %{SOURCE2}

#init script
%if %{usesystemd} == 1
%{__install} -d -m0755 %{buildroot}%{_unitdir}
%{__install} -D -m0755 %{SOURCE5} %{buildroot}%{_unitdir}
%else
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/init.d
%{__install} -D -m0755 %{SOURCE3} %{buildroot}%{_sysconfdir}/init.d/SABnzbd
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -D -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/SABnzbd
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
#doc CHANGELOG.txt COPYRIGHT.txt GPL2.txt GPL3.txt INSTALL.txt ISSUES.txt README.txt Sample-PostProc.sh licenses/*
%doc COPYRIGHT.txt GPL2.txt GPL3.txt INSTALL.txt ISSUES.txt README.txt licenses/*
%{_bindir}/SABnzbd
%{_datadir}/SABnzbd
%{_datadir}/applications/fedora-SABnzbd.desktop
%if %{usesystemd} == 1
%{_unitdir}/SABnzbd@.service
%else
%{_sysconfdir}/init.d/SABnzbd
%config(noreplace) %{_sysconfdir}/sysconfig/SABnzbd
%endif


%post
%if %{usesystemd} == 1
%systemd_post SABnzbd@.service
%else
update-desktop-database &>/dev/null ||:
/sbin/chkconfig --add SABnzbd
%endif


%preun
%if %{usesystemd} == 1
%systemd_preun SABnzbd@.service
%else
if [ $1 = 0 ] ; then
    /sbin/service SABnzbd stop >/dev/null 2>&1
    /sbin/chkconfig --del SABnzbd
fi
%endif

%postun
%if %{usesystemd} == 1
%systemd_postun_with_restart SABnzbd@.service
%else
if [ "$1" -ge "1" ] ; then
    /sbin/service SABnzbd condrestart >/dev/null 2>&1 || :
fi
update-desktop-database &> /dev/null ||:
%endif


%changelog
