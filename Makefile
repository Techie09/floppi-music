doc/img/floppi-icon_128.png: doc/img/floppi-icon.svg
	convert -scale x128 $< $@

doxygen: doc/img/floppi-icon_128.png
	doxygen Doxyfile

gh-pages: doxygen
	t=$$(mktemp -d); cp -r doc/doxygen/html/* "$$t"; git checkout gh-pages; cp -r "$$t"/* .; git add *; git commit -a -m "gh-pages"; git checkout master

.PHONY: doxygen gh-pages
	