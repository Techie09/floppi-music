doc/img/floppi-icon_128.png: doc/img/floppi-icon.svg
	convert -scale x128 $< $@

doxygen: doc/img/floppi-icon_128.png
	doxygen Doxyfile

.PHONY: doxygen
	