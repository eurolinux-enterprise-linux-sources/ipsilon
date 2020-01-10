# Bundling request for bootstrap/patternfly: https://fedorahosted.org/fpc/ticket/483

Name:       ipsilon
Version:    1.0.0
Release:    12%{?builddate}%{?gittag}%{?dist}
Summary:    An Identity Provider Server

Group:      System Environment/Base
License:    GPLv3+ and MIT
URL:        https://fedorahosted.org/ipsilon/
Source0:    https://fedorahosted.org/released/ipsilon/ipsilon-%{version}.tar.gz
BuildArch:  noarch

Patch0:     ipsilon-informative-ldap-error.patch
Patch1:     ipsilon-fullpath-url.patch
Patch2:     ipsilon-cve-xss.patch
Patch3:     ipsilon-cve-permcheck.patch
Patch4:     ipsilon-count-ipa-as-login-plugin.patch
Patch5:     ipsilon-log-nameid-error.patch
Patch6:     ipsilon-add-city-attribute.patch
Patch7:     ipsilon-db-keys.patch
Patch8:     ipsilon-saml-patch-check.patch
Patch9:     ipsilon-database-cleanup.patch
Patch10:    ipsilon-cve-check-sp-deletion-permissions.patch


BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  lasso-python
BuildRequires:  m2crypto

Requires:       python-requests
Requires:       %{name}-base = %{version}-%{release}
BuildArch:      noarch

%description
Ipsilon is a multi-protocol Identity Provider service. Its function is to
bridge authentication providers and applications to achieve Single Sign On
and Federation.


%package base
Summary:        Ipsilon base IDP server
Group:          System Environment/Base
License:        GPLv3+
Requires:       httpd
Requires:       mod_ssl
Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       %{name}-provider = %{version}-%{release}
Requires:       mod_wsgi
Requires:       python-cherrypy
Requires:       python-jinja2
Requires:       python-lxml
Requires:       python-sqlalchemy
Requires:       open-sans-fonts
Requires(pre):  shadow-utils
Requires(post): %_sbindir/semanage, %_sbindir/restorecon
Requires(postun): %_sbindir/semanage


%description base
The Ipsilon IdP server without installer


%package filesystem
Summary:        Package providing files required by Ipsilon
Group:          System Environment/Base
License:        GPLv3+

%description filesystem
Package providing basic directory structure required
for all Ipsilon parts


%package client
Summary:        Tools for configuring Ipsilon clients
Group:          System Environment/Base
License:        GPLv3+
Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       %{name}-saml2-base = %{version}-%{release}
Requires:       mod_auth_mellon
Requires:       python-requests
BuildArch:      noarch

%description client
Client install tools


%package tools-ipa
summary:        IPA helpers
Group:          System Environment/Base
License:        GPLv3+
Requires:       %{name}-authgssapi = %{version}-%{release}
Requires:       %{name}-authform = %{version}-%{release}
%if 0%{?rhel}
Requires:       ipa-client
Requires:       ipa-admintools
%else
Requires:       freeipa-client
Requires:       freeipa-admintools
%endif
BuildArch:      noarch

%description tools-ipa
Convenience client install tools for IPA support in the Ipsilon identity Provider


%package saml2-base
Summary:        SAML2 base
Group:          System Environment/Base
License:        GPLv3+
Requires:       lasso-python
Requires:       python-lxml
BuildArch:      noarch

%description saml2-base
Provides core SAML2 utilities


%package saml2
Summary:        SAML2 provider plugin
Group:          System Environment/Base
License:        GPLv3+
Provides:       ipsilon-provider = %{version}-%{release}
Requires:       %{name}-base = %{version}-%{release}
Requires:       %{name}-saml2-base = %{version}-%{release}
BuildArch:      noarch

%description saml2
Provides a SAML2 provider plugin for the Ipsilon identity Provider


%package persona
Summary:        Persona provider plugin
Group:          System Environment/Base
License:        GPLv3+
Provides:       ipsilon-provider = %{version}-%{release}
Requires:       %{name}-base = %{version}-%{release}
Requires:       m2crypto
BuildArch:      noarch

%description persona
Provides a Persona provider plugin for the Ipsilon identity Provider


%package authfas
Summary:        Fedora Authentication System login plugin
Group:          System Environment/Base
License:        GPLv3+
Requires:       %{name}-base = %{version}-%{release}
Requires:       python-fedora
BuildArch:      noarch

%description authfas
Provides a login plugin to authenticate against the Fedora Authentication System


%package authform
Summary:        mod_intercept_form_submit login plugin
Group:          System Environment/Base
License:        GPLv3+
Requires:       %{name}-base = %{version}-%{release}
Requires:       mod_intercept_form_submit
BuildArch:      noarch

%description authform
Provides a login plugin to authenticate with mod_intercept_form_submit


%package authgssapi
Summary:        mod_auth_gssapi based login plugin
Group:          System Environment/Base
License:        GPLv3+
Requires:       %{name}-base = %{version}-%{release}
Requires:       mod_auth_gssapi
BuildArch:      noarch

%description authgssapi
Provides a login plugin to allow authentication via the mod_auth_gssapi
Apache module.


%package authldap
Summary:        LDAP info and login plugin
Group:          System Environment/Base
License:        GPLv3+
Requires:       %{name}-base = %{version}-%{release}
Requires:       python-ldap
BuildArch:      noarch

%description authldap
Provides a login plugin to allow authentication and info retrieval via LDAP.

%package infosssd
Summary:        SSSD & mod_lookup_identity-based identity plugin
Group:          System Environment/Base
License:        GPLv3+
Requires:       %{name}-base = %{version}-%{release}
Requires:       mod_lookup_identity
Requires:       libsss_simpleifp
Requires:       sssd >= 1.12.4
BuildArch:      noarch

%description infosssd
Provides an info plugin to allow retrieval via mod_lookup_identity and
SSSD.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1


%build
CFLAGS="%{optflags}" %{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_defaultdocdir}
# These 0700 permissions are because ipsilon will store private keys here
install -d -m 0700 %{buildroot}%{_sharedstatedir}/ipsilon
install -d -m 0700 %{buildroot}%{_sysconfdir}/ipsilon
mv %{buildroot}/%{_bindir}/ipsilon %{buildroot}/%{_libexecdir}
mv %{buildroot}/%{_bindir}/ipsilon-server-install %{buildroot}/%{_sbindir}
mv %{buildroot}%{_defaultdocdir}/%{name} %{buildroot}%{_defaultdocdir}/%{name}-%{version}
rm -fr %{buildroot}%{python2_sitelib}/tests
ln -s %{_datadir}/fonts %{buildroot}%{_datadir}/ipsilon/ui/fonts
# Remove openid
rm -fr %{buildroot}%{python2_sitelib}/ipsilon/providers/openid*
rm -fr %{buildroot}%{_datadir}/ipsilon/templates/openid
# Remove authfas
rm -fr %{buildroot}%{python2_sitelib}/ipsilon/login/authfas*
# Remove authpam
rm -fr %{buildroot}%{python2_sitelib}/ipsilon/login/authpam*

#%check
# The test suite is not being run because:
#  1. The last step of %%install removes the entire test suite
#  2. It increases build time a lot
#  3. It adds more build dependencies (namely postgresql server and client libraries)

%pre
getent group ipsilon >/dev/null || groupadd -r ipsilon
getent passwd ipsilon >/dev/null || \
    useradd -r -g ipsilon -d %{_sharedstatedir}/ipsilon -s /sbin/nologin \
    -c "Ipsilon Server" ipsilon
exit 0


%files filesystem
%doc COPYING README
%dir %{_datadir}/ipsilon
%dir %{_datadir}/ipsilon/templates
%dir %{_datadir}/ipsilon/templates/install
%dir %{python2_sitelib}/ipsilon
%{python2_sitelib}/ipsilon/__init__.py*
%{python2_sitelib}/ipsilon-*.egg-info
%dir %{python2_sitelib}/ipsilon/tools
%{python2_sitelib}/ipsilon/tools/__init__.py*
%{python2_sitelib}/ipsilon/tools/files.py*

%files
%doc %{_mandir}/man*/ipsilon-server-install.1*
%{_sbindir}/ipsilon-server-install
%{_datadir}/ipsilon/templates/install/*.conf
%{_datadir}/ipsilon/ui/saml2sp
%dir %{python2_sitelib}/ipsilon/helpers
%{python2_sitelib}/ipsilon/helpers/common.py*
%{python2_sitelib}/ipsilon/helpers/__init__.py*

%files base
%doc %{_mandir}/man*/ipsilon.7*
%doc %{_mandir}/man*/ipsilon.conf.5*
%{_defaultdocdir}/%{name}-%{version}
%{python2_sitelib}/ipsilon/admin
%{python2_sitelib}/ipsilon/rest
%dir %{python2_sitelib}/ipsilon/login
%{python2_sitelib}/ipsilon/login/__init__*
%{python2_sitelib}/ipsilon/login/common*
%{python2_sitelib}/ipsilon/login/authtest*
%dir %{python2_sitelib}/ipsilon/info
%{python2_sitelib}/ipsilon/info/__init__*
%{python2_sitelib}/ipsilon/info/common*
%{python2_sitelib}/ipsilon/info/infonss*
%dir %{python2_sitelib}/ipsilon/providers
%{python2_sitelib}/ipsilon/providers/__init__*
%{python2_sitelib}/ipsilon/providers/common*
%{python2_sitelib}/ipsilon/root.py*
%{python2_sitelib}/ipsilon/util
%{_datadir}/ipsilon/templates/*.html
%{_datadir}/ipsilon/templates/admin
%dir %{_datadir}/ipsilon/templates/login
%{_datadir}/ipsilon/templates/login/index.html
%{_datadir}/ipsilon/templates/login/form.html
%dir %{_datadir}/ipsilon/ui
%{_datadir}/ipsilon/ui/css
%{_datadir}/ipsilon/ui/img
%{_datadir}/ipsilon/ui/js
%{_datadir}/ipsilon/ui/fonts
%{_libexecdir}/ipsilon
%dir %attr(0751,root,root) %{_sharedstatedir}/ipsilon
%dir %attr(0751,root,root) %{_sysconfdir}/ipsilon

%files client
%doc %{_mandir}/man*/ipsilon-client-install.1*
%{_bindir}/ipsilon-client-install
%{_datadir}/ipsilon/templates/install/saml2

%files tools-ipa
%{python2_sitelib}/ipsilon/helpers/ipa.py*

%files saml2-base
%{python2_sitelib}/ipsilon/tools/saml2metadata.py*
%{python2_sitelib}/ipsilon/tools/certs.py*

%files saml2
%{python2_sitelib}/ipsilon/providers/saml2*
%{_datadir}/ipsilon/templates/saml2

%files persona
%{python2_sitelib}/ipsilon/providers/persona*
%{_datadir}/ipsilon/templates/persona

%files authform
%{python2_sitelib}/ipsilon/login/authform*

%files authgssapi
%{python2_sitelib}/ipsilon/login/authgssapi*
%{_datadir}/ipsilon/templates/login/gssapi.html

%files authldap
%{python2_sitelib}/ipsilon/login/authldap*
%{python2_sitelib}/ipsilon/info/infoldap*

%files infosssd
%{python2_sitelib}/ipsilon/info/infosssd.*


%changelog
* Wed Oct 14 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-12
- Backport patch for CVE-2015-5301 RHBZ#1271666

* Tue Sep 22 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-11
- Fix error during TranStore cleanup RHBZ#1256518

* Thu Sep 10 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-10
- Finish backporting database cleanup RHBZ#1256518

* Tue Sep 08 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-9
- Backport database keys patch RHBZ#1252392
- Backport SAML path check patch RHBZ#1253821
- Backport database cleanup RHBZ#1256518

* Wed Sep 02 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-8
- Moved ipsilon-client-install man page to client subpackage RHBZ#1255103
- Backported patch to count IPA as login plugin RHBZ#1256517
- Backported patch to log error if nameid is invalid RHBZ#1256520
- Backported patch to add city attribute RHBZ#1257213

* Fri Aug 21 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-7
- Added dependency on python-requests for client RHBZ#1254644
- Fixed possible XSS flaws CVE-2015-5215, CVE-2015-5216
- Fixed permission check CVE-2015-5217

* Thu Jul 30 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-6
- Removed gpg key check during build RHBZ#1248529
- Fixed the license tag to include external code RHBZ#1248538
- Use full path url RHBZ#1251149

* Mon Jul 27 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-5
- Backport patch to give more informative errors if password expired

* Wed Jun 17 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-4
- Don't package authpam, the dependencies are not available.

* Mon Jun 15 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-3
- Don't package authfas, the dependencies are not available.

* Thu May 28 2015 Rob Crittenden <rcritten@redhat.com> - 1.0.0-2
- Don't package openid, the dependencies are not available.

* Mon May 11 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-1
- Update to release 1.0.0

* Mon Apr 20 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.6.0-1
- Update to release 0.6.0

* Mon Mar 30 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.5.0-1
- Update to release 0.5.0

* Mon Mar 02 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.4.0-1
- Update to release 0.4.0

* Wed Jan 28 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.3.0-5
- Split IPA tools

* Mon Jan 12 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.3.0-4
- Add symlink to fonts directory

* Tue Dec 16 2014 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.3.0-3
- Fix typo
- Add comments on why the test suite is not in check
- The subpackages require the base package
- Add link to FPC ticket for bundling exception request

* Tue Dec 16 2014 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.3.0-2
- Fix shebang removal

* Tue Dec 16 2014 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.3.0-1
- Initial packaging
