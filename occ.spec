# TODO: verify/complete webserver configs (only apache 2.4 tested)
Summary:	Online Chess Club - small PHP chess game
Summary(pl.UTF-8):	Online Chess Club - mała gra w szachy w PHP
Name:		occ
Version:	1.4
Release:	2
License:	GPL v2
Group:		Applications/WWW
Source0:	https://downloads.sourceforge.net/lgames/%{name}-%{version}.tar.gz
# Source0-md5:	4bffaa7dac327bc932e563b5142462e6
Source1:	apache.conf
Source2:	lighttpd.conf
Patch0:		%{name}-datadir.patch
URL:		https://lgames.sourceforge.net/OCC/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php(session)
Requires:	webapps
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%define		_noautoreq_pear	.*

%description
Online Chess Club (OCC) is a small PHP chess game. It is not meant for
public use but rather for playing with friends. Any number of games
can be opened and the idea is to check once in a while (like once a
day) whether somebody has moved and if so respond along with a
comment. While it is possible to play a quick game by hitting Refresh
frequently or using a chat tool for communication this is not the aim
of OCC. Other online chess games may fit this purpose better.

OCC stores all moves of a game (can be replayed in history browser)
and automatically recognizes checkmate and stalemate. A draw can be
proposed at any time (opponent needs to agree). When a game is
finished it is archived. All games can be saved as PGN to analyse them
with your favorite chess tool, e.g., with Fritz.

%description -l pl.UTF-8
Online Chess Club (OCC) to mała gra w szachy napisana w PHP. Nie jest
przeznaczona do użytku publicznego, raczej do grania ze znajomymi.
Można rozpocząć dowolną liczbę gier, a idea polaga na tym, żeby
sprawdzać co jakiś czas (np. raz dziennie), czy ktoś się ruszył i
reagować na ruch wraz z komentarzem. O ile możliwa jest szybka
rozgrywka poprzez częste wciskanie przycisku "Refresh" albo
wykorzystywanie komunikatora do komunikacji, nie jest to celem OCC -
inne gry w szachy online mogą być lepsze do tego celu.

OCC zapisuje wszystkie ruchy z gry (można je odtworzyć w przeglądarce
historii) i automatycznie rozpoznaje sytuacje mata i pata. W każdej
chwili można zaproponować remis (za zgodą przeciwnika). Po zakończeniu
gra jest archiwizowana. Wszystkie gry można zapisać w formacie PGN w
celu przeanalizowania dowolnym narzędziem, np. Fritzem.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},/var/lib/%{name}}

cp -a images *.php *.js $RPM_BUILD_ROOT%{_appdir}
cp -a occ-data tmp $RPM_BUILD_ROOT/var/lib/%{name}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc Changelog README
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}
%attr(710,root,http) %dir /var/lib/%{name}
%attr(710,root,http) %dir /var/lib/%{name}/occ-data
%attr(770,root,http) %dir /var/lib/%{name}/occ-data/archive
%attr(770,root,http) %dir /var/lib/%{name}/occ-data/games
%attr(710,root,http) %dir /var/lib/%{name}/occ-data/users
%attr(770,root,http) %dir /var/lib/%{name}/occ-data/users/lhistory
%attr(770,root,http) %dir /var/lib/%{name}/occ-data/users/notes
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{name}/occ-data/users/accounts.php
%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{name}/occ-data/users/stats
%attr(770,root,http) %dir /var/lib/%{name}/tmp
