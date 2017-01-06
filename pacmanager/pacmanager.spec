%define _bashcompletiondir %(pkg-config --variable=completionsdir bash-completion)

Name:       pacmanager
Version:    4.5.5.7
Release:    7%{?dist}
Summary:    Perl Auto Connector a multi-purpose SSH/terminal connection manager
License:    GPLv3+
URL:        https://sites.google.com/site/davidtv/
Source0:    https://downloads.sourceforge.net/project/pacmanager/pac-4.0/pac-%{version}-all.tar.gz
BuildArch:  noarch
Requires:   perl-Gtk2-Unique perl-Gtk2-Ex-Simple-List perl-Gtk2-GladeXML perl-Gtk2
Requires:   perl-Gnome2-Vte perl-Gnome2-GConf
Requires:   perl-Crypt-Blowfish perl-Crypt-Rijndael perl-Crypt-CBC
Requires:   perl-YAML uuid-perl perl-Expect perl-IO-Stty perl-IO-Tty
Requires:   perl-Net-Ping perl-Net-ARP perl-Digest-SHA1 perl-Digest-SHA
Requires:   perl-Carp perl-Encode perl-Exporter perl-Socket
Requires:   perl-Socket6 perl-Storable perl-Time-HiRes perl-constant
Requires:   perl vte ftp telnet bash
BuildRequires: pkgconfig(bash-completion)
BuildRequires: desktop-file-utils


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
sed -ri -e '/^(Exec|Icon)=/{s|pac|%{name}|}' \
        -e 's|(^Categories=).*|\1GTK;Network;|' \
        -e 's|(^Actions=.*;)|\1Tray;|' res/pac.desktop
sed -ri 's|([\t_ ]*)pac([ ]*)|\1%{name}\2|g' res/pac_bash_completion
cat <<EOF >> res/pac.desktop
[Desktop Action Tray]
Name=Start %{name} in system tray
Exec=%{name} --iconified
EOF
cat res/pac.desktop

%build


%check
desktop-file-validate res/pac.desktop


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/{%{_mandir}/man1,%{_bindir}}
mkdir -p %{buildroot}/%{_datadir}/{%{name}/{lib,res},applications}
mkdir -p %{buildroot}/%{_bashcompletiondir}
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/{24x24,64x64}/apps

install -m 755 pac %{buildroot}/%{_bindir}/%{name}
install -m 755 utils/pac_from_mcm.pl %{buildroot}/%{_bindir}/%{name}_from_mcm
install -m 755 utils/pac_from_putty.pl %{buildroot}/%{_bindir}/%{name}_from_putty

cp -a res/pac.desktop %{buildroot}/%{_datadir}/applications/%{name}.desktop
cp -a res/pac.1 %{buildroot}/%{_mandir}/man1/%{name}.1
cp -a res/pac_bash_completion %{buildroot}/%{_bashcompletiondir}/%{name}

# Copy the icons over to /usr/share/icons/
cp -a res/pac24x24.png %{buildroot}/%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
cp -a res/pac64x64.png %{buildroot}/%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

# Copy the remaining resources and libraries
cp -a res/*.{png,jpg,pl,glade} res/termcap %{buildroot}/%{_datadir}/%{name}/res/
cp -a lib/* %{buildroot}/%{_datadir}/%{name}/lib/

# This seems necessary for the migration tools to work
pushd %{buildroot}/%{_datadir}/%{name}/lib
  ln -s ex/*.pm .
popd

# Remove the Vte binaries(?) and require perl-Gnome2-Vte instead
rm -rf %{buildroot}/%{_datadir}/%{name}/lib/ex/vte*


%files
%doc README
%license LICENSE
%{_mandir}/man1/%{name}*
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_bashcompletiondir}/%{name}*
%{_bindir}/%{name}*


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
* Mon Dec 26 2016 Michael Goodwin <mike@mgoodwin.net> 4.5.5.7-7
- Remove perl-libs as explicit dependency

* Mon Dec 26 2016 Michael Goodwin <mike@mgoodwin.net> 4.5.5.7-5
- Add missing dependencies

* Wed Sep 28 2016 Michael Goodwin <mike@mgoodwin.net> 4.5.5.7-4
- Post-acceptance SPEC updates
    https://bugzilla.redhat.com/show_bug.cgi?id=1372123#c5

* Wed Aug 31 2016 Michael Goodwin <mike@mgoodwin.net> 4.5.5.7
- Initial packaging of pacmanager RPM
