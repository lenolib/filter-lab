#Compile with: python setup.py build_ext --compiler=mingw32 --inplace
#It might be necessary to delete the files "cython_functions.c" and 
#"cython_functions.pyd" beforehand.  

if __name__ == "__main__":
	import numpy
	from distutils.core import setup
	from distutils.extension import Extension
	from Cython.Distutils import build_ext
	ext_modules = [
		Extension("cython_functions", 
				  ["cython_functions.pyx"],
				  )
		]

	setup(name = 'Cython image functions',      
		  cmdclass = {'build_ext': build_ext},
		  ext_modules = ext_modules,
		  include_dirs=[numpy.get_include()])
