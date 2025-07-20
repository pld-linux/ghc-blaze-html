#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	blaze-html
Summary:	A blazingly fast HTML combinator library for Haskell
Summary(pl.UTF-8):	Biblioteka olśniewająco szybkiego kombinatora HTML dla Haskella
Name:		ghc-%{pkgname}
Version:	0.9.1.2
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/blaze-html
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	a1b7997875d18d26b13de20aa032e2ec
URL:		http://hackage.haskell.org/package/blaze-html
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-blaze-builder >= 0.3
BuildRequires:	ghc-blaze-builder < 0.5
BuildRequires:	ghc-blaze-markup >= 0.8
BuildRequires:	ghc-blaze-markup < 0.9
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-bytestring < 0.11
BuildRequires:	ghc-text >= 0.10
BuildRequires:	ghc-text < 1.3
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-blaze-builder-prof >= 0.3
BuildRequires:	ghc-blaze-builder-prof < 0.5
BuildRequires:	ghc-blaze-markup-prof >= 0.8
BuildRequires:	ghc-blaze-markup-prof < 0.9
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-bytestring-prof < 0.11
BuildRequires:	ghc-text-prof >= 0.10
BuildRequires:	ghc-text-prof < 1.3
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4
Requires:	ghc-base < 5
Requires:	ghc-blaze-builder >= 0.3
Requires:	ghc-blaze-builder < 0.5
Requires:	ghc-blaze-markup >= 0.8
Requires:	ghc-blaze-markup < 0.9
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-bytestring < 0.11
Requires:	ghc-text >= 0.10
Requires:	ghc-text < 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
A blazingly fast HTML combinator library for the Haskell programming
language.

%description -l pl.UTF-8
Biblioteka olśniewająco szybkiego kombinatora HTML dla języka
programowania Haskell.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-base-prof < 5
Requires:	ghc-blaze-builder-prof >= 0.3
Requires:	ghc-blaze-builder-prof < 0.5
Requires:	ghc-blaze-markup-prof >= 0.8
Requires:	ghc-blaze-markup-prof < 0.9
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-bytestring-prof < 0.11
Requires:	ghc-text-prof >= 0.10
Requires:	ghc-text-prof < 1.3

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for %{pkgname} ghc package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname} ghc package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSblaze-html-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSblaze-html-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSblaze-html-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html/Renderer
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html/Renderer/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html/Renderer/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/FrameSet
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/FrameSet/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/FrameSet/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/Strict
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/Strict/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/Strict/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/Transitional
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/Transitional/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/Transitional/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html5
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html5/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html5/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/FrameSet
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/FrameSet/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/FrameSet/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/Strict
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/Strict/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/Strict/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/Transitional
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/Transitional/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/Transitional/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml5
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml5/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml5/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSblaze-html-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html/Renderer/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/FrameSet/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/Strict/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html4/Transitional/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/Html5/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/FrameSet/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/Strict/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml1/Transitional/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Blaze/XHtml5/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
