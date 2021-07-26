from setuptools import setup

version = '2.0'

setup(name='pki-tutorial',
      version=version,
      description='OpenSSL PKI Tutorial NG',
      author='Stefan H. Holek, Matthias R. Wiora',
      author_email='stefan@epy.co.at, matthias@wiora.co.uk',
      url='http://pki-tutorial-ng.readthedocs.org/',
      license='CC',
      zip_safe=False,
      install_requires=[
          'setuptools',
          'sphinx',
          'pygments-openssl',
      ],
)
