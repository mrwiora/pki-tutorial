.. SSLCA documentation master file, created by
   sphinx-quickstart on Sat May 19 14:30:39 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. highlight:: bash

Advanced PKI
==============================================================================

The Advanced PKI consists of a root CA and a layer of subordinate CAs.


.. toctree::
   :hidden:

   root-ca.conf
   email-ca.conf
   network-ca.conf
   software-ca.conf
   email-client.conf
   tls-server.conf
   tls-client.conf
   code-signing.conf


Overview
========

We assume a company named **Fnord AS**, controlling the domain fnord.no.
It runs a three-pronged PKI to serve its security needs.
To implement the PKI, we first create the Fnord Root CA and its CA
certificate. We then use the root CA to create three signing CAs:

#. Fnord Email CA
#. Fnord Network CA
#. Fnord Software CA

Subsequently we show each CA in operation.

All commands are ready to be copy/pasted into a terminal session.
When you have reached the end of this page, you will have built
and operated a real-life PKI.

To get started, fetch the Advanced PKI example files and change into the
new directory::

    git clone https://bitbucket.org/stefanholek/pki-example-2
    cd pki-example-2

Layout
======

.. image:: ../_static/AdvancedPKILayout.gif
   :width: 490
   :height: 442

We use one configuration file per CA:

* :doc:`root-ca.conf`
* :doc:`email-ca.conf`
* :doc:`network-ca.conf`
* :doc:`software-ca.conf`

And one configuration file per CSR type:

* :doc:`email-client.conf`
* :doc:`tls-server.conf`
* :doc:`tls-client.conf`
* :doc:`code-signing.conf`

Please study the configuration files before you continue.


\1. Create Root CA
==================

\1.1 Create directories
-----------------------
::

    mkdir -p ca/root-ca/private ca/root-ca/db crl certs
    chmod 700 ca/root-ca/private

\1.2 Create database
--------------------
::

    cp /dev/null ca/root-ca/db/root-ca.db
    cp /dev/null ca/root-ca/db/root-ca.db.attr
    echo 01 > ca/root-ca/db/root-ca.crt.srl
    echo 01 > ca/root-ca/db/root-ca.crl.srl

\1.3 Create CA request
----------------------
::

    openssl req -new \
        -config etc/root-ca.conf \
        -out ca/root-ca.csr \
        -keyout ca/root-ca/private/root-ca.key

\1.4 Create CA certificate
--------------------------
::

    openssl ca -selfsign \
        -config etc/root-ca.conf \
        -in ca/root-ca.csr \
        -out ca/root-ca.crt \
        -enddate 310101000000Z \
        -extensions rootca_ext

2048-bit RSA keys are deemed safe until 2030 (`RSA Labs`_).

.. _`RSA Labs`: http://www.rsa.com/rsalabs/node.asp?id=2004

\1.5 Create initial CRL
-----------------------
::

    openssl ca -gencrl \
        -config etc/root-ca.conf \
        -out crl/root-ca.crl


\2. Create Email CA
===================

\2.1 Create directories
-----------------------
::

    mkdir -p ca/email-ca/private ca/email-ca/db crl certs
    chmod 700 ca/email-ca/private

\2.2 Create database
--------------------
::

    cp /dev/null ca/email-ca/db/email-ca.db
    cp /dev/null ca/email-ca/db/email-ca.db.attr
    echo 01 > ca/email-ca/db/email-ca.crt.srl
    echo 01 > ca/email-ca/db/email-ca.crl.srl

\2.3 Create CA request
----------------------
::

    openssl req -new \
        -config etc/email-ca.conf \
        -out ca/email-ca.csr \
        -keyout ca/email-ca/private/email-ca.key

\2.4 Create CA certificate
--------------------------
::

    openssl ca \
        -config etc/root-ca.conf \
        -in ca/email-ca.csr \
        -out ca/email-ca.crt

\2.5 Create initial CRL
-----------------------
::

    openssl ca -gencrl \
        -config etc/email-ca.conf \
        -out crl/email-ca.crl

\2.6 Create PEM bundle
----------------------
::

    cat ca/email-ca.crt ca/root-ca.crt > \
        ca/email-ca-chain.pem


\3. Create Network CA
=====================

\3.1 Create directories
-----------------------
::

    mkdir -p ca/network-ca/private ca/network-ca/db crl certs
    chmod 700 ca/network-ca/private

\3.2 Create database
--------------------
::

    cp /dev/null ca/network-ca/db/network-ca.db
    cp /dev/null ca/network-ca/db/network-ca.db.attr
    echo 01 > ca/network-ca/db/network-ca.crt.srl
    echo 01 > ca/network-ca/db/network-ca.crl.srl

\3.3 Create CA request
----------------------
::

    openssl req -new \
        -config etc/network-ca.conf \
        -out ca/network-ca.csr \
        -keyout ca/network-ca/private/network-ca.key

\3.4 Create CA certificate
--------------------------
::

    openssl ca \
        -config etc/root-ca.conf \
        -in ca/network-ca.csr \
        -out ca/network-ca.crt

\3.5 Create initial CRL
-----------------------
::

    openssl ca -gencrl \
        -config etc/network-ca.conf \
        -out crl/network-ca.crl

\3.6 Create PEM bundle
----------------------
::

    cat ca/network-ca.crt ca/root-ca.crt > \
        ca/network-ca-chain.pem


\4. Create Software CA
======================

\4.1 Create directories
-----------------------
::

    mkdir -p ca/software-ca/private ca/software-ca/db crl certs
    chmod 700 ca/software-ca/private

\4.2 Create database
--------------------
::

    cp /dev/null ca/software-ca/db/software-ca.db
    cp /dev/null ca/software-ca/db/software-ca.db.attr
    echo 01 > ca/software-ca/db/software-ca.crt.srl
    echo 01 > ca/software-ca/db/software-ca.crl.srl

\4.3 Create CA request
----------------------
::

    openssl req -new \
        -config etc/software-ca.conf \
        -out ca/software-ca.csr \
        -keyout ca/software-ca/private/software-ca.key

\4.4 Create CA certificate
--------------------------
::

    openssl ca \
        -config etc/root-ca.conf \
        -in ca/software-ca.csr \
        -out ca/software-ca.crt

\4.5 Create initial CRL
-----------------------
::

    openssl ca -gencrl \
        -config etc/software-ca.conf \
        -out crl/software-ca.crl

\4.6 Create PEM bundle
----------------------
::

    cat ca/software-ca.crt ca/root-ca.crt > \
        ca/software-ca-chain.pem


\5. Operate Email CA
====================

\5.1 Create email request
-------------------------
::

    openssl req -new \
        -config etc/email-client.conf \
        -out certs/fred.csr \
        -keyout certs/fred.key

DN: C=NO, O=Fnord AS, CN=Fred Flintstone, emailAddress=fred\@fnord.no

\5.2 Create email certificate
-----------------------------
::

    openssl ca \
        -config etc/email-ca.conf \
        -in certs/fred.csr \
        -out certs/fred.crt

\5.3 Create PKCS#12 bundle
--------------------------
::

    openssl pkcs12 -export \
        -name "Fred Flintstone (Email Security)" \
        -caname "Fnord Email CA" \
        -caname "Fnord Root CA" \
        -inkey certs/fred.key \
        -in certs/fred.crt \
        -certfile ca/email-ca-chain.pem \
        -out certs/fred.p12

\5.4 Revoke certificate
-----------------------
::

    openssl ca \
        -config etc/email-ca.conf \
        -revoke ca/email-ca/01.pem \
        -crl_reason superseded

\5.5 Create CRL
---------------
::

    openssl ca -gencrl \
        -config etc/email-ca.conf \
        -out crl/email-ca.crl


\6. Operate Network CA
======================

\6.1 Create server request
--------------------------
::

    SAN=DNS:fnord.no,DNS:www.fnord.no \
    openssl req -new \
        -config etc/tls-server.conf \
        -out certs/fnord.no.csr \
        -keyout certs/fnord.no.key \
        -nodes

DN: C=NO, O=Fnord AS, CN=fnord.no. Note that the subjectAltName
must be specified as environment variable.

\6.2 Create server certificate
------------------------------
::

    openssl ca \
        -config etc/network-ca.conf \
        -in certs/fnord.no.csr \
        -out certs/fnord.no.crt

\6.3 Create PKCS#12 bundle
--------------------------
::

    openssl pkcs12 -export \
        -name "fnord.no (Network Component)" \
        -caname "Fnord Network CA" \
        -caname "Fnord Root CA" \
        -inkey certs/fnord.no.key \
        -in certs/fnord.no.crt \
        -certfile ca/network-ca-chain.pem \
        -out certs/fnord.no.p12

\6.4 Create PEM bundle
----------------------
::

    cat certs/fnord.no.key certs/fnord.no.crt > \
        certs/fnord.no.pem

Most OpenSSL-based software accepts this format (e.g. Apache mod_ssl,
stunnel).

\6.5 Create client request
--------------------------
::

    openssl req -new \
        -config etc/tls-client.conf \
        -out certs/barney.csr \
        -keyout certs/barney.key

DN: C=NO, O=Telenor AS, OU=Support, CN=Barney Rubble, emailAddress=barney\@telenor.no

\6.6 Create client certificate
------------------------------
::

    openssl ca \
        -config etc/network-ca.conf \
        -in certs/barney.csr \
        -out certs/barney.crt \
        -policy extern_pol \
        -extensions client_ext

\6.7 Create PKCS#12 bundle
--------------------------
::

    openssl pkcs12 -export \
        -name "Barney Rubble (Network Access)" \
        -caname "Fnord Network CA" \
        -caname "Fnord Root CA" \
        -inkey certs/barney.key \
        -in certs/barney.crt \
        -certfile ca/network-ca-chain.pem \
        -out certs/barney.p12

\6.8 Revoke certificate
-----------------------
::

    openssl ca \
        -config etc/network-ca.conf \
        -revoke ca/network-ca/02.pem \
        -crl_reason superseded

\6.9 Create CRL
---------------
::

    openssl ca -gencrl \
        -config etc/network-ca.conf \
        -out crl/network-ca.crl


\7. Operate Software CA
=======================

\7.1 Create code-signing request
--------------------------------
::

    openssl req -new \
        -config etc/code-signing.conf \
        -out certs/software.csr \
        -keyout certs/software.key

DN: C=NO, O=Fnord AS, OU=Fnord Certificate Authority, CN=Fnord Software Certificate

\7.2 Create code-signing certificate
------------------------------------
::

    openssl ca \
        -config etc/software-ca.conf \
        -in certs/software.csr \
        -out certs/software.crt

\7.3 Create PKCS#12 bundle
--------------------------
::

    openssl pkcs12 -export \
        -name "Fnord Software Certificate" \
        -caname "Fnord Software CA" \
        -caname "Fnord Root CA" \
        -inkey certs/software.key \
        -in certs/software.crt \
        -certfile ca/software-ca-chain.pem \
        -out certs/software.p12

\7.4 Revoke certificate
-----------------------
::

    openssl ca \
        -config etc/software-ca.conf \
        -revoke ca/software-ca/01.pem \
        -crl_reason superseded

\7.5 Create CRL
---------------
::

    openssl ca -gencrl \
        -config etc/software-ca.conf \
        -out crl/software-ca.crl


\8. Publish Certificates
========================

\8.1 Create DER certificate
---------------------------
::

    openssl x509 \
        -in ca/root-ca.crt \
        -out ca/root-ca.cer \
        -outform der

All published certificates must be in DER format.
MIME type: application/pkix-cert.
[:rfc:`2585#section-4.1`]

\8.2 Create DER CRL
-------------------
::

    openssl crl \
        -in crl/email-ca.crl \
        -out crl/email-ca.crl \
        -outform der

All published CRLs must be in DER format.
MIME type: application/pkix-crl.
[:rfc:`2585#section-4.2`]

\8.3 Create PKCS#7 bundle
-------------------------
::

    openssl crl2pkcs7 -nocrl \
        -certfile ca/network-ca-chain.pem \
        -out ca/network-ca-chain.p7c \
        -outform der

PKCS#7 is used to bundle two or more certificates.
MIME type: application/pkcs7-mime.
[:rfc:`5273#page-3`]


References
======================

* http://openssl.org/docs/apps/req.html
* http://openssl.org/docs/apps/ca.html
* http://openssl.org/docs/apps/x509.html
* http://openssl.org/docs/apps/crl.html
* http://openssl.org/docs/apps/crl2pkcs7.html
* http://openssl.org/docs/apps/pkcs7.html
* http://openssl.org/docs/apps/pkcs12.html

