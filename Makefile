# local make srpm
SPECS  := umbriel.spec xdg-desktop-portal-umbriel.spec vm-curator.spec mangowm.spec scenefx.spec megasync.spec megacmd.spec
TOPDIR := $(CURDIR)/rpmbuild

srpm:
	mkdir -p $(TOPDIR)/SOURCES $(TOPDIR)/SRPMS
	for s in $(SPECS); do spectool -g --directory $(TOPDIR)/SOURCES $$s; done
	rpmbuild -bs --define '_topdir $(TOPDIR)' --define '_sourcedir $(TOPDIR)/SOURCES' $(SPECS)

clean:
	rm -rf $(TOPDIR)

.PHONY: srpm clean
