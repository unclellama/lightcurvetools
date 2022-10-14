import setuptools

setuptools.setup(name='lightcurvetools',
        version='0.1',
        description='a class for 3-column lightcurves, loading, smoothing etc',
        url='#',
        author='max',
        install_requires=['numpy',
                    'matplotlib',
                    'astropy',
                    'scipy'],
        author_email='unclellama@gmail.com',
        packages=setuptools.find_packages(),
        zip_safe=False)