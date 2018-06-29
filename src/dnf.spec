%global hawkey_version 0.10.1
%global librepo_version 1.7.19
%global libcomps_version 0.1.8
%global rpm_version 4.13.0-0.rc1.29
%global min_plugins_core 2.1.3
%global dnf_langpacks_ver 0.15.1-6

%global confdir %{_sysconfdir}/%{name}

%global pluginconfpath %{confdir}/plugins

## What Python subpackages to build
# Note that --without python2 will fail to build manpages
# so it's currently unsupported
# Also double check the results if you build with different combos
#
# %%dnf_python selects what dnf requires and what /usr/bin/dnf runs on
# The build has to be enabled, i.e. you cannot build --without python3
# and set dnf_python to python3 at the same time
# It should be one of: python2, python3, platform-python (with dash!)
%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_without python2
%bcond_with python3
%bcond_with platform_python
%global dnf_python python2
%else
%bcond_without python2
%bcond_without python3
%bcond_without platform_python
%if 0%{?_module_build}
%global dnf_python platform-python
%else
%global dnf_python python3
%endif
%endif

%if %{with python2}
%global py2pluginpath %{python2_sitelib}/%{name}-plugins
%endif

%if %{with python3}
%global py3pluginpath %{python3_sitelib}/%{name}-plugins
%endif

%if %{with platform_python}
%global platpypluginpath %{platform_python_sitelib}/%{name}-plugins
%endif

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

Name:           dnf
Version:        2.7.5
Release:        2%{?dist}
Summary:        Package manager forked from Yum, using libsolv as a dependency resolver
# For a breakdown of the licensing, see PACKAGE-LICENSING
License:        GPLv2+ and GPLv2 and GPL
URL:            https://github.com/rpm-software-management/dnf
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         0001-Allow-to-set-cacheonly-from-commands-and-conf-RhBug-.patch
Patch1:         0002-Remove-redundant-conf-option-cacheonly.patch
Patch2:         0003-Remove-unnecessary-code-for-set-cacheonly.patch
BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gettext
# Documentation
BuildRequires:  %{_bindir}/sphinx-build
BuildRequires:  systemd
BuildRequires:  bash-completion

Requires:       %{dnf_python}-%{name} = %{version}-%{release}

%if 0%{?rhel} && 0%{?rhel} <= 7
Requires:       python-dbus
%else
#if %%{with platform_python}
# TODO: use rich deps once it is allowed
# platform-python-dbus doesn't exist
#Requires:       (platform-python-dbus if NetworkManager)
#else
%if %{with python3}
#Recommends:     (python3-dbus if NetworkManager)
Recommends:     python3-dbus
%else
#Recommends:     (python2-dbus if NetworkManager)
Recommends:     python2-dbus
%endif
#endif
%endif

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
Provides:       dnf-command(autoremove)
Provides:       dnf-command(check-update)
Provides:       dnf-command(clean)
Provides:       dnf-command(distro-sync)
Provides:       dnf-command(downgrade)
Provides:       dnf-command(group)
Provides:       dnf-command(history)
Provides:       dnf-command(info)
Provides:       dnf-command(install)
Provides:       dnf-command(list)
Provides:       dnf-command(makecache)
Provides:       dnf-command(mark)
Provides:       dnf-command(provides)
Provides:       dnf-command(reinstall)
Provides:       dnf-command(remove)
Provides:       dnf-command(repolist)
Provides:       dnf-command(repoquery)
Provides:       dnf-command(repository-packages)
Provides:       dnf-command(search)
Provides:       dnf-command(updateinfo)
Provides:       dnf-command(upgrade)
Provides:       dnf-command(upgrade-to)
Conflicts:      python2-dnf-plugins-core < %{min_plugins_core}
Conflicts:      python3-dnf-plugins-core < %{min_plugins_core}

# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      dnf-langpacks < %{dnf_langpacks_ver}

%description
Package manager forked from Yum, using libsolv as a dependency resolver.

%package conf
Summary:        Configuration files for DNF
Requires:       libreport-filesystem
# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      dnf-langpacks-conf < %{dnf_langpacks_ver}

%description conf
Configuration files for DNF.

%if 0%{?rhel} && 0%{?rhel} <= 7
%package -n yum4
Requires:       %{name} = %{version}-%{release}
Summary:        As a Yum CLI compatibility layer, supplies /usr/bin/yum4 redirecting to DNF

%description -n yum4
As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF.

%else
%package yum
Conflicts:      yum < 3.4.3-505
Requires:       %{name} = %{version}-%{release}
Summary:        As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF

%description yum
As a Yum CLI compatibility layer, supplies /usr/bin/yum redirecting to DNF.
%endif

%if %{with python2}
%package -n python2-%{name}
Summary:        Python 2 interface to DNF
%{?python_provide:%python_provide python2-%{name}}
BuildRequires:  python2-devel
BuildRequires:  python2-hawkey >= %{hawkey_version}
BuildRequires:  python-iniparse
BuildRequires:  python-libcomps >= %{libcomps_version}
BuildRequires:  python-librepo >= %{librepo_version}
BuildRequires:  python-nose
BuildRequires:  python2-gpg
Requires:       python2-gpg
BuildRequires:  pyliblzma
Requires:       pyliblzma
Requires:       %{name}-conf = %{version}-%{release}
Requires:       deltarpm
Requires:       python2-hawkey >= %{hawkey_version}
Requires:       python-iniparse
Requires:       python-libcomps >= %{libcomps_version}
Requires:       python-librepo >= %{librepo_version}
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  rpm-python >= %{rpm_version}
Requires:       rpm-python >= %{rpm_version}
Requires:       rpm-plugin-systemd-inhibit
%else
BuildRequires:  python2-rpm >= %{rpm_version}
Requires:       python2-rpm >= %{rpm_version}
Recommends:     rpm-plugin-systemd-inhibit
%endif
# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      python-dnf-langpacks < %{dnf_langpacks_ver}

%description -n python2-%{name}
Python 2 interface to DNF.
%endif

%if %{with python3}
%package -n python3-%{name}
Summary:        Python 3 interface to DNF.
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-devel
BuildRequires:  python3-hawkey >= %{hawkey_version}
BuildRequires:  python3-iniparse
BuildRequires:  python3-libcomps >= %{libcomps_version}
BuildRequires:  python3-librepo >= %{librepo_version}
BuildRequires:  python3-nose
BuildRequires:  python3-gpg
Requires:       python3-gpg
Requires:       %{name}-conf = %{version}-%{release}
Requires:       deltarpm
Requires:       python3-hawkey >= %{hawkey_version}
Requires:       python3-iniparse
Requires:       python3-libcomps >= %{libcomps_version}
Requires:       python3-librepo >= %{librepo_version}
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  rpm-python3 >= %{rpm_version}
Requires:       rpm-python3 >= %{rpm_version}
Requires:       rpm-plugin-systemd-inhibit
%else
BuildRequires:  python3-rpm >= %{rpm_version}
Requires:       python3-rpm >= %{rpm_version}
Recommends:     rpm-plugin-systemd-inhibit
%endif
# dnf-langpacks package is retired in F25
# to have clean upgrade path for dnf-langpacks
Obsoletes:      python3-dnf-langpacks < %{dnf_langpacks_ver}

%description -n python3-%{name}
Python 3 interface to DNF.
%endif

%if %{with platform_python}
%package -n platform-python-%{name}
Summary:        Python 3 interface to DNF.
BuildRequires:  platform-python-devel
BuildRequires:  platform-python-hawkey >= %{hawkey_version}
BuildRequires:  platform-python-iniparse
BuildRequires:  platform-python-libcomps >= %{libcomps_version}
BuildRequires:  platform-python-librepo >= %{librepo_version}
BuildRequires:  platform-python-nose
BuildRequires:  platform-python-gpg
Requires:       platform-python-gpg
BuildRequires:  platform-python-rpm >= %{rpm_version}
Requires:       %{name}-conf = %{version}-%{release}
Requires:       deltarpm
Requires:       platform-python-hawkey >= %{hawkey_version}
Requires:       platform-python-iniparse
Requires:       platform-python-libcomps >= %{libcomps_version}
Requires:       platform-python-librepo >= %{librepo_version}
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires:       rpm-plugin-systemd-inhibit
%else
Recommends:     rpm-plugin-systemd-inhibit
%endif
Requires:       platform-python-rpm >= %{rpm_version}

%description -n platform-python-%{name}
Platform Python interface to DNF.
%endif

%package automatic
Summary:        Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.
BuildRequires:  systemd
Requires:       %{name} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description automatic
Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.

%prep
%autosetup -p1
%if %{with python2}
mkdir build-py2
%endif

%if %{with python3}
mkdir build-py3
%endif

%if %{with platform_python}
mkdir build-platform_py
%endif

%build
%if %{with python2}
pushd build-py2
  %cmake ..
  %make_build
  make doc-man
popd
%endif

%if %{with python3}
pushd build-py3
  %cmake .. -DPYTHON_DESIRED:str=3 -DWITH_MAN=0
  %make_build
popd
%endif

%if %{with platform_python}
pushd build-platform_py
  %cmake ..  -DPYTHON_DESIRED:str=3 -DPYTHON_EXECUTABLE:FILEPATH=%{__platform_python} -DWITH_MAN=0
  %make_build
popd
%endif

%install
%if %{with python2}
pushd build-py2
  %make_install
popd
%endif

%if %{with python3}
pushd build-py3
  %make_install
popd
%endif

%if %{with platform_python}
pushd build-platform_py
  %make_install
popd
%endif

%find_lang %{name}

mkdir -p %{buildroot}%{pluginconfpath}/

%if %{with python2}
mkdir -p %{buildroot}%{py2pluginpath}/
%endif

%if %{with python3}
mkdir -p %{buildroot}%{py3pluginpath}/__pycache__/
%endif

%if %{with platform_python}
mkdir -p %{buildroot}%{platpypluginpath}/__pycache__/
%endif

mkdir -p %{buildroot}%{_localstatedir}/log/
mkdir -p %{buildroot}%{_var}/cache/dnf/
touch %{buildroot}%{_localstatedir}/log/%{name}.log



%if %{with platform_python}
cp %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf-pp
cp %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic-pp
sed -i 's|#!%{__python3}|#!%{__platform_python}|' %{buildroot}%{_bindir}/dnf{,-automatic}-pp
%if %{without python3}
rm %{buildroot}%{_bindir}/*-3
%endif
%endif

%if %{with python3}
sed -i 's|#!%{__platform_python}|#!%{__python3}|' %{buildroot}%{_bindir}/dnf{,-automatic}-3
%endif

%if %{with python2}
%if 0%{?rhel} && 0%{?rhel} <= 7
ln -sr  %{buildroot}%{_bindir}/dnf-2 %{buildroot}%{_bindir}/yum4
ln -sr  %{buildroot}%{_mandir}/man8/dnf.8.gz %{buildroot}%{_mandir}/man8/yum4.8.gz
rm -f %{buildroot}%{_mandir}/man8/yum.8.gz
%endif
sed -i 's|#!/usr/bin/python|#!%{__python2}|' %{buildroot}%{_bindir}/*-2
%endif

ln -sr  %{buildroot}%{_bindir}/dnf %{buildroot}%{_bindir}/yum

%if "%{dnf_python}" == "python3"
ln -sr  %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv -f  %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
%else
%if "%{dnf_python}" == "python2"
ln -sr  %{buildroot}%{_bindir}/dnf-2 %{buildroot}%{_bindir}/dnf
mv -f %{buildroot}%{_bindir}/dnf-automatic-2 %{buildroot}%{_bindir}/dnf-automatic
%else
ln -sr  %{buildroot}%{_bindir}/dnf-pp %{buildroot}%{_bindir}/dnf
mv -f  %{buildroot}%{_bindir}/dnf-automatic-pp %{buildroot}%{_bindir}/dnf-automatic
%endif
%endif
rm %{buildroot}%{_bindir}/dnf-automatic-*


%check
%if %{with python2}
pushd build-py2
  ctest -VV
popd
%endif

%if %{with python3}
pushd build-py3
  ctest -VV
popd
%endif

%if %{with platform_python}
pushd build-platform_py
  ctest -VV
popd
%endif

%post
%systemd_post dnf-makecache.timer

%preun
%systemd_preun dnf-makecache.timer

%postun
%systemd_postun_with_restart dnf-makecache.timer

%post automatic
%systemd_post dnf-automatic.timer
%systemd_post dnf-automatic-notifyonly.timer
%systemd_post dnf-automatic-download.timer
%systemd_post dnf-automatic-install.timer

%preun automatic
%systemd_preun dnf-automatic.timer
%systemd_preun dnf-automatic-notifyonly.timer
%systemd_preun dnf-automatic-download.timer
%systemd_preun dnf-automatic-install.timer

%postun automatic
%systemd_postun_with_restart dnf-automatic.timer
%systemd_postun_with_restart dnf-automatic-notifyonly.timer
%systemd_postun_with_restart dnf-automatic-download.timer
%systemd_postun_with_restart dnf-automatic-install.timer

%files -f %{name}.lang
%{_bindir}/%{name}
%if 0%{?rhel} && 0%{?rhel} <= 7
%{_sysconfdir}/bash_completion.d/%{name}
%else
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}
%endif
%{_mandir}/man8/%{name}.8*
%{_mandir}/man8/yum2dnf.8*
%{_unitdir}/%{name}-makecache.service
%{_unitdir}/%{name}-makecache.timer
%{_var}/cache/%{name}/

%files conf
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%dir %{confdir}
%dir %{pluginconfpath}
%dir %{confdir}/protected.d
%config(noreplace) %{confdir}/%{name}.conf
%config(noreplace) %{confdir}/protected.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%ghost %{_localstatedir}/log/hawkey.log
%ghost %{_localstatedir}/log/%{name}.log
%ghost %{_localstatedir}/log/%{name}.librepo.log
%ghost %{_localstatedir}/log/%{name}.rpm.log
%ghost %{_localstatedir}/log/%{name}.plugin.log
%ghost %{_sharedstatedir}/%{name}
%ghost %{_sharedstatedir}/%{name}/groups.json
%ghost %{_sharedstatedir}/%{name}/yumdb
%ghost %{_sharedstatedir}/%{name}/history
%{_mandir}/man5/%{name}.conf.5*
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/libreport/events.d/collect_dnf.conf

%if 0%{?rhel} && 0%{?rhel} <= 7
%files -n yum4
%{_bindir}/yum4
%{_mandir}/man8/yum4.8*
%exclude %{_mandir}/man8/yum.8*

%else
%files yum
%{_bindir}/yum
%{_mandir}/man8/yum.8*
%endif

%if %{with python2}
%files -n python2-%{name}
%{_bindir}/%{name}-2
%exclude %{python2_sitelib}/%{name}/automatic
%{python2_sitelib}/%{name}/
%dir %{py2pluginpath}
%endif

%if %{with python3}
%files -n python3-%{name}
%{_bindir}/%{name}-3
%exclude %{python3_sitelib}/%{name}/automatic
%{python3_sitelib}/%{name}/
%dir %{py3pluginpath}
%dir %{py3pluginpath}/__pycache__
%endif

%if %{with platform_python}
%files -n platform-python-%{name}
%{_bindir}/%{name}-pp
%exclude %{platform_python_sitelib}/%{name}/automatic
%{platform_python_sitelib}/%{name}/
%dir %{platpypluginpath}
%dir %{platpypluginpath}/__pycache__
%endif

%files automatic
%{_bindir}/%{name}-automatic
%config(noreplace) %{confdir}/automatic.conf
%{_mandir}/man8/%{name}.automatic.8*
%{_unitdir}/%{name}-automatic.service
%{_unitdir}/%{name}-automatic.timer
%{_unitdir}/%{name}-automatic-notifyonly.service
%{_unitdir}/%{name}-automatic-notifyonly.timer
%{_unitdir}/%{name}-automatic-download.service
%{_unitdir}/%{name}-automatic-download.timer
%{_unitdir}/%{name}-automatic-install.service
%{_unitdir}/%{name}-automatic-install.timer


%if "%{dnf_python}" == "python3"
%{python3_sitelib}/%{name}/automatic/
%else
%if "%{dnf_python}" == "python2"
%{python2_sitelib}/%{name}/automatic/
%else
%{platform_python_sitelib}/%{name}/automatic/
%endif
%endif

%changelog
* Wed Nov 29 2017 Jaroslav Mracek <jmracek@redhat.com> - 2.7.5-2
- Fix problem with demands.cacheonly that caused problems for system-upgrade

* Wed Oct 18 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.7.5-1
- Improve performance for excludes and includes handling (RHBZ #1500361)
- Fixed problem of handling checksums for local repositories (RHBZ #1502106)
- Fix traceback when using dnf.Base.close() (RHBZ #1503575)

* Mon Oct 16 2017 Jaroslav Mracek <jmracek@redhat.com> - 2.7.4-1
- Update to 2.7.4-1
- Enhanced performance for excludes and includes handling
- Solved memory leaks at time of closing of dnf.Base()
- Resolves: rhbz#1480979 - I thought it abnormal that dnf crashed.
- Resolves: rhbz#1461423 - Memory leak in python-dnf
- Resolves: rhbz#1499564 - dnf list installed crashes
- Resolves: rhbz#1499534 - dnf-2 is much slower than dnf-1 when handling groups
- Resolves: rhbz#1499623 - Mishandling stderr vs stdout (dnf search, dnf repoquery)

* Fri Oct 06 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.7.3-1
- Fix URL detection (RHBZ #1472847)
- Do not remove downloaded files with --destdir option (RHBZ #1498426)
- Fix handling of conditional packages in comps (RHBZ #1427144)

* Mon Oct 02 2017 Jaroslav Mracek <jmracek@redhat.com> - 2.7.2-1
- Update to 2.7.2-1
- Added new option ``--comment=<comment>`` that adds a comment to transaction in history
- :meth:`dnf.Base.pre_configure_plugin` configure plugins by running their pre_configure() method
- Added pre_configure() methotd for plugins and commands to configure dnf before repos are loaded
- Resolves: rhbz#1421478 - dnf repository-packages: error: unrecognized arguments: -x rust-rpm-macros
- Resolves: rhbz#1491560 - 'dnf check' reports spurious "has missing requires of" errors
- Resolves: rhbz#1465292 - DNF remove protected duplicate package
- Resolves: rhbz#1279001 - [RFE] Missing dnf --downloaddir option
- Resolves: rhbz#1212341 - [RFE] Allow plugins to override the core configuration
- Resolves: rhbz#1299482 - mock --init fails with message "Failed calculating RPMDB checksum"
- Resolves: rhbz#1488398 - dnf upstream tests failures on f26
- Resolves: rhbz#1192811 - dnf whatprovides should show which provides matched a pattern
- Resolves: rhbz#1288845 - "dnf provides" wildcard matching is unreliable (not all packages with matches listed)
- Resolves: rhbz#1473933 - [abrt] dnf-automatic: resolved(): rpm_conf.py:58:resolved:AttributeError: 'Rpmconf' object has no attribute '_interactive'
- Resolves: rhbz#1237349 - dnf autoremove not removing what dnf list extras shows
- Resolves: rhbz#1470050 - the 'priority=' option in /etc/yum.repos.d/*.repo is not respected
- Resolves: rhbz#1347927 - dnf --cacheonly downloads packages
- Resolves: rhbz#1478115 - [abrt] dnf: _hcmd_undo(): __init__.py:888:_hcmd_undo:IndexError: list index out of range
- Resolves: rhbz#1461171 -  RFE: support --advisory= with install
- Resolves: rhbz#1448874 - "dnf needs-restarting" vanished from bash completion
- Resolves: rhbz#1495116 - Dnf version fails with traceback in container

* Tue Sep 26 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.6.3-13
- Don't use rich deps for now

* Fri Sep 22 2017 Jaroslav Mracek <jmracek@redhat.com> - 2.6.3-12
- Added support for command pre_configuration

* Wed Sep 13 2017 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.6.3-11
- Added patch to obey repository priority configuration

* Wed Sep 13 2017 Jaroslav Mracek <jmracek@redhat.com> - 2.6.3-10
- Added patch to add services for dnf-automatic that were previously removed

* Tue Aug 22 2017 Miro Hrončok <mhroncok@redhat.com> - 2.6.3-4
- Add %%dnf_python macro that selects what dnf runs on
- Enable platform_python once again, but set %%dnf_python to python3

* Mon Aug 21 2017 Tomas Orsava <torsava@redhat.com> - 2.6.3-3
- Rebuilt without platform-python to revert the switch of /usr/bin/dnf to
  platform-python in standard Fedora

* Fri Aug 11 2017 Miro Hrončok <mhroncok@redhat.com> - 2.6.3-2
- Add platform-python subpackage
- Remove system_python macros
- Switch /usr/bin/dnf to use platform-python

* Mon Aug 07 2017 Jaroslav Mracek <jmracek@redhat.com> 2.6.3-1
- Fix problem with dnf.Package().remote_location() (RhBug:1476215) (Jaroslav
  Mracek)
- Change behavior of -C according to documentation (RhBug:1473964) (Jaroslav
  Mracek)
- It should prevent to ask attribute of None (RhBug:1359482) (Jaroslav Mracek)
- Solve a problems with --arch options (RhBug:1476834) (Jaroslav Mracek)
- Use security plugin code for dnf-automatic (Jaroslav Mracek)
- Fix unicode error for python2 (Jaroslav Mracek)
- Inform about packages installed for group (Jaroslav Mracek)
- Provide info if pkg is removed due to dependency (RhBug:1244755) (Jaroslav
  Mracek)
- Unify format of %%{_mandir} paths in dnf.spec (Jaroslav Mracek)
- Remove test_yumlayer.py as unneeded test (Jaroslav Mracek)
- Provide yum4 package for rhel7 build (Jaroslav Mracek)
- Make yum compatible layer very minimal (RhBug:1476748) (Jaroslav Mracek)
- Remove metadata_expire from yum compatible layer (Jaroslav Mracek)
- Remove keepcache from yum compatibility layer (Jaroslav Mracek)
- Remove options from yum conf (Jaroslav Mracek)
- Remove unused functionality from  yum compatible layer (Jaroslav Mracek)
- Add deplist command for dnf (Jaroslav Mracek)
- Fix problems with --downloaddir options (RhBug:1476464) (Jaroslav Mracek)
- Move description of --forcearch into proper place (Jaroslav Mracek)
- Provide description of --downloaddir option (Jaroslav Mracek)
- Fix if in spec file (Jaroslav Mracek)
- Add description of "test" tsflags (Jaroslav Mracek)
- Enable import gpg_keys with tsflag test (RhBug:1464192) (Jaroslav Mracek)
- Keep old reason when undoing erase (RhBug:1463107) (Eduard Čuba)
- spec: eliminate other weak dependencies for el<=7 (Igor Gnatenko)
- spec: do not strongly require inhibit plugin (Igor Gnatenko)
- Inform that packages are only downloaded (RhBug:1426196) (Jaroslav Mracek)
- Move releasever check after the etc/dnf/vars substitutions. (Alexander
  Kanavin)
- Provide substitution for Repodict.add_new_repo() (RhBug:1457507) (Jaroslav
  Mracek)

* Tue Aug 01 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.6.2-3
- Unblock libguestfs builds due to regression here

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Jaroslav Mracek <jmracek@redhat.com> 2.6.2-1
- Remove autodeglob optimization (Jaroslav Rohel)
- Integrate --destdir with --destdir from download plugin (Ondřej Sojka)
- Add CLI option --destdir (RhBug:1279001) (Ondřej Sojka)
- Add myself to the AUTHORS file (Nathaniel McCallum)
- Add the --forcearch CLI flag (Nathaniel McCallum)
- Add 'ignorearch' option (Nathaniel McCallum)
- Provide an API for setting 'arch' and 'basearch' (Nathaniel McCallum)
- Add nevra forms for repoquery command (Jaroslav Rohel)
- Fix UnicodeDecodeError during checkSig() on non UTF-8 locale (RhBug:1397848)
  (Jaroslav Rohel)
- Add dnf option --noautoremove (RhBug:1361424) (Jaroslav Mracek)
- Add group argument for mark command (Jaroslav Mracek)
- Report problems for each pkg during gpgcheck (RhBug:1387925) (Jaroslav
  Mracek)
- fix minor spelling mistakes (René Genz)
- Print warning when wrong delimiter in cache (RhBug:1332099) (Vítek Hoch)
- Fix the loading of config for dnf-automatic command_email (RhBug:1470116)
  (Jaroslav Rohel)
- Enable download progress bar if redirected output (RhBug:1161950) (Jaroslav
  Mracek)
- Support short abbrevations of commands (RhBug:1320254) (Vítek Hoch)
- Remove unused variables kwargs (Jaroslav Mracek)
- Not reinstall packages if install from repository-pkgs used (Jaroslav Mracek)
- bump dnf version to 2.6.0 (Igor Gnatenko)
- spec: use python2- prefix for hawkey (Igor Gnatenko)
- spec: use sphinx-build binary rather than package name (Igor Gnatenko)
- spec: python-bugzilla is not needed for building (Igor Gnatenko)
- spec: fix instructions about generating tarball (Igor Gnatenko)
- po: Update translations (Igor Gnatenko)
- Add an example of installation without weak-deps  (RhBug:1424723) (Jaroslav
  Mracek)
- Add detection if mirrorlist is used for metalink (Jaroslav Mracek)
- Rename variable (Jaroslav Mracek)
- Add --groupmember option to repoquery (RhBug:1462486) (Jaroslav Mracek)
- Check checksum for local repositories (RhBug:1314405) (Jaroslav Mracek)
- Spelling fixes (Ville Skyttä)
- repoquery --obsoletes prints obsoletes (RhBug:1457368) (Matěj Cepl)
- Provide pkg name hint for icase (RhBug:1339280) (RhBug:1138978) (Jaroslav
  Mracek)
- Return only latest pkgs for "dnf list upgrades" (RhBug:1423472) (Jaroslav
  Mracek)
- cleanup code not executed in case of exception (Marek Blaha)
- Allow to modify message for user confirmation (Jaroslav Mracek)
- Add autocheck_running_kernel config option (Štěpán Smetana)
- Inform about skipped packages for group install (RhBug:1427365) (Jaroslav
  Mracek)
- Remove group remove unneeded pkgs (RhBug:1398871) (RhBug:1432312) (Jaroslav
  Mracek)
- po: update translations (Igor Gnatenko)

* Mon Jun 12 2017 Jaroslav Mracek <jmracek@redhat.com> 2.5.1-1
- bump version to 2.5.1 + update release notes (Jaroslav Mracek)
- Fix: dnf update --refresh fails for repo_gpgcheck=1 (RhBug:1456419) (Daniel
  Mach)
- Don't try to cut datetime message (Jaroslav Rohel)
- Use localized datetime format (RhBug:1445021) (Jaroslav Rohel)
- Work with locale date (Jaroslav Rohel)
- Use ISO 8601 time format in logfile (Jaroslav Rohel)
- Add unitest to prevent callbacks breakage (Jaroslav Mracek)
- Provide compatibility for tools that do not use total_drpms (Jaroslav Mracek)
- Requires strict usage of repoquery --recursive (Jaroslav Mracek)
- Fix output for --resolve with --installed for repoquery (Jaroslav Mracek)
- Remove unnecessary inheritance of yum conf options (Martin Hatina)
- Remove alwaysprompt option support (RhBug:1400714) (Jaroslav Rohel)
- Allow to install groups with multilib_policy=all (RhBug:1250702) (Jaroslav
  Mracek)
- Redesign Base.install() to provide alternatives (Jaroslav Mracek)
- Report excludes includes into logger.debug (RhBug:1381988) (Jaroslav Mracek)
- Provide new API to parse string to NEVRA () (Jaroslav Mracek)
- Add more repoquery querytags (Jaroslav Rohel)
- Not hide tracebacks (Jaroslav Mracek)
- Solve error handling for get attr in yumdb (RhBug:1397848) (Jaroslav Mracek)
- Provide a better error if throttle to low (RhBug:1321407) (Jaroslav Mracek)
- Change timeout to 30s (RhBug:1291867) (Jaroslav Mracek)
- Add pre_transaction hook for plugins (Jaroslav Rohel)
- Not download metadata if "dnf history [info|list|userinstalled]" (Jaroslav
  Mracek)
- Not download metadata if "dnf repo-pkgs <repo> list --installed" (Jaroslav
  Mracek)
- Not download metadata if "dnf list --installed" (RhBug:1372895) (Jaroslav
  Mracek)
- Format pkg str for repoquery --tree due to -qf (RhBug:1444751) (Jaroslav
  Mracek)

* Wed May 24 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.5.0-2
- Revert patch which breaks API

* Mon May 22 2017 Jaroslav Mracek <jmracek@redhat.com> 2.5.0-1
- Update release notes (Jaroslav Mracek)
- Change documentation for history --userinstalled (RhBug:1370062) (Jaroslav
  Mracek)
- Change example to install plugin using versionlock (Jaroslav Mracek)
- Remove unused method Goal.best_run_diff() (Jaroslav Mracek)
- Change recommendations if some problems appear (RhBug:1293067) (Jaroslav
  Mracek)
- Report problems for goals with optional=True (Jaroslav Mracek)
- Format resolve problem messages in method in dnf.util (Jaroslav Mracek)
- Enhance reports about broken dep (RhBug:1398040)(RhBug:1393814) (Jaroslav
  Mracek)
- search: do not generate error if not match anything (RhBug:1342157) (Jaroslav
  Rohel)
- Check if any plugin is removed in transaction (RhBug:1379906) (Jaroslav
  Mracek)
- Show progress for DRPM (RhBug:1198975) (Jaroslav Mracek)
- Fix disabledplugin option (Iavael)
- [history]: fixed info command merged output (Eduard Čuba)

* Thu May 11 2017 Jaroslav Mracek <jmracek@redhat.com> 2.4.1-1
- bump version to 2.4.1 + update release notes (Jaroslav Mracek)
- goal: do not mark weak dependencies as userinstalled (Igor Gnatenko)
- fix typo in supplements (RhBug:1446756) (Igor Gnatenko)
- Describe present behavior of installonly_limit conf option (Jaroslav Mracek)
- Reset all transaction for groups if Base.reset() (RhBug:1446432) (Jaroslav
  Mracek)
- Explain how add negative num for --latest-limit (RhBug:1446641) (Jaroslav
  Mracek)
- trivial: don't duplicate option names (Igor Gnatenko)
- Add support for --userinstalled for repoquery command (RhBug:1278124)
  (Jaroslav Rohel)
- Fix header of search result sections (RhBug:1301868) (Jaroslav Rohel)
- Filter out src for get_best_selector (Jaroslav Mracek)
- Add minor changes in formating of documentation (Jaroslav Mracek)

* Thu May 04 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.4.0-2
- Don't choose src packages for installation

* Tue May 02 2017 Jaroslav Mracek <jmracek@redhat.com> 2.4.0-1
- po: Update translations (Igor Gnatenko)
- po: Update translations (Igor Gnatenko)
- introduce '--enableplugin' option (Martin Hatina)
- Improve detection of file patterns (Jaroslav Mracek)
- Add method _get_nevra_solution() for subject (Jaroslav Mracek)
- Do not add "*" into query filter in _nevra_to_filters() (Jaroslav Mracek)
- Remove usage of nevra_possibilities_real() (Jaroslav Mracek)
- Increase performance for downgrade_to() (Jaroslav Mracek)
- Add additional keys for get_best_query() (Jaroslav Mracek)
- Increase performance for get_best_selector() (Jaroslav Mracek)
- Increase performance for get_best_query() (Jaroslav Mracek)
- Fix "Package" text translation (RhBug:1302935) (Jaroslav Rohel)
- Create a warning if releasever is None (Jaroslav Mracek)
- Adds cost, excludepkgs, and includepkgs to Doc (RhBug:1248684) (Jaroslav
  Mracek)
- Change auto-detection of releasever in empty installroot (Jaroslav Mracek)
- Do not load system repo for makecache command (RhBug:1441636) (Jaroslav
  Mracek)
- Do not raise assertion if group inst and rmv pkgs (RhBug:1438438) (Jaroslav
  Mracek)
- yum layer using python3 (Martin Hatina)
- Filter url protocols for baseurl in Package.remote_location (Jaroslav Mracek)
- Add armv5tl to arm basearch (Neal Gompa)
- Setup additional parameters for handler for remote packages (Jaroslav Mracek)
- Use same method for user/password setting of every librepo.handle (Jaroslav
  Mracek)
- Fix PEP8 violations and remove unused import (Jaroslav Mracek)
- Handle unknown file size in download progress (Jaroslav Mracek)
- Allow to delete cashed files from command line by clean command (Jaroslav
  Mracek)
- Save command line packages into chachedir (RhBug:1256313) (Jaroslav Mracek)
- Add progress bar for download of commandline pkgs (RhBug:1161950) (Jaroslav
  Mracek)
- Fix minor typo Closes: #781 Approved by: ignatenkobrain (Yuri Chornoivan)
- Mark unremoved packages as failed (RhBug:1421244) (Jaroslav Mracek)

* Mon Apr 10 2017 Jaroslav Mracek <jmracek@redhat.com> 2.3.0-1
- update release notes (Jaroslav Mracek)
- po: Update translations (Igor Gnatenko)
- Add require of subcommand for repo-pkgs command (Jaroslav Rohel)
- shell: Fix commands initialization (Jaroslav Rohel)
- po: Update translations (Igor Gnatenko)
- Add support for --location for repoquery command (RhBug:1290137) (Jaroslav
  Mracek)
- Add support of --recursive with --resolve in repoquery (Jaroslav Mracek)
- Add --recursive option for repoquery (Jaroslav Mracek)
- Add --whatconflicts for repoquery (Jaroslav Mracek)
- Add support for multiple options for repoquery (Jaroslav Mracek)
- Add multiple format option for repoquery (Jaroslav Mracek)
- Fix problem with "dnf repoquery --querytags" (Jaroslav Mracek)
- Add support of 3 options into updateinfo command (Jaroslav Mracek)
- Add inheritance of reason for obsoleting packages (Jaroslav Mracek)
- Mark installonlypkgs correctly as user installed (RhBug:1349314) (Jaroslav
  Mracek)
- Solve a problem with None names in callbacks (Jaroslav Mracek)
- Solve a problem for callbacks (Jaroslav Mracek)
- Revert "remove: CLI: --randomwait" (RhBug:1247122) (Ondřej Sojka)
- po: update translations (Igor Gnatenko)
- po: update translations (Igor Gnatenko)
- Set strings for translations (RhBug:1298717) (Jaroslav Mracek)

* Mon Mar 27 2017 Jaroslav Mracek <jmracek@redhat.com> 2.2.0-1
- bump version to 2.2.0 + update release notes (Jaroslav Mracek)
- Add documentation of new API callback actions (RhBug:1411432) (Jaroslav
  Mracek)
- Fix python2 doesn't have e.__traceback__ attribute (Jaroslav Mracek)
- Do not report erasing package as None. (Jaroslav Mracek)
- Display scriplet for transaction (RhBug:1411423) (RhBug:1406130) (Jaroslav
  Mracek)
- Add support for rpmcallbacks (Jaroslav Mracek)
- AUTHORS: updated (Jaroslav Rohel)
- Not show expiration check if no repo enabled (RhBug:1369212) (Jaroslav
  Mracek)
- Fix changelog in dnf spec file (Jaroslav Mracek)
- po: update translations (Igor Gnatenko)
- Add myself (mhatina) to AUTHORS (Martin Hatina)
- po: Update translations (Igor Gnatenko)

* Tue Mar 21 2017 Jaroslav Mracek <jmracek@redhat.com> 2.1.1-1.1
- Exchange tarball of dnf-2.1.1

* Tue Mar 21 2017 Jaroslav Mracek <jmracek@redhat.com> 2.1.1-1
- bump version to 2.1.1 + update release notes (Jaroslav Mracek)
- Sync the translation with locale (Jaroslav Rohel)
- Disable exceptions in logging (Jaroslav Rohel)
- Fix severity info in "updateinfo info" (Jaroslav Mracek)
- Add help for shell commands (Jaroslav Rohel)
- shell: no crash if missing args (Jaroslav Rohel)
- proper check of releasever, when using installroot (RhBug:1417542) (Martin
  Hatina)
- Inform about "Cache was expired" with "dnf clean" (RhBug:1401446) (Jaroslav
  Mracek)
- crypto: port to the official gpgme bindings (Igor Gnatenko)
- Fix doc example for `fill_sack` method (Lubomír Sedlář)
- po: update translations (Igor Gnatenko)
- Not try to install src package (RhBug:1416699) (Jaroslav Mracek)
- Add usage for add_new_repo() with repofrompath option (Jaroslav Mracek)
- Add new API add_new_repo() in RepoDict() (RhBug:1427132) (Jaroslav Mracek)
- docs: adds documentation for dnf-automatic's Command and CommandEmail
  emitters. (rhn)
- docs: fixes typo in section description in automatic (rhn)
- Adds new emitters for dnf-automatic. (rhn)
- po: update translations (Igor Gnatenko)
- Ensure that callback will not kill dnf transaction (Jaroslav Mracek)
- Ensure that name will be not requested on None (RhBug:1397047) (Jaroslav
  Mracek)
- Python 3.6 invalid escape sequence deprecation fix (Ville Skyttä)
- display severity information in updateinfo (#741) (Michael Mraka)
- po: update translations (Igor Gnatenko)
- Add --nodocs option for dnf (RhBug:1379628) (Jaroslav Mracek)
- Replace passive plugin noroot (Jaroslav Mracek)
- Fix incorrect formating of string for logger.info (Jaroslav Mracek)
- Not print help if empty line in script for shell command (Jaroslav Mracek)
- Run fill_sack after all repos have changed status (Jaroslav Mracek)
- Remove Hawkey object from repo if rerun of dnf.fill_sack (Jaroslav Mracek)
- util/on_metered_connection: be more polite to failures (Igor Gnatenko)
- cosmetic: i18n: rewording of 'Login user' (RhBug:1424939) (Jan Silhan)
- Fix problem with --whatprovides in repoquery (RhBug:1396992) (Jaroslav
  Mracek)
- Add -a and --all option for repoquery (RhBug:1412970) (Jaroslav Mracek)
- Change camel-case of output of grouplist (Jaroslav Mracek)
- Minor correction in release notes (Jaroslav Mracek)
- Minor correction in release notes (Jaroslav Mracek)

* Thu Feb 16 2017 Jaroslav Mracek <jmracek@redhat.com> 2.1.0-1
- bump version to 2.1.0 + update release notes (Jaroslav Mracek)
- Fix problem with --recent option in repoquery (Jaroslav Mracek)
- Fix problem with duplicated --obsoletes (RhBug:1421835) (Jaroslav Mracek)
- Python 3.6 invalid escape sequence deprecation fixes (Ville Skyttä)
- Add --repoid as alias for --repo (Jaroslav Mracek)
- introduce dnf.base.Base.update_cache() (Martin Hatina)
- Try to install uninstalled packages if group installed (Jaroslav Mracek)
- Enable search of provides in /usr/(s)bin (RgBug:1421618) (Jaroslav Mracek)
- style: ignore E261 (Igor Gnatenko)
- makecache: do not run on metered connections (RhBug:1415711) (Igor Gnatenko)
- change '--disableplugins' to '--disableplugin' (Martin Hatina)
- cosmetic: removed unused import (Jan Silhan)
- show hint how to display why package was skipped (RhBug:1417627) (Jan Silhan)
- spec: add information how to obtain archive (Igor Gnatenko)
- fix messages (UX) (Jaroslav Rohel)
- zanata update (Jan Silhan)

* Thu Feb 09 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.0.1-2
- Update to 2.0.1

* Thu Feb 09 2017 Jaroslav Mracek <jmracek@redhat.com> 2.0.1-1
- bump version to 2.0.1 + update release notes (Jaroslav Mracek)
- introduce cli 'obsoletes' option (Martin Hatina)
- swap tids if they are in wrong order (RhBug:1409361) (Michael Mraka)
- Disable shell command recursion (Jaroslav Rohel)
- Honor additional arguments for DNF shell repo list command (Jaroslav Rohel)
- don't traceback when bug title is not set (Michael Mraka)
- introducing list-security, info-security etc. commands (Michael Mraka)
- Add lsedlar to contributors list (Lubomír Sedlář)
- Return just name from Package.source_name (Lubomír Sedlář)
- introduce dnf.conf.config.MainConf.exclude() (Martin Hatina)
- systemd: Disable daemons on ostree-managed systems (Colin Walters)
- introduced dnf.base.Base.autoremove() (RhBug:1414512) (Martin Hatina)
- po: update translations (Igor Gnatenko)
- build: use relative directory for translations (Igor Gnatenko)
- Temporary eliminate a problem with install remove loop (Jaroslav Mracek)
- Handle info message when DRPM wastes data (RhBug:1238808) (Daniel
  Aleksandersen)
- Fix output for better translation (RhBug:1386085) (Abhijeet Kasurde)
- yum layer refactored (Martin Hatina)
- return values changed to match yum's (Martin Hatina)
- Reword sentence after removing package (RhBug:1286553) (Abhijeet Kasurde)
- Minor documentation revisions (Mark Szymanski)
- Minor code fix (Abhijeet Kasurde)
- automatic: email emitter date header (David Greenhouse)
- Solve problem when no repo and only rpms with upgrade command (Jaroslav
  Mracek)
- bash_completion: use system-python if it's available (Igor Gnatenko)
- spec: use system-python for dnf-yum as well (Igor Gnatenko)
- comps/groups: fix tests (Michal Luscon)
- comps: adjust group_upgrade to new CompsTransPkg style (Michal Luscon)
- groups: refactored installation (RhBug:1337731, RhBug:1336879) (Michal
  Luscon)
- Increase requirement for hawkey (Jaroslav Mracek)
- Change reporting problems for downgradePkgs() (Jaroslav Mracek)
- Use selector for base.package_upgrade() (Jaroslav Mracek)
- Add usage of selectors for base.package_install() (Jaroslav Mracek)
- Use selector for base.package_downgrade() (Jaroslav Mracek)
- Redirect base.downgrade() to base.downgrade_to() (Jaroslav Mracek)
- Enable wildcard for downgrade command (RhBug:1173349) (Jaroslav Mracek)
- Refactor downgrade cmd behavior (RhBug:1329617)(RhBug:1283255) (Jaroslav
  Mracek)
- Redirect logger.info into stderr for repolist (RhBug:1369411) (Jaroslav
  Mracek)
- Redirect logger.info into stderr for repoquery (RhBug:1243393) (Jaroslav
  Mracek)
- Add possibility for commands to redirect logger (Jaroslav Mracek)
- Put information about metadata expiration into stdout (Jaroslav Mracek)
- Change warning about added repo into info (RhBug:1243393) (Jaroslav Mracek)
- Move grouplist output from logger into stdout (Jaroslav Mracek)
- let repo exclude work the same way as global exclude (Michael Mraka)
- Fix wrong assumptions about metalinks (RhBug:1411349) (Jaroslav Mracek)
- handle --disablerepo/--enablerepo properly with strict (RhBug:1345976)
  (Štěpán Smetana)
- Add fix to notify user about no repos (RhBug:1369212) (Abhijeet Kasurde)
- Add information about "hidden" option in dnf doc (RhBug:1349247) (Abhijeet
  Kasurde)
- Fix for 'history package-list' (Amit Upadhye)
- Enable multiple args for repoquery -f (RhBug:1403930) (Jaroslav Mracek)
- Set default repo.name as repo._section (Jaroslav Mracek)
- Create from self.forms value forms in cmd.run() (Jaroslav Mracek)
- Add description of swap command into documentation (Jaroslav Mracek)
- Add swap command (RhBug:1403465) (RhBug:1110780) (Jaroslav Mracek)
- Solve a problem with shell when empty line or EOF (Jaroslav Mracek)
- shell: add history of commands (RhBug:1405333) (Michal Luscon)
- Add info if no files with repoquery -l (RhBug:1254879) (Jaroslav Mracek)
- po: update translations (Igor Gnatenko)
- po: migrate to zanata python client and trivial fixes in build (Igor
  Gnatenko)
- po: include all possible languages from zanata (Igor Gnatenko)
- po: include comments for translations (Igor Gnatenko)
- shell: catch exceptions from depsolving (Michal Luscon)
- shell: update documentation (Michal Luscon)
- shell: add transaction reset cmd (Michal Luscon)
- shell: add transaction resolve cmd (Michal Luscon)
- shell: provide rewritable demands for cmds (Michal Luscon)
- shell: catch tracebacks from shlex (Michal Luscon)
- shell: handle ctrl+D more gracefully (Michal Luscon)
- groups: set demands in configure instead of run (Michal Luscon)
- shell: implement config cmd (Michal Luscon)
- shell: add help (Michal Luscon)
- shell: make alias repo list -> repolist (Michal Luscon)
- shell: catch exceptions from do_transaction (Michal Luscon)
- shell: resolve transaction in ts run (Michal Luscon)
- shell: add default value for internal methods argument (Michal Luscon)
- shell: create run alias for ts run (Michal Luscon)
- shell: add ts list cmd (Michal Luscon)
- shell: refill sack after every successful repo cmd (Michal Luscon)
- shell: allow running multiple transaction in one session (Michal Luscon)
- shell: add ts command (Michal Luscon)
- shell: catch cmd parsing and run exceptions (Michal Luscon)
- shell: allow to run scripts (Michal Luscon)
- shell: add repo cmd (Michal Luscon)
- shell: add resolving + transaction run support (Michal Luscon)
- shell: implement quit method (Michal Luscon)
- shell: add custom cmds stubs (Michal Luscon)
- shell: implement basic logic (Michal Luscon)
- shell: register new cmd (Michal Luscon)

* Thu Dec 15 2016 mluscon <mluscon@redhat.com> - 2.0.0-2
- rebuild py36

* Wed Dec 14 2016 Michal Luscon <mluscon@redhat.com> 2.0.0-1
- tests: catch ModuleNotFoundError as well (Igor Gnatenko)
- Switch out automatic service for automatic-download and automatic-install
  (Pat Riehecky)
- Make upgrade-to alias for upgrade (RhBug:1327999) (Jaroslav Mracek)
- skip appending an empty option (RhBug: 1400081) (Michael Mraka)
- Add description of nevra foems for commands and autoremove args (Jaroslav
  Mracek)
- Add support of arguments nevra forms for autoremove command (Jaroslav Mracek)
- Add nevra forms for remove command (Jaroslav Mracek)
- Add nevra forms for install command (Jaroslav Mracek)
- add bin/yum into .gitignore (Michal Luscon)
- clean: acquire all locks before cleaning (RhBug:1293782) (Michal Luscon)
- Change hawkey version requirement (Jaroslav Mracek)
- Add information for translators (RhBug:1386078) (Jaroslav Mracek)
- Change info to warning for clean repoquery output (RhBug:1358245) (Jaroslav
  Mracek)
- Add description of pkg flag for Query (RhBug:1243393) (Jaroslav Mracek)
- Add minor changes in documentation (Jaroslav Mracek)
- Do not always overwrite the name with the repo ID (Neal Gompa)

* Tue Dec 06 2016 Martin Hatina <mhatina@redhat.com> - 2.0.0-0.rc2.5
- Fix libdnf requirement version

* Tue Dec 06 2016 Martin Hatina <mhatina@redhat.com> - 2.0.0-0.rc2.4
- Increase requirement of libdnf

* Sun Dec 04 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-0.rc2.3
- Restore patch for relaxing strict groups

* Fri Dec 02 2016 Martin Hatina <mhatina@redhat.com> 2.0.0-0.rc2.2
- Restore changelog

* Fri Dec 02 2016 Martin Hatina <mhatina@redhat.com> 2.0.0-0.rc2.1
- See http://dnf.readthedocs.io/en/latest/release_notes.html

* Thu Oct 06 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-0.rc1.4
- Fix crash in repoquery
- Trim changelog

* Tue Oct 04 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-0.rc1.3
- Revert group install strict bugfix (RHBZ #1380945)

* Fri Sep 30 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.0.0-0.rc1.2
- Add alias 'rpm' for 'type=' option (RHBZ #1380580)

* Thu Sep 29 2016 Michal Luscon <mluscon@redhat.com> 2.0.0-0.rc1.1
- See http://dnf.readthedocs.io/en/latest/release_notes.html

* Thu Sep 08 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.10-2
- Obsolete dnf-langpacks
- Backport patch for dnf repolist disabled

* Thu Aug 18 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.10-1
- Update to 1.1.10

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.9-6
- Fix typo

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.9-5
- Also change shebang for %%{?system_python_abi} in %%{_bindir}/dnf

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.9-4
- Add %%{?system_python_abi}

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 24 2016 Michal Luscon <mluscon@redhat.com> 1.1.9-2
- Revert "group: treat mandatory pkgs as mandatory if strict=true" (RhBug:1337731)
- enforce-api: reflect changes from #992475 in completion_helper (RhBug:1338504)
- enforce-api: add compatibility methods for renamed counterparts (RhBug:1338564)

* Thu May 19 2016 Igor Gnatenko <ignatenko@redhat.com> 1.1.9-1
- doc: release notes 1.1.9 (Igor Gnatenko)
- spec: correctly set up requirements for python subpkg (Igor Gnatenko)
- spec: follow new packaging guidelines & make compatible with el7 (Igor
  Gnatenko)
- zanata update (Jan Silhan)
- enforce-api: add missing bits of Base class (Michal Luscon)
- help: unify help msg strings (Michal Luscon)
- enforce-api: decorate Base class (Michal Luscon)
- util: add decorator informing users of nonapi functions (Michal Luscon)
- Added description for 'autoremove' in dnf help (RhBug:1324086) (Abhijeet
  Kasurde)
- i18n: fixup for 0db13feed (Michal Luscon)
- i18n: use fallback mode if terminal does not support UTF-8 (RhBug:1332012)
  (Michal Luscon)
- Revert "spec: follow new packaging guidelines & make compatible with el7"
  (Michal Luscon)
- move autoglob feature directly to filterm() and filter() (Michael Mraka)
- group: treat mandatory pkgs as mandatory if strict=true (RhBug:1292892)
  (Michal Luscon)
- locks: fix lock paths in tmpfsd config since cachedir has been changed
  (Michal Luscon)
- remove formating from translation strings (Michal Luscon)
- base: set diskspace check filter before applying the filters (RhBug:1328674)
  (Michal Luscon)
- order repos by priority and cost (Michael Mraka)
- spec: follow new packaging guidelines & make compatible with el7 (Igor
  Gnatenko)
- bash-completion: first try to set fallback to BASH_COMPLETION_COMPATDIR (Igor
  Gnatenko)
- updated copyrights for files changed this year (Michael Mraka)
- cli: fix warning from re.split() about non-empty pattern (RhBug:1286556)
  (Igor Gnatenko)
- update authors file (Michal Luscon)
- Define __hash__ method for YumHistoryPackage (RhBug:1245121) (Max Prokhorov)

* Tue Apr 05 2016 Michal Luscon <mluscon@redhat.com> 1.1.8-1
- refactor: repo: add md_expired property (Michal Domonkos)
- test: fix cachedir usage in LocalRepoTest (Michal Domonkos)
- clean: operate on all cached repos (RhBug:1278225) (Michal Domonkos)
- refactor: repo: globally define valid repoid chars (Michal Domonkos)
- RepoPersistor: only write to disk when requested (Michal Domonkos)
- clean: remove dead subcommands (Michal Domonkos)
- doc: --best in case of problem (RhBug:1309408) (Jan Silhan)
- Added fix for correct error message for group info (RhBug:1209649) (Abhijeet
  Kasurde)
- repo: don't get current timeout for librepo (RhBug:1272977) (Igor Gnatenko)
- doc: fix default timeout value (Michal Luscon)
- cli: inform only about nonzero md cache check interval (Michal Luscon)
- base: report errors in batch at the end of md downloading (Michal Luscon)
- repo: produce more sane error if md download fails (Michal Luscon)
- zanata update (RhBug:1322226) (Jan Silhan)
- doc: Fixed syntax of `assumeyes` and `defaultyes` ref lables in
  `conf_ref.rst` (Matt Sturgeon)
- Fix output headers for dnf history command (Michael Dunphy)
- doc: change example of 'dnf-command(repoquery)' (Jaroslav Mracek)
- makacache.service: shorten journal logs (RhBug:1315349) (Michal Luscon)
- config: improve UX of error msg (Michal Luscon)
- Added user friendly message for out of range value (RhBug:1214562) (Abhijeet
  Kasurde)
- doc: prefer repoquery to list (Jan Silhan)
- history: fix empty history cmd (RhBug:1313215) (Michal Luscon)
- Very minor tweak to the docs for `--assumeyes` and `--assumeno` (Matt
  Sturgeon)

* Thu Feb 25 2016 Michal Luscon <mluscon@redhat.com> 1.1.7-1
- Add `/etc/distro.repos.d` as a path owned by the dnf package (Neal Gompa
  (ニール・ゴンパ))
- Change order of search and add new default repodirs (RhBug:1286477) (Neal
  Gompa (ニール・ゴンパ))
- group: don't mark available packages as installed (RhBug:1305356) (Jan
  Silhan)
- history: adjust demands for particular subcommands (RhBug:1258503) (Michal
  Luscon)
- Added extension command for group list (RhBug:1283432) (Abhijeet Kasurde)
- perf: dnf repository-packages <repo> upgrade (RhBug:1306304) (Jan Silhan)
- sack: Pass base.conf.substitutions["arch"] to sack in build_sack() function.
  (Daniel Mach)
- build: make python2/3 binaries at build time (Michal Domonkos)
- fix dnf history traceback (RhBug:1303149) (Jan Silhan)
- cli: truncate expiration msg (RhBug:1302217) (Michal Luscon)

* Mon Jan 25 2016 Michal Luscon <mluscon@redhat.com> 1.1.6-1
- history: don't fail if there is no history (RhBug:1291895) (Michal Luscon)
- Allow dnf to use a socks5 proxy, since curl support it (RhBug:1256587)
  (Michael Scherer)
- output: do not log rpm info twice (RhBug:1287221) (Michal Luscon)
- dnf owns /var/lib/dnf dir (RhBug:1294241) (Jan Silhan)
- Fix handling of repo that never expire (RhBug:1289166) (Jaroslav Mracek)
- Filter out .src packages when multilib_proto=all (Jeff Smith)
- Enable string for translation (RhBug:1294355) (Parag Nemade)
- Let logging format messages on demand (Ville Skyttä)
- clean: include metadata of local repos (RhBug:1226322) (Michal Domonkos)
- completion: Install to where bash-completion.pc says (Ville Skyttä)
- spec: bash completion is not a %%config file (Ville Skyttä)
- Change assertion handling for rpmsack.py (RhBug:1275878) (Jaroslav Mracek)
- cli: fix storing arguments in history (RhBug:1239274) (Ting-Wei Lan)

* Thu Dec 17 2015 Michal Luscon <mluscon@redhat.com> 1.1.5-1
- base: save group persistor only after successful transaction (RhBug:1229046)
  (Michal Luscon)
- base: do not clean tempfiles after remove transaction (RhBug:1282250) (Michal
  Luscon)
- base: clean packages that do not belong to any trans (Michal Luscon)
- upgrade: allow group upgrade via @ syntax (RhBug:1265391) (Michal Luscon)
- spec: Mark license files as %%license where available (Ville Skyttä)
- Remove unused imports (Ville Skyttä)
- Spelling fixes (Ville Skyttä)
- Fix typos in documentation (Rob Cutmore)
- parser: add support for braces in substitution (RhBug:1283017) (Dave
  Johansen)
- completion_helper: Don't omit "packages" from clean completions (Ville
  Skyttä)
- bash-completion: Avoid unnecessary python invocation per _dnf_helper (Ville
  Skyttä)
- repo: Download drpms early (RhBug:1260421) (Ville Skyttä)
- clean: Don't hardcode list of args in two places (Ville Skyttä)
- cli: don't crash if y/n and sys.stdin is None (RhBug:1278382) (Adam
  Williamson)
- sp err "environement" -> "environment" (Michael Goodwin)
- Remove -OO from #!/usr/bin/python (RhBug:1230820) (Jaroslav Mracek)
- cli: warn if plugins are disabled (RhBug:1280240) (Michal Luscon)

* Mon Nov 16 2015 Michal Luscon <mluscon@redhat.com> 1.1.4-1
- AUTHORS: updated (Jan Silhan)
- query: add compatibility methods (Michal Luscon)
- query: add recent, extras and autoremove methods to Query (Michal Luscon)
- query: add duplicated and latest-limit queries into api (Michal Luscon)
- format the email message with its as_string method (Olivier Andrieu)
- added dnf.i18n.ucd* functions as deprecated API (Jan Silhan)
- i18n: unicode resulting translations (RhBug:1278031) (Jan Silhan)
- po: get rid of new lines in translation (Jan Silhan)
- output: add skip count to summary (RhBug:1264032) (Michal Domonkos)
- groups: fix environment upgrade (Michal Luscon)
- Fix plural strings extraction (RhBug:1209056) (Baurzhan Muftakhidinov)
- po: fixed malformed beginning / ending (Jan Silhan)
- zanata update (Jan Silhan)
- cli: prevent tracebacks after C^ (RhBug:1274946) (Michal Luscon)

* Wed Oct 14 2015 Michal Luscon <mluscon@redhat.com> 1.1.3-1
- Update command_ref.rst (Jaroslav Mracek)
- Change in automatic.conf email settings to prevent email error with default
  sender name (Jaroslav Mracek)
- Replace assert_called() with assert_called_with() for Py35 support (Neal
  Gompa (ニール・ゴンパ))
- doc: improve documentation (Jaroslav Mracek)
- doc: update the instructions related to nightly builds (Radek Holy)
- Revert "Add the continuous integration script" (Radek Holy)
- Revert "cosmetic: ci: fix the Copr name in the README" (Radek Holy)
- Fix typo in Command.canonical's doctring (Timo Wilken)
- base: group_install is able to exclude mandatory packages
  (Related:RhBug:1199868) (Jan Silhan)

* Wed Sep 30 2015 Michal Luscon <mluscon@redhat.com> 1.1.2-4
- don't import readline as it causes crashes in Anaconda
  (related:RhBug:1258364)

* Tue Sep 22 2015 Michal Luscon <mluscon@redhat.com> 1.1.2-3
- Revert "completion_helper: don't get IndexError (RhBug:1250038)"

* Tue Sep 22 2015 Michal Luscon <mluscon@redhat.com> 1.1.2-2
- add hawkey version requirement
- revert commit #70956

* Tue Sep 22 2015 Michal Luscon <mluscon@redhat.com> 1.1.2-1
- doc: release notes 1.1.2 (Michal Luscon)
- sanitize non Unicode command attributes (RhBug:1262082) (Jan Silhan)
- don't redirect confirmation to stderr RhBug(1258364) (Vladan Kudlac)
- clean: add rpmdb to usage (Vladan Kudlac)
- completion_helper: don't get IndexError (RhBug:1250038) (Vladan Kudlac)
- add --downloadonly switch (RhBug:1048433) (Adam Salih)
- Add globbing support to base.by_provides() (RhBug:11259650) (Valentina
  Mukhamedzhanova)
- spec: packaging python(3)-dnf according to new Fedora guidelines
  (RhBug:1260198) (Jaroslav Mracek)
- Bug in Source0: URL in dnf.spec fixed (RhBug:126255) (Jaroslav Mracek)
- To dnf.spec added provides dnf-command(command name) for 21 dnf commands
  (RhBug:1259657) (jmracek)
- Expire repo cache on failed package download (Valentina Mukhamedzhanova)
- cosmetic: ci: fix the Copr name in the README (Radek Holy)
- Add the continuous integration script (Radek Holy)
- Set proper charset on email in dnf-automatic (RhBug:1254982) (Valentina
  Mukhamedzhanova)
- doc: improve configuration description (RhBug:1261766) (Michal Luscon)
- remove: show from which repo a package is (Vladan Kudlac)
- list: show from which repo a package is (RhBug:1234491) (Vladan Kudlac)
- Spelling/grammar fixes (Ville Skyttä)
- install: fix crash when terminal window is small (RhBug:1256531) (Vladan
  Kudlac)
- install: mark unification of the progress bar (Vladan Kudlac)
- fix translations in python3 (RhBug:1254687) (Michal Luscon)
- group: CompsQuery now returns group ids (RhBug:1261656) (Michal Luscon)

* Tue Sep 08 2015 Michal Luscon <mluscon@redhat.com> 1.1.1-2
- fix access to demands (RhBug:1259194) (Jan Silhan)
- make clean_requiremets_on_remove=True (RhBug:1260280) (Jan Silhan)

* Mon Aug 31 2015 Michal Luscon <mluscon@redhat.com> 1.1.1-1
- Fixed typo (RhBug:1249319) (Adam Salih)
- fixed downgrade with wildcard (RhBug:1234763) (Adam Salih)
- reorganize logic of get_best_selector(s) and query (RhBug:1242946) (Adam
  Salih)
- completion_helper: don't crash if exception occurred (RhBug:1225225) (Igor
  Gnatenko)
- base: expire cache if repo is not available (Michal Luscon)
- Don't suggest --allowerasing if it is enabled (Christian Stadelmann)
- translation works in python3 (RhBug:1254687) (Jan Silhan)
- logrotate less often (RhBug:1247766) (Jan Silhan)
- implement dnf mark command (RhBug:1125925) (Michal Luscon)
- groups: use comps data to migrate persistor (Michal Luscon)
- groups: preserve api compatibility (Michal Luscon)
- groups: use persistor data for removing env/group (Michal Luscon)
- persistor: add migration and bump version (Michal Luscon)
- persistor: store name and ui_name of group (Michal Luscon)
- show real metadata timestamp on the server in verbose mode (Jan Silhan)
- lock: make rpmdb lock blocking (RhBug:1210289) (Michal Luscon)

* Wed Aug 12 2015 Michal Luscon <mluscon@redhat.com> 1.1.0-2
- update: installonly pkgs are not shown in both install and skipped section
  (RhBug:1252415) (Jan Silhan)
- output: sort skipped packages (Jan Silhan)
- output: skipped conflicts are set (RhBug:1252032) (Jan Silhan)
- keep the dwongrading package installed if transaction fails (RhBug:1249379)
  (Jan Silhan)
- don't store empty attributes (RhBug:1246928) (Michael Mraka)
- doc: correct dnf.conf man section (RhBug:1245349) (Michal Luscon)

* Mon Aug 10 2015 Michal Luscon <mluscon@redhat.com> 1.1.0-1
- print skipped pkg with broken deps too (Related:RhBug:1210445) (Jan Silhan)
- history: set commands output as default (RhBug:1218401) (Michal Luscon)
- Update es.po. save:guardar -> save:ahorrar (Máximo Castañeda)
- cosmetic: option arg in Base.*install is replaced with strict (Jan Silhan)
- group: don't fail on first non-existing group (Jan Silhan)
- install: skips local pkgs of lower version when strict=0
  (Related:RhBug:1227952) (Jan Silhan)
- install: skip broken/conflicting packages in groups when strict=0 (Jan
  Silhan)
- install: skip broken/conflicting packages when strict=0 (Jan Silhan)
- implemented `strict` config option working in install cmd (RhBug:1197456)
  (Jan Silhan)
- fixed 'dnf --quiet repolist' lack of output (RhBug:1236310) (Nick Coghlan)
- Add support for MIPS architecture (Michal Toman)
- package: respect baseurl attribute in localPkg() (RhBug:1219638) (Michal
  Luscon)
- Download error message is not written on the same line as progress bar
  anymore (RhBug: 1224248) (Adam Salih)
- dnf downgrade does not try to downgrade not installed packages (RhBug:
  1243501) (max9631)
- pkgs not installed due to rpm error are reported (RhBug:1207981) (Adam Salih)
- dnf install checks availability of all given packages (RhBug:1208918) (Adam
  Salih)
- implemented install_weak_deps config option (RhBug:1221635) (Jan Silhan)
- ignore SIGPIPE (RhBug:1236306) (Michael Mraka)
- always add LoggingTransactionDisplay to the list of transaction displays
  (RhBug:1234639) (Radek Holy)
- Add missing FILES section (RhBug: 1225237) (Adam Salih)
- doc: Add yum vs dnf hook information (RhBug:1244486) (Parag Nemade)
- doc: clarify the expected type of the do_transactions's display parameter
  (Radek Holy)
- apichange: add dnf.cli.demand.DemandSheet.transaction_display (Radek Holy)
- apichange: add dnf.callback.TransactionProgress (Radek Holy)
- move the error output from TransactionDisplay into a separate class (Radek
  Holy)
- rename TransactionDisplay.errorlog to TransactionDisplay.error (Radek Holy)
- report package verification as a regular RPM transaction event (Radek Holy)
- rename TransactionDisplay.event to TransactionDisplay.progress (Radek Holy)
- apichange: deprecate dnf.callback.LoggingTransactionDisplay (Radek Holy)
- use both CliTransactionDisplay and demands.transaction_display (Radek Holy)
- apichange: accept multiple displays in do_transaction (Radek Holy)
- support multiple displays in RPMTransaction (Radek Holy)
