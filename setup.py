from setuptools import setup

version = '1.1'

setup(name='pki-tutorial',
      version=version,
      description='OpenSSL PKI Tutorial',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='http://pki-tutorial.readthedocs.org/',
      license='CC',
      zip_safe=False,
      install_requires=[
          'setuptools',
          'sphinx',
          'pygments-openssl',
      ],
)
