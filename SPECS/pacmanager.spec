Name:       pacmanager
Version:    4.5.5.7
Release:    2%{?dist}
Summary:    Perl Auto Connector a multi-purpose SSH/terminal connection manager
License:    GPLv3+
URL:        https://sites.google.com/site/davidtv/
Source0:    https://downloads.sourceforge.net/project/pacmanager/pac-4.0/pac-%{version}-all.tar.gz
BuildArch:  noarch
Requires:   perl vte ftp telnet perl-Gtk2-Unique perl-Gnome2-Vte
Requires:   perl-IO-Stty perl-Crypt-Blowfish perl-Crypt-Rijndael


%description
PAC is a telnet/ssh/rsh/etc connection manager/automator written in Perl GTK
aimed at making administration easier. Users who may have used SecureCRT,
PuTTY, and/or mRemoteNG in the past may find this application useful.


%prep
%autosetup -n pac -p1
find . -type f -exec sed -i \
  -e "s|\$RealBin[ ]*\.[ ]*'|'%{_datadir}/%{name}|g" \
  -e 's|"\$RealBin/|"%{_datadir}/%{name}/|g' \
  -e 's|/\.\.\(/\)|\1|' \
  '{}' \+
sed -ri '/^(Exec|Icon)=/{s|pac|%{name}|}' res/pac.desktop


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/{%{_mandir}/man1,%{_bindir}}
mkdir -p %{buildroot}/%{_datadir}/{%{name}/{lib,res},applications}
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/{24x24,64x64,256x256}/apps

install -m 755 pac %{buildroot}/%{_bindir}/%{name}
install -m 755 utils/pac_from_mcm.pl %{buildroot}/%{_bindir}/%{name}_from_mcm
install -m 755 utils/pac_from_putty.pl %{buildroot}/%{_bindir}/%{name}_from_putty

cp -a res/pac.desktop %{buildroot}/%{_datadir}/applications/%{name}.desktop
cp -a res/pac.1 %{buildroot}/%{_mandir}/man1/%{name}.1

# Copy the icons over to /usr/share/icons/
cp -a res/pac24x24.png %{buildroot}/%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
cp -a res/pac64x64.png %{buildroot}/%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
cp -a res/pac256x256.jpg %{buildroot}/%{_datadir}/icons/hicolor/256x256/apps/%{name}.jpg

# Copy the remaining resources and libraries
cp -a res/*.{png,jpg,pl,glade} res/termcap %{buildroot}/%{_datadir}/%{name}/res/
cp -a lib/* %{buildroot}/%{_datadir}/%{name}/lib/
cp -a res/pac_bash_completion %{buildroot}/%{_sysconfdir}/bash_completion.d/%{name}

# This seems necessary for the migration tools to work
pushd %{buildroot}/%{_datadir}/%{name}/lib
  ln -s ex/*.pm .
popd

# Remove the Vte binaries(?) and require perl-Gnome2-Vte instead
rm -rf %{buildroot}/%{_datadir}/%{name}/lib/ex/vte*


%files
%doc README LICENSE
%doc %{_mandir}/man1/%{name}*
%{_datadir}/*
%{_sysconfdir}/*
%{_bindir}/*

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%changelog
* Wed Aug 31 2016 Michael Goodwin <mike@mgoodwin.net> 4.5.5.7
- Initial packaging of pacmanager RPM
