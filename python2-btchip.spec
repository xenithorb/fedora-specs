%global srcname btchip-python

# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?__python2: %global __python2 %__python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}


Name:     python2-btchip
Version:  0.1.18
Release:  1%{?dist}
Summary:  Python communication library for Ledger Hardware Wallet products

License:  ASL 2.0
URL:      https://github.com/LedgerHQ/%{srcname}
Source0:  https://github.com/LedgerHQ/%{srcname}/archive/v%{version}.tar.gz

BuildArch:     noarch
BuildRequires: python2 python2-devel python-setuptools
#BuildRequires: libusbx-devel hidapi

Requires: python2 python2-hidapi
Requires: hidapi >= 0.7.99

%{?python_provide: %python_provide python2-%{srcname}}

%description
%{srcname} is a python API for communicating primarily with the Ledger HW.1
hardware bitcoin wallet. This library is also adds compatibility to Electrum in
order to use the "Nano", "Nano S", and other Ledger-based hardware wallets.


%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build


%install
rm -rf $RPM_BUILD_ROOT
%py2_install


%check
#%%{__python2} setup.py test


%files
%license LICENSE
%doc README.md
# For noarch packages: sitelib
%{python2_sitelib}/*


%changelog
* Sun Jan  1 2017 Michael Goodwin <mike@mgoodwin.net> - 0.1.18-1
- Initial packaging of btchip-python for Fedora
