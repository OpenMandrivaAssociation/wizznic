
#define debug_package	%{nil}
Name:           wizznic
Summary:        An implementation of Puzznic
Version:        0.9.9
Release:        3
License:        GPLv3
Group:          Games/Boards
Source:         http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.bz2
Source1:        %{name}.desktop
Patch0:         %{name}-linux.patch
Url:            http://sourceforge.net/projects/wizznic/
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(SDL_image)
BuildRequires:  pkgconfig(SDL_mixer)
BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(libpng)

%description
Wizznic is an implementation of Puzznic.
It is made very easy for non-programmers to contribute Levels/Graphics and
sounds. 

%prep
%setup -q -n wizznic-0.9.9-src
%patch0 -p0


%build
export CFLAGS="$RPM_OPT_FLAGS"
%make DATADIR="%{_datadir}/%{name}/" %{?_smp_mflags} -f Makefile.linux

# Create wrapper script
echo -e "#!/bin/bash\ncd %{_datadir}/%{name}/\n%{_bindir}/%{name}-bin \$*\n" > %{name}-wrapper.sh


%install
# install binaries
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 %{name} %{buildroot}%{_bindir}/%{name}-bin
install -p -m 755 %{name}-wrapper.sh %{buildroot}%{_bindir}/%{name}

# install menu entry
mkdir -p %{buildroot}%{_datadir}/applications
install -p %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

# install icons
install -d -D -m 755 %{buildroot}%{_datadir}/pixmaps/
ln -s %{_datadir}/%{name}/data/wmicon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

# install game data
install -d -m755 %{buildroot}%{_datadir}/%{name}
cp -Rf data %{buildroot}%{_datadir}/%{name}/data
cp -Rf packs %{buildroot}%{_datadir}/%{name}/packs

%post
chmod -R 755 %{_datadir}/%{name}

%files
%defattr(-,root,root,-)
%doc doc/changelog.txt  doc/credits.txt  doc/install.txt  doc/media-licenses.txt  doc/music-score-credits.txt  doc/ports.txt  doc/readme.txt
%{_bindir}/%{name}
%{_bindir}/%{name}-bin
%{_datadir}/%{name}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

