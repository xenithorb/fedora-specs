Name:       pacmanager
Version:    4.5.5.7
Release:    1%{?dist}
Summary:    Perl Auto Connector a multi-purpose SSH/terminal connection manager
License:    GPLv3
URL:        https://sites.google.com/site/davidtv/
Source0:    http://downloads.sourceforge.net/project/pacmanager/pac-4.0/pac-%{version}-all.tar.gz
Source100:  make_patch.sh
Patch0:     %{name}-%{version}-libdir.patch
BuildArch:  noarch
Requires:   perl vte ftp telnet perl-Gtk2-Unique perl-Gnome2-Vte
Requires:   perl-IO-Stty perl-Crypt-Blowfish perl-Crypt-Rijndael


%description
PAC is a telnet/ssh/rsh/etc connection manager/automator written in Perl GTK
aimed at making administration easier. Users who may have used SecureCRT,
PuTTY, and/or mRemoteNG in the past may find this application useful.


%prep
%autosetup -n pac -p1


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/{%{_mandir}/man1,%{_bindir},%{_datadir}/{%{name},applications}}
mkdir -p %{buildroot}/{%{_libdir}/%{name},%{_libexecdir}/%{name}}
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d

install -m 755 pac %{buildroot}/%{_bindir}/%{name}
install -m 755 utils/pac_from_mcm.pl %{buildroot}/%{_libexecdir}/%{name}
install -m 755 utils/pac_from_putty.pl %{buildroot}/%{_libexecdir}/%{name}
cp -a res/pac.desktop %{buildroot}/%{_datadir}/applications/%{name}.desktop
cp -a res/pac.1 %{buildroot}/%{_mandir}/man1/%{name}.1
cp -a res/*.{png,jpg,pl,glade} res/termcap %{buildroot}/%{_datadir}/%{name}
cp -a lib/* %{buildroot}/%{_libdir}/%{name}/
cp -a res/pac_bash_completion %{buildroot}/%{_sysconfdir}/bash_completion.d/%{name}
# Remove the Vte binaries(?) and require perl-Gnome2-Vte instead
rm -rf %{buildroot}/%{_libdir}/%{name}/ex/vte*


%files
%doc README LICENSE
%doc %{_mandir}/man1/%{name}*
%{_libdir}/*
%{_libexecdir}/*
%{_datadir}/*
%{_sysconfdir}/*
%{_bindir}/*


%changelog
* Wed Aug 31 2016 xenithorb <mike@mgoodwin.net>
- Initial packaging of pacmanager RPM
