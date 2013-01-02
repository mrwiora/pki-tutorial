.. SSLCA documentation master file, created by
   sphinx-quickstart on Sat May 19 14:30:39 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. highlight:: bash

==============================================================================
Expert PKI
==============================================================================

The Expert PKI consist of a root CA, an intermediate CA, and two signing CAs.


Overview
========

We assume a company named **Blue AB**, controlling the domain blue.se.
The company operates a flexible, multi-level PKI. To construct the PKI, we
start with the Blue Root CA followed by the intermediate Network CA.
We then create the two signing CAs and proceed to issue
user certificates.

All commands are ready to be copy/pasted into a terminal session.
When you have reached the end of this page, you will have created and
operated a real-world PKI.

To get started, fetch the Expert PKI example files and change into the new
directory::

    git clone https://bitbucket.org/stefanholek/pki-example-3
    cd pki-example-3

Layout
======

.. image:: ../_static/ExpertPKILayout.png
   :width: 465
   :height: 420

We use one configuration file per CA:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   root-ca.conf
   network-ca.conf
   identity-ca.conf
   component-ca.conf

And one configuration file per CSR type:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   identity.conf
   encryption.conf
   tls-server.conf
   tls-client.conf
   timestamping.conf
   ocsp-signing.conf

Please study the configuration files before you continue.


Create Root CA
=======================

Create directories
-----------------------
::

    mkdir -p ca/root-ca/private ca/root-ca/db crl certs
    chmod 700 ca/root-ca/private

Create database
--------------------
::

    cp /dev/null ca/root-ca/db/root-ca.db
    cp /dev/null ca/root-ca/db/root-ca.db.attr
    echo 01 > ca/root-ca/db/root-ca.crt.srl
    echo 01 > ca/root-ca/db/root-ca.crl.srl

Create CA request
----------------------
::

    openssl req -new \
        -config etc/root-ca.conf \
        -out ca/root-ca.csr \
        -keyout ca/root-ca/private/root-ca.key

Create CA certificate
--------------------------
::

    openssl ca -selfsign \
        -config etc/root-ca.conf \
        -in ca/root-ca.csr \
        -out ca/root-ca.crt \
        -extensions root_ca_ext \
        -enddate 310101000000Z

2048-bit RSA keys are deemed safe until 2030 (`RSA Labs`_).

.. _`RSA Labs`: http://www.rsa.com/rsalabs/node.asp?id=2004

Create initial CRL
-----------------------
::

    openssl ca -gencrl \
        -config etc/root-ca.conf \
        -out crl/root-ca.crl


Create Network CA
==========================

Create directories
-----------------------
::

    mkdir -p ca/network-ca/private ca/network-ca/db crl certs
    chmod 700 ca/network-ca/private

Create database
--------------------
::

    cp /dev/null ca/network-ca/db/network-ca.db
    cp /dev/null ca/network-ca/db/network-ca.db.attr
    echo 01 > ca/network-ca/db/network-ca.crt.srl
    echo 01 > ca/network-ca/db/network-ca.crl.srl

Create CA request
----------------------
::

    openssl req -new \
        -config etc/network-ca.conf \
        -out ca/network-ca.csr \
        -keyout ca/network-ca/private/network-ca.key

Create CA certificate
--------------------------
::

    openssl ca \
        -config etc/root-ca.conf \
        -in ca/network-ca.csr \
        -out ca/network-ca.crt \
        -extensions intermediate_ca_ext \
        -enddate 310101000000Z

Create initial CRL
-----------------------
::

    openssl ca -gencrl \
        -config etc/network-ca.conf \
        -out crl/network-ca.crl

Create PEM bundle
----------------------
::

    cat ca/network-ca.crt ca/root-ca.crt > \
        ca/network-ca-chain.pem


Create Identity CA
===========================

Create directories
-----------------------
::

    mkdir -p ca/identity-ca/private ca/identity-ca/db crl certs
    chmod 700 ca/identity-ca/private

Create database
--------------------
::

    cp /dev/null ca/identity-ca/db/identity-ca.db
    cp /dev/null ca/identity-ca/db/identity-ca.db.attr
    echo 01 > ca/identity-ca/db/identity-ca.crt.srl
    echo 01 > ca/identity-ca/db/identity-ca.crl.srl

Create CA request
----------------------
::

    openssl req -new \
        -config etc/identity-ca.conf \
        -out ca/identity-ca.csr \
        -keyout ca/identity-ca/private/identity-ca.key

Create CA certificate
--------------------------
::

    openssl ca \
        -config etc/network-ca.conf \
        -in ca/identity-ca.csr \
        -out ca/identity-ca.crt \
        -extensions signing_ca_ext

Create initial CRL
-----------------------
::

    openssl ca -gencrl \
        -config etc/identity-ca.conf \
        -out crl/identity-ca.crl

Create PEM bundle
----------------------
::

    cat ca/identity-ca.crt ca/network-ca-chain.pem > \
        ca/identity-ca-chain.pem


Create Component CA
============================

Create directories
-----------------------
::

    mkdir -p ca/component-ca/private ca/component-ca/db crl certs
    chmod 700 ca/component-ca/private

Create database
--------------------
::

    cp /dev/null ca/component-ca/db/component-ca.db
    cp /dev/null ca/component-ca/db/component-ca.db.attr
    echo 01 > ca/component-ca/db/component-ca.crt.srl
    echo 01 > ca/component-ca/db/component-ca.crl.srl

Create CA request
----------------------
::

    openssl req -new \
        -config etc/component-ca.conf \
        -out ca/component-ca.csr \
        -keyout ca/component-ca/private/component-ca.key

Create CA certificate
--------------------------
::

    openssl ca \
        -config etc/network-ca.conf \
        -in ca/component-ca.csr \
        -out ca/component-ca.crt \
        -extensions signing_ca_ext

Create initial CRL
-----------------------
::

    openssl ca -gencrl \
        -config etc/component-ca.conf \
        -out crl/component-ca.crl

Create PEM bundle
----------------------
::

    cat ca/component-ca.crt ca/network-ca-chain.pem > \
        ca/component-ca-chain.pem


Operate Identity CA
============================

Create identity request
----------------------------
::

    openssl req -new \
        -config etc/identity.conf \
        -out certs/fred-id.csr \
        -keyout certs/fred-id.key

DN: C=SE, O=Blue AB, CN=Fred Flintstone, emailAddress=fred\@blue.se

Create identity certificate
--------------------------------
::

    openssl ca \
        -config etc/identity-ca.conf \
        -in certs/fred-id.csr \
        -out certs/fred-id.crt \
        -extensions identity_ext

Create PKCS#12 bundle
--------------------------
::

    openssl pkcs12 -export \
        -name "Fred Flintstone (Blue Identity)" \
        -caname "Blue Identity CA" \
        -caname "Blue Network CA" \
        -caname "Blue Root CA" \
        -inkey certs/fred-id.key \
        -in certs/fred-id.crt \
        -certfile ca/identity-ca-chain.pem \
        -out certs/fred-id.p12

Create encryption request
------------------------------
::

    openssl req -new \
        -config etc/encryption.conf \
        -out certs/fred-enc.csr \
        -keyout certs/fred-enc.key

DN: C=SE, O=Blue AB, CN=Fred Flintstone, emailAddress=fred\@blue.se

Create encryption certificate
----------------------------------
::

    openssl ca \
        -config etc/identity-ca.conf \
        -in certs/fred-enc.csr \
        -out certs/fred-enc.crt \
        -extensions encryption_ext

Create PKCS#12 bundle
--------------------------
::

    openssl pkcs12 -export \
        -name "Fred Flintstone (Blue Encryption)" \
        -caname "Blue Identity CA" \
        -caname "Blue Network CA" \
        -caname "Blue Root CA" \
        -inkey certs/fred-enc.key \
        -in certs/fred-enc.crt \
        -certfile ca/identity-ca-chain.pem \
        -out certs/fred-enc.p12

Revoke certificate
-----------------------
::

    openssl ca \
        -config etc/identity-ca.conf \
        -revoke ca/identity-ca/02.pem \
        -crl_reason superseded

Create CRL
---------------
::

    openssl ca -gencrl \
        -config etc/identity-ca.conf \
        -out crl/identity-ca.crl


Operate Component CA
============================

Create server request
--------------------------
::

    SAN=DNS:blue.se,DNS:www.blue.se \
    openssl req -new \
        -config etc/tls-server.conf \
        -out certs/blue.se.csr \
        -keyout certs/blue.se.key

DN: C=SE, O=Blue AB, CN=www.blue.se

Create server certificate
------------------------------
::

    openssl ca \
        -config etc/component-ca.conf \
        -in certs/blue.se.csr \
        -out certs/blue.se.crt \
        -extensions server_ext

Create client request
--------------------------
::

    openssl req -new \
        -config etc/tls-client.conf \
        -out certs/monitor.csr \
        -keyout certs/monitor.key

DN: C=SE, O=Blue AB, CN=Blue Network Monitor

Create client certificate
------------------------------
::

    openssl ca \
        -config etc/component-ca.conf \
        -in certs/monitor.csr \
        -out certs/monitor.crt \
        -extensions client_ext

Create time stamping request
---------------------------------
::

    openssl req -new \
        -config etc/timestamping.conf \
        -out certs/timestamp.csr \
        -keyout certs/timestamp.key

DN: C=SE, O=Blue AB, CN=Blue Timestamp Service

Create time stamping certificate
-------------------------------------
::

    openssl ca \
        -config etc/component-ca.conf \
        -in certs/timestamp.csr \
        -out certs/timestamp.crt \
        -extensions timestamp_ext

Create OCSP-signing request
--------------------------------
::

    openssl req -new \
        -config etc/ocsp-signing.conf \
        -out certs/responder.csr \
        -keyout certs/responder.key

DN: C=SE, O=Blue AB, CN=Blue OCSP Responder

Create OCSP-signing certificate
------------------------------------
::

    openssl ca \
        -config etc/component-ca.conf \
        -in certs/responder.csr \
        -out certs/responder.crt \
        -extensions ocsp_ext

Revoke certificate
-----------------------
::

    openssl ca \
        -config etc/component-ca.conf \
        -revoke ca/component-ca/03.pem \
        -crl_reason superseded

Create CRL
----------------
::

    openssl ca -gencrl \
        -config etc/component-ca.conf \
        -out crl/component-ca.crl


Publish Certificates
========================

Create DER certificate
---------------------------
::

    openssl x509 \
        -in ca/root-ca.crt \
        -out ca/root-ca.cer \
        -outform der

All published certificates must be in DER format.
MIME type: application/pkix-cert.
[:rfc:`2585#section-4.1`]

Create DER CRL
-------------------
::

    openssl crl \
        -in crl/network-ca.crl \
        -out crl/network-ca.crl \
        -outform der

All published CRLs must be in DER format.
MIME type: application/pkix-crl.
[:rfc:`2585#section-4.2`]

Create PKCS#7 bundle
-------------------------
::

    openssl crl2pkcs7 -nocrl \
        -certfile ca/component-ca-chain.pem \
        -out ca/component-ca-chain.p7c \
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
