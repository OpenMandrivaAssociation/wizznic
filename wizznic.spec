
Name:           wizznic
BuildRequires:  SDL-devel SDL_image-devel SDL_mixer-devel libpng-devel
Summary:        An implementation of Puzznic
Version:        0.9.9
Release:        %mkrel 1
License:        GPL
Group:          Games/Boards
# Downloaded from sourceforge.
# Removed binaries and Windows BAT files
Source:         http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.bz2
Source1:        %{name}.desktop
# Linux makefile and user data patch
# Submitted to SourceForge project:
# https://sourceforge.net/tracker/?func=detail&aid=2925556&group_id=286702&atid=1214849
# PATCH-FIX-UPSTREAM wizznic-linux.patch PVince81@yahoo.fr
Patch0:         %{name}-linux.patch
Patch1:         wizznic-implicit-decl.patch
Url:            http://sourceforge.net/projects/wizznic/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  fdupes


%description
Wizznic is an implementation of Puzznic.
It is made very easy for non-programmers to contribute Levels/Graphics and sounds. 

%prep
%setup -q -n wizznic-0.9.9-src
# %patch0 -p1
# %patch1 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"
make DATADIR="%{_gamesdatadir}/%{name}" %{?_smp_mflags} -f Makefile.linux

# Removing userlevels directory, this one will be created in the user's home
# rmdir data/userlevels

# Create wrapper script
echo -e "#!/bin/bash\ncd %{_gamesdatadir}/%{name}/\n%{_bindir}/%{name}-bin \$*\n" > %{name}-wrapper.sh

%install
make DESTDIR="%{buildroot}" DATADIR="%{_gamesdatadir}/%{name}" -f Makefile.linux install
# Remove doc, as it will be included later
rm %{buildroot}/%{_gamesdatadir}/%{name}/data/media-licenses.txt
install -D -m 644 %{S:1} %{buildroot}/%{_gamesdatadir}/applications/%{name}.desktop
install -d -D -m 755 %{buildroot}/%{_gamesdatadir}/pixmaps/
ln -s %{_gamesdatadir}/%{name}/data/wmicon.png %{buildroot}/%{_gamesdatadir}/pixmaps/%{name}.png

# install wrapper script
mv %{buildroot}/%{_bindir}/%{name} %{buildroot}/%{_bindir}/%{name}-bin
install -D -m 755 %{name}-wrapper.sh %{buildroot}/%{_bindir}/%{name}


%files
%defattr(-,root,root,-)
%doc data/media-licenses.txt changelog.txt readme.txt
%{_bindir}/%{name}
%{_bindir}/%{name}-bin
%dir %{_gamesdatadir}/%{name}/
%{_gamesdatadir}/%{name}/*
%{_gamesdatadir}/applications/%{name}.desktop
%{_gamesdatadir}/pixmaps/%{name}.png

