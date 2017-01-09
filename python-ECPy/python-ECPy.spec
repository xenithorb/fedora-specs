%global srcname ECPy
%global owner ubinity
%global desc ECPy (pronounced ekpy), is a pure python Elliptic Curve library \
providing ECDSA, EDDSA, ECSchnorr, Borromean signatures as well as Point \
operations.

Name:     python-%{srcname}
Version:  0.8.1
Release:  1%{?dist}
Summary:  Python Elliptic Curve Library

License:  ASL 2.0
URL:      https://github.com/%{owner}/%{srcname}
Source0:  https://github.com/%{owner}/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch: noarch
BuildRequires: python2-devel python3-devel python3-sphinx

%description
%{desc}


%package -n python2-%{srcname}
Summary: %{summary}
Requires: python2-future
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}

%package -n python3-%{srcname}
Summary: %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%package doc
Summary: Documentation for python-%{srcname}

%description doc
This package contains the documentation for python-%{srcname}


%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build
%py3_build
%make_build -C doc singlehtml
rm -f doc/build/singlehtml/{.buildinfo,.nojekyll}


%install
%py2_install
%py3_install


%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/*

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%files doc
%license LICENSE
%doc doc/build/singlehtml/*


%changelog
* Mon Jan 9 2017 Michael Goodwin <xenithorb@fedoraproject.org> - 0.8.1-1
- Initial packaging for Fedora
