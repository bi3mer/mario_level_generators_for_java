average_linker_size:
	mv LinkerScripts/average_linker_size.py .;
	-pypy3 average_linker_size.py;
	echo
	mv average_linker_size.py LinkerScripts/average_linker_size.py;
	
build_link:
	mv LinkerScripts/build_link.py .;
	echo
	-pypy3 build_link.py;
	echo
	mv build_link.py LinkerScripts/build_link.py;