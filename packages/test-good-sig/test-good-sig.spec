%global debug_package %{nil}

Name:           test-good-sig
Version:        0.1.0
Release:        1%{?dist}
Summary:        Hello, World! in C language

License:        None
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
%{summary}

%prep
%autosetup

%build
CFLAGS="$RPM_OPT_FLAGS -Wl,-z,lazy"
export CFLAGS
%make_build

%install
%make_install

%files
%{_bindir}/%{name}

%changelog
* Wed Feb 28 2018 Martin Sehnoutka <msehnout@users.noreply.github.com>
 - New package
- 
