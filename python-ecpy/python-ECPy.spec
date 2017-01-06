%global srcname ECPy
%global sum Pure Pyhton Elliptic Curve Library
%global desc ECPy (pronounced ekpy), is a pure python Elliptic Curve library \
providing ECDSA, EDDSA, ECSchnorr, Borromean signatures as well as Point \
operations.\
\
Docs: https://ubinity.github.com/ECPy

Name:     python-%{srcname}
Version:  0.8.1
Release:  0%{?dist}
Summary:  %{sum}

License:  ASL 2.0
URL:      https://github.com/ubinity/%{srcname}
Source0:  https://github.com/ubinity/%{srcname}/archive/v%{version}.tar.gz

BuildArch: noarch
BuildRequires: python2-devel python3-devel

%description
%{desc}


%package -n python2-%{srcname}
Summary: %{sum}
Requires: python2-future
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}


%package -n python3-%{srcname}
Summary: %{sum}
Requires: python3-future
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}


%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build
%py3_build


%install
%py2_install
%py3_install


%check
# Current tests try to contact PyPi and fail on Koji
#%%{__python2} setup.py test


%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/*


%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*


%changelog
* Fri Jan 6 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.8.1-0
- Initial packaging for Fedora
