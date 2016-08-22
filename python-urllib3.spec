# TODO: use system six, [backports.]ssl_match_hostname
#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_with	tests	# test target (uses network etc.)
#
%define 	module	urllib3
Summary:	HTTP library with thread-safe connection pooling, file post, and more
Summary(pl.UTF-8):	Biblioteka HTTP z bezpieczną wątkowo pulą połączeń, wysyłaniem plików itd.
Name:		python-%{module}
Version:	1.16
Release:	1
License:	MIT
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/3b/f0/e763169124e3f5db0926bc3dbfcd580a105f9ca44cf5d8e6c7a803c9f6b5/%{module}-%{version}.tar.gz
# Source0-md5:	fcaab1c5385c57deeb7053d3d7d81d59
URL:		http://urllib3.readthedocs.org/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
%if %{with tests}
BuildRequires:	python-PySocks >= 1.5.6
BuildRequires:	python-PySocks < 2.0
BuildRequires:	python-mock
BuildRequires:	python-nose
BuildRequires:	python-tornado
# SO_REUSEPORT option
BuildRequires:	uname(release) >= 3.9
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
BuildRequires:	python3-PySocks >= 1.5.6
BuildRequires:	python3-PySocks < 2.0
BuildRequires:	python3-nose
BuildRequires:	python3-tornado
# SO_REUSEPORT option
BuildRequires:	uname(release) >= 3.9
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 2 HTTP module with connection pooling and file POST abilities.
Features are:
- Re-use the same socket connection for multiple requests (with
  optional client-side certificate verification).
- File posting (encode_multipart_formdata).
- Built-in redirection and retries (optional).
- Supports gzip and deflate decoding.
- Thread-safe and sanity-safe.

%description -l pl.UTF-8
Moduł HTTP dla Pythona 2 z pulą połączeń i możliwością wysyłania
plików metodą POST. Możliwości:
- używanie tego samego połączenia dla wielu żądań (z opcjonalną
  weryfikacją certyfikatu po stronie klienta)
- wysyłanie plików (encode_multipart_formdata)
- wbudowane przekierowania i ponawianie prób (opcjonalne)
- obsługa kodowań gzip i deflate
- bezpieczeństwo względem wątków.

%package -n python3-urllib3
Summary:	HTTP library with thread-safe connection pooling, file post, and more
Summary(pl.UTF-8):	Biblioteka HTTP z bezpieczną wątkowo pulą połączeń, wysyłaniem plików itd.
Group:		Development/Languages/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-urllib3
Python 3 HTTP module with connection pooling and file POST abilities.
Features are:
- Re-use the same socket connection for multiple requests (with
  optional client-side certificate verification).
- File posting (encode_multipart_formdata).
- Built-in redirection and retries (optional).
- Supports gzip and deflate decoding.
- Thread-safe and sanity-safe.

%description -n python3-urllib3 -l pl.UTF-8
Moduł HTTP dla Pythona 3 z pulą połączeń i możliwością wysyłania
plików metodą POST. Możliwości:
- używanie tego samego połączenia dla wielu żądań (z opcjonalną
  weryfikacją certyfikatu po stronie klienta)
- wysyłanie plików (encode_multipart_formdata)
- wbudowane przekierowania i ponawianie prób (opcjonalne)
- obsługa kodowań gzip i deflate
- bezpieczeństwo względem wątków.

%prep
%setup -q -n %{module}-%{version}

# this test requires Google App Engine SDK
%{__rm} test/contrib/test_gae_manager.py

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# already in Python 2.7+
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/urllib3/packages/ordered_dict.py*
%py_postclean
%endif

%if %{with python3}
%py3_install

# already in Python 2.7+
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/urllib3/packages/{ordered_dict.py,__pycache__/ordered_dict.*.py*}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt LICENSE.txt README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-urllib3
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
