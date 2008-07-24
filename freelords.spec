Summary:	A Linux clone of the old DOS game WarLords
Name:		freelords
Version:        0.3.8
Release:	%mkrel 3
License:	GPLv2+
Group:		Games/Strategy
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source:		%{name}-%{version}.tar.bz2
URL:		http://sourceforge.net/projects/freelords/
BuildRequires:	libsigc++1.2-devel >= 1.2.0 
BuildRequires:	paragui-devel >= 1.1.8
BuildRequires:	SDL_image-devel >= 1.2.0 
BuildRequires:	SDL_mixer-devel >= 1.2.0  
BuildRequires:	ImageMagick
# paragui test fails without this...
BuildRequires:	freetype2-devel
##add gaming zone support
BuildRequires:	ggz-client-libs-devel
BuildRequires:	ggz-server-devel ggz-server
Obsoletes:	freelords-cvs-sdl
Provides:	freelords-cvs-sdl

Requires(post):		ggz-client-libs
Requires(preun):	ggz-client-libs


%description
FreeLords is a turn-based strategy game similar to Warlords. 
It can be played with friends on one computer or via a network.

%prep
%setup -q

%build 
%configure2_5x	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
                --enable-fullscreen
%make CXXFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert dat/various/%{name}.png -scale 48x48 %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert dat/various/%{name}.png -scale 32x32 %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert dat/various/%{name}.png -scale 16x16 %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
  
#fix config locations
#mkdir -p %{buildroot}{%{_sysconfdir}/ggzd/games,%{_sysconfdir}/ggzd/rooms}
#mv %{buildroot}%{_datadir}/games/%{name}/freelordsrc %{buildroot}%{_sysconfdir}/freelordsrc
#mv %{buildroot}%{_usr}/etc/ggzd/games/freelords-server.dsc %{buildroot}%{_sysconfdir}/ggzd/games/freelords-server.dsc
#mv %{buildroot}%{_usr}/etc/ggzd/rooms/freelords-server.room %{buildroot}%{_sysconfdir}/ggzd/rooms/freelords-server.room
#rm -rfd %{buildroot}%{_usr}/etc/ggzd
#ln -s %{_sysconfdir}/freelordsrc %{buildroot}%{_datadir}/games/%{name}/freelordsrc 
#ln -s %{_sysconfdir}/ggzd %{buildroot}%{_usr}/etc/ggzd
rm -rf %{buildroot}%{_gamesdatadir}/applications
test -e %{buildroot}%{_gamesdatadir}/locale/locale.alias && rm -f %{buildroot}%{_gamesdatadir}/locale/locale.alias

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=FreeLords
Comment=A Linux clone of the old DOS game WarLords
Exec=%{_gamesbindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;StrategyGame;
EOF

%find_lang %{name} 

#rm -f %{buildroot}%{_sysconfdir}/ggz.modules

%post
%if %mdkversion < 200900
%{update_menus}
%endif
#ggz-config -i -f -m %{_sysconfdir}/ggzd/games/freelords-server.dsc  >& /dev/null || :

%preun
#ggz-config -r -m %{_sysconfdir}/ggzd/games/freelords-server.dsc  >& /dev/null || :

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf %{buildroot} 

%files  -f %{name}.lang
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS ChangeLog DEPENDENCIES HACKER NEWS README TODO
%doc doc/*
#%config(noreplace) %{_sysconfdir}/freelordsrc
#%dir %{_sysconfdir}/ggzd
#%config(noreplace) %{_sysconfdir}/ggzd/games/freelords-server.dsc
#%config(noreplace) %{_sysconfdir}/ggzd/rooms/freelords-server.room 
#%{_prefix}/etc/ggzd
%{_gamesbindir}/freelords*
%{_gamesdatadir}/%{name} 
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%dir %{_gamesdatadir}/locale
%lang(de) %{_gamesdatadir}/locale/de/LC_MESSAGES/freelords.mo
%lang(hi) %{_gamesdatadir}/locale/hi/LC_MESSAGES/freelords.mo
%lang(it) %{_gamesdatadir}/locale/it/LC_MESSAGES/freelords.mo
%lang(pl) %{_gamesdatadir}/locale/pl/LC_MESSAGES/freelords.mo

