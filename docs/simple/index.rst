.. SSLCA documentation master file, created by
   sphinx-quickstart on Sat May 19 14:30:39 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. highlight:: bash

==============================================================================
Simple PKI
==============================================================================

The Simple PKI consists of one root CA and one signing CA.



Overview
========

We assume an organisation named **Simple Inc**, controlling the domain
simple.org.
The organisation runs a small PKI to secure its email and intranet traffic.

.. image:: ../_static/SimplePKILayout.png
   :width: 467
   :height: 394

To construct the PKI, we first create the Simple Root CA and its CA certificate.
We then use the root CA to create the Simple Signing CA.
Once the CAs are in place, we issue an email-protection certificate
to employee Fred Flintstone and a TLS-server certificate to the webserver at
www.simple.org.
Finally, we look at the output formats the CA needs to support and show
how to view the contents of files we have created.

All commands are ready to be copy/pasted into a terminal session.
When you have reached the end of this page, you will have performed
all operations you are likely to encounter in a PKI.

To get started, fetch the Simple PKI example files and change into the
new directory::

    git clone https://bitbucket.org/stefanholek/pki-example-1
    cd pki-example-1


Configuration Files
===================

We use one configuration file per CA:

.. toctree::
   :maxdepth: 2
   :titlesonly:

   root-ca.conf
   signing-ca.conf

And one configuration file per CSR type:

.. toctree::
   :maxdepth: 2
   :titlesonly:

   email.conf
   server.conf

Please familiarize yourself with the configuration files before you continue.


1. Create Root CA
==================

1.1 Create directories
------------------------
::

    mkdir -p ca/root-ca/private ca/root-ca/db crl certs
    chmod 700 ca/root-ca/private

The ``ca`` directory holds CA resources, the ``crl`` directory holds CRLs, and
the ``certs`` directory holds user certificates.

1.2 Create database
---------------------
::

    cp /dev/null ca/root-ca/db/root-ca.db
    cp /dev/null ca/root-ca/db/root-ca.db.attr
    echo 01 > ca/root-ca/db/root-ca.crt.srl
    echo 01 > ca/root-ca/db/root-ca.crl.srl

The database files must exist before the ``openssl ca`` command can be used.
The file contents are described in :doc:`../cadb`.

1.3 Create CA request
-----------------------
::

    openssl req -new \
        -config etc/root-ca.conf \
        -out ca/root-ca.csr \
        -keyout ca/root-ca/private/root-ca.key

With the ``openssl req -new`` command we create a private key and a certificate
signing request (CSR) for the root CA.
You will be asked for a passphrase to protect the private key.
The ``openssl req`` command takes its configuration from the [req] section of the
:doc:`configuration file <root-ca.conf>`.

1.4 Create CA certificate
---------------------------
::

    openssl ca -selfsign \
        -config etc/root-ca.conf \
        -in ca/root-ca.csr \
        -out ca/root-ca.crt \
        -extensions root_ca_ext

With the ``openssl ca`` command we issue a root CA certificate based
on the CSR.
The root certificate is self-signed and serves as the starting point for
all trust relationships in the PKI.
The ``openssl ca`` command takes its configuration from the [ca] section of the
:doc:`configuration file <root-ca.conf>`.


2. Create Signing CA
=====================

2.1 Create directories
------------------------
::

    mkdir -p ca/signing-ca/private ca/signing-ca/db crl certs
    chmod 700 ca/signing-ca/private

The ``ca`` directory holds CA resources, the ``crl`` directory holds
CRLs, and the ``certs`` directory holds user certificates. We will use this
layout for all CAs in this tutorial.

2.2 Create database
---------------------
::

    cp /dev/null ca/signing-ca/db/signing-ca.db
    cp /dev/null ca/signing-ca/db/signing-ca.db.attr
    echo 01 > ca/signing-ca/db/signing-ca.crt.srl
    echo 01 > ca/signing-ca/db/signing-ca.crl.srl

The contents of these files are described in :doc:`../cadb`.

2.3 Create CA request
-----------------------
::

    openssl req -new \
        -config etc/signing-ca.conf \
        -out ca/signing-ca.csr \
        -keyout ca/signing-ca/private/signing-ca.key

With the ``openssl req -new`` command we create a private key and a CSR for
the signing CA.
You will be asked for a passphrase to protect the private key.
The ``openssl req`` command takes its configuration from the [req] section of the
:doc:`configuration file <signing-ca.conf>`.

2.4 Create CA certificate
---------------------------
::

    openssl ca \
        -config etc/root-ca.conf \
        -in ca/signing-ca.csr \
        -out ca/signing-ca.crt \
        -extensions signing_ca_ext

With the ``openssl ca`` command we issue a certificate based on the CSR.
The command takes its configuration from the [ca] section of the
:doc:`configuration file <root-ca.conf>`.
Note that it is the root CA that issues the signing CA certificate!
Note also that we attach a different set of extensions.


3. Operate Signing CA
======================

3.1 Create email request
--------------------------
::

    openssl req -new \
        -config etc/email.conf \
        -out certs/fred.csr \
        -keyout certs/fred.key

With the ``openssl req -new`` command we create the private key and CSR for an
email-protection certificate. We use a :doc:`request configuration file
<email.conf>` specifically prepared for the task.
When prompted enter these DN components:
DC=org, DC=simple, O=Simple Inc, CN=Fred Flintstone,
emailAddress=fred\@simple.org. Leave other fields empty.

3.2 Create email certificate
------------------------------
::

    openssl ca \
        -config etc/signing-ca.conf \
        -in certs/fred.csr \
        -out certs/fred.crt \
        -extensions email_ext

We use the signing CA to issue the email-protection certificate. The
certificate type is defined by the extensions we attach.
A copy of the certificate is saved in the certificate archive under the name
``ca/signing-ca/01.pem`` (01 being the certificate serial number in hex.)

3.3 Create server request
---------------------------
::

    SAN=DNS:www.simple.org \
    openssl req -new \
        -config etc/server.conf \
        -out certs/simple.org.csr \
        -keyout certs/simple.org.key

Next we create the private key and CSR for a TLS-server certificate, using a
different :doc:`request configuration file <server.conf>`.
When prompted enter these DN components:
DC=org, DC=simple, O=Simple Inc, CN=www.simple.org.
Note that the subjectAltName must be specified as environment variable.
Note also that server keys typically have no passphrase.

3.4 Create server certificate
-------------------------------
::

    openssl ca \
        -config etc/signing-ca.conf \
        -in certs/simple.org.csr \
        -out certs/simple.org.crt \
        -extensions server_ext

We use the signing CA to issue the TLS-server certificate. The certificate
type is defined by the extensions we attach.
A copy of the certificate is saved in the certificate archive under the name
``ca/signing-ca/02.pem``.

3.5 Revoke certificate
------------------------
::

    openssl ca \
        -config etc/signing-ca.conf \
        -revoke ca/signing-ca/01.pem \
        -crl_reason superseded

Certain events, like certificate replacement or loss of private key, require a
certificate to be revoked before its scheduled expiration date. The ``openssl ca
-revoke`` command marks a certificate as revoked in the CA database. It will
from then on be included in CRLs issued by the CA.
The above command revokes the certificate with serial number 01 (hex).

3.6 Create CRL
----------------
::

    openssl ca -gencrl \
        -config etc/signing-ca.conf \
        -out crl/signing-ca.crl

The ``openssl ca -gencrl`` command creates a certificate revocation list
(CRL).
The CRL contains all revoked, not-yet-expired certificates from the CA
database.
A new CRL must be issued at regular intervals.


4. Output Formats
===================

4.1 Create DER certificate
----------------------------
::

    openssl x509 \
        -in certs/fred.crt \
        -out certs/fred.cer \
        -outform der

All published certificates must be in DER format [:rfc:`2585#section-3`].
Also see :doc:`../mime`.

4.2 Create DER CRL
--------------------
::

    openssl crl \
        -in crl/signing-ca.crl \
        -out crl/signing-ca.crl \
        -outform der

All published CRLs must be in DER format [:rfc:`2585#section-3`].
Also see :doc:`../mime`.

4.3 Create PKCS#7 bundle
--------------------------
::

    openssl crl2pkcs7 -nocrl \
        -certfile ca/signing-ca.crt \
        -certfile ca/root-ca.crt \
        -out ca/signing-ca-chain.p7c \
        -outform der

PKCS#7 is used to bundle two or more certificates. The format would
also allow for CRLs but they are not used in practice.

4.4 Create PKCS#12 bundle
---------------------------
::

    openssl pkcs12 -export \
        -name "Fred Flintstone" \
        -inkey certs/fred.key \
        -in certs/fred.crt \
        -out certs/fred.p12

PKCS#12 is used to bundle a certificate and its private key.
Additional certificates may be added, typically the certificates comprising
the chain up to the Root CA.

4.5 Create PEM bundle
-----------------------
::

    cat ca/signing-ca.crt ca/root-ca.crt > \
        ca/signing-ca-chain.pem

    cat certs/fred.key certs/fred.crt > \
        certs/fred.pem

PEM bundles are created by concatenating other PEM-formatted files. Both
"cert chain" and "key + cert" versions are in use.


5. View Results
================

5.1 View request
------------------
::

    openssl req \
        -in certs/fred.csr \
        -noout \
        -text

The ``openssl req`` command can be used to display the contents of CSR files.
The ``-noout`` and ``-text`` options select a human-readable output format.

5.2 View certificate
----------------------
::

    openssl x509 \
        -in certs/fred.crt \
        -noout \
        -text

The ``openssl x509`` command can be used to display the contents of
certificate files.
The ``-noout`` and ``-text`` options have the same purpose as before.

5.3 View CRL
--------------
::

    openssl crl \
        -in crl/signing-ca.crl \
        -inform der \
        -noout \
        -text

The ``openssl crl`` command can be used to view the contents of CRL files.
Note that we specify ``-inform der`` because we have already converted the CRL
in step 4.2.

5.4 View PKCS#7 bundle
------------------------
::

    openssl pkcs7 \
        -in ca/signing-ca-chain.p7c \
        -inform der \
        -noout \
        -text \
        -print_certs

The ``openssl pkcs7`` command can be used to display the contents of PKCS#7
bundles.

5.5 View PKCS#12 bundle
-------------------------
::

    openssl pkcs12 \
        -in certs/fred.p12 \
        -nodes \
        -info

The ``openssl pkcs12`` command can be used to display the contents of PKCS#12
bundles.


References
======================

* http://openssl.org/docs/apps/req.html
* http://openssl.org/docs/apps/ca.html
* http://openssl.org/docs/apps/x509.html
* http://openssl.org/docs/apps/crl.html
* http://openssl.org/docs/apps/crl2pkcs7.html
* http://openssl.org/docs/apps/pkcs7.html
* http://openssl.org/docs/apps/pkcs12.html

