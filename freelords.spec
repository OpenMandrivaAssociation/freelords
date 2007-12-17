%define	name	freelords
%define	version	0.3.7
%define rel         3
%define	release	%mkrel %{rel}
%define	Summary	A Linux clone of the old dos game W*arLords

Summary:	%{Summary}
Name:		%{name}
Version:         %{version}
Release:	%{release}
License:	GPL
Group:		Games/Strategy
Source:		%{name}-%{version}.tar.bz2
URL:		http://sourceforge.net/projects/freelords/
Patch0:         freelords-0.3.7-path.h.patch.bz2
Patch1:         freelords-0.3.7-ai_smart.h.patch.bz2
Patch2:         freelords-0.3.7-scroller.h.patch.bz2
Patch3:         freelords-0.3.7-tooltip.h.patch.bz2
BuildRequires:	libsigc++1.2-devel >= 1.2.0 paragui-devel >= 1.0.4
BuildRequires:  SDL_image-devel >= 1.2.0 
BuildRequires:  SDL_mixer-devel >= 1.2.0  
BuildRequires:	ImageMagick
##add gaming zone support
BuildRequires:  ggz-client-libs-devel
BuildRequires:  ggz-server-devel ggz-server
Obsoletes:	freelords-cvs-sdl
Provides:	freelords-cvs-sdl
Requires(post): ggz-client-libs
Requires(preun): ggz-client-libs


%description
FreeLords is a turn-based strategy game similar to W*rl*rds. 
It can be played with friends on one computer or via a network.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build 

##CAE not needed now
##export LD_LIBRARY_PATH=/usr/X11R6/lib
%configure	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
                --enable-ggz \
                --enable-fullscreen
%make CXXFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir},%{_menudir}}
convert dat/various/%{name}.png -geometry 48x48 %{buildroot}%{_liconsdir}/%{name}.png
convert dat/various/%{name}.png -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert dat/various/%{name}.png -geometry 16x16 %{buildroot}%{_miconsdir}/%{name}.png
  
#fix config locations
mkdir -p %{buildroot}{%{_sysconfdir}/ggzd/games,%{_sysconfdir}/ggzd/rooms}
mv %{buildroot}%{_datadir}/games/%{name}/freelordsrc %{buildroot}%{_sysconfdir}/freelordsrc
mv %{buildroot}%{_usr}/etc/ggzd/games/freelords-server.dsc %{buildroot}%{_sysconfdir}/ggzd/games/freelords-server.dsc
mv %{buildroot}%{_usr}/etc/ggzd/rooms/freelords-server.room %{buildroot}%{_sysconfdir}/ggzd/rooms/freelords-server.room
rm -rfd %{buildroot}%{_usr}/etc/ggzd
ln -s %{_sysconfdir}/freelordsrc %{buildroot}%{_datadir}/games/%{name}/freelordsrc 
ln -s %{_sysconfdir}/ggzd %{buildroot}%{_usr}/etc/ggzd

cat > %{buildroot}%{_menudir}/%{name} << EOF
?package(%{name}):\
	command="%{_gamesbindir}/%{name}" \
	icon="%{name}.png" \
	title="FreeLords" \
	longtitle="%{Summary}" \
	needs="x11" \
	section="More Applications/Games/Strategy"
EOF

%find_lang %{name} 

rm -f %buildroot%{_sysconfdir}/ggz.modules

%post
%{update_menus}
ggz-config -i -f -m %_sysconfdir/ggzd/games/freelords-server.dsc  >& /dev/null || :

%preun
ggz-config -r -m %_sysconfdir/ggzd/games/freelords-server.dsc  >& /dev/null || :

%postun
%{clean_menus}

%clean
rm -rf %{buildroot} 

%files  -f %{name}.lang
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS BUGS COPYING ChangeLog DEPENDENCIES HACKER INSTALL NEWS README TODO
%doc doc/*
%config(noreplace) %{_sysconfdir}/freelordsrc
%dir %{_sysconfdir}/ggzd
%config(noreplace) %{_sysconfdir}/ggzd/games/freelords-server.dsc
%config(noreplace) %{_sysconfdir}/ggzd/rooms/freelords-server.room 
%{_prefix}/etc/ggzd
%{_gamesbindir}/freelords*
%{_gamesdatadir}/%{name} 
%{_gamesdatadir}/applications/*
%{_menudir}/%{name} 
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%dir %{_gamesdatadir}/locale
%lang(de) %{_gamesdatadir}/locale/de/LC_MESSAGES/freelords.mo
%lang(hi) %{_gamesdatadir}/locale/hi/LC_MESSAGES/freelords.mo
%lang(it) %{_gamesdatadir}/locale/it/LC_MESSAGES/freelords.mo

