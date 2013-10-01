install:
	cat requirements_apt.txt | apt-get install
	pip install -r requirements_pip.txt
	cd "filters_package";\
		python cython_functions_setup.py build_ext --inplace;\
		python cython_functions_setup.py clean
