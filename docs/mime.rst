======================
Appendix A: MIME Types
======================

.. highlight:: none

File Types
----------

When operating a PKI we deal with only a handful of file types:

#. PKCS#8 private keys

#. PKCS#10 CSRs

#. X.509 certificates

#. X.509 CRLs

#. PKCS#7 bundles of two or more certificates

#. PKCS#12 bundles of private key + certificate(s)

MIME Types
----------

The list of MIME types and file extensions however is easily twice as long::

    application/pkcs8                   .p8  .key
    application/pkcs10                  .p10 .csr
    application/pkix-cert               .cer
    application/pkix-crl                .crl
    application/pkcs7-mime              .p7c

    application/x-x509-ca-cert          .crt .der
    application/x-x509-user-cert        .crt
    application/x-pkcs7-crl             .crl

    application/x-pem-file              .pem
    application/x-pkcs12                .p12 .pfx

    application/x-pkcs7-certificates    .p7b .spc
    application/x-pkcs7-certreqresp     .p7r

Where do they come from?

#. pkcs8 and the .p8 extension are defined in :rfc:`5958#section-7.1`.
   The .key extension is OpenSSL practice. [#]_

#. pkcs10 and the .p10 extension are defined in :rfc:`5967#section-3.1`.
   The .csr extension is Apache mod_ssl practice.

#. pkix-cert and the .cer extension are defined in :rfc:`2585#section-4.1`.

#. pkix-crl and the .crl extension are defined in :rfc:`2585#section-4.2` as well.

#. pkcs7-mime and the .p7c extension are defined in :rfc:`5273#page-3`.

#. x-x509-ca-cert and the .crt extension were introduced by Netscape.
   File contents are the same as with pkix-cert: a DER encoded X.509 certificate.
   [:rfc:`5280#section-4`] [#]_

#. x-x509-user-cert was introduced by Netscape at the same time
   but didn't catch on.

#. x-pkcs7-crl was also introduced by Netscape. Note that the .crl
   extension conflicts with pkix-crl. File contents are the same in either
   case: a DER encoded X.509 CRL.
   [:rfc:`5280#section-5`]

#. x-pem-file and the .pem extension stem from a predecessor of S/MIME:
   Privacy Enhanced Mail.

#. x-pkcs12 and the .p12 extension are used for PKCS#12 files.
   The .pfx extension is a relic from a predecessor of PKCS#12.
   It is still used in Microsoft environments (the extension not the format).

#. x-pkcs7-certificates as well as the .p7b and .spc extensions were introduced
   by Microsoft. File contents are the same as with pkcs7-mime: a DER
   encoded certs-only PKCS#7 bundle. [:rfc:`2315#section-9.1`]

#. x-pkcs7-certreqresp and the .p7r extension were also introduced by Microsoft.
   Likely yet another alias for pkcs7-mime.

.. rubric:: Footnotes

.. [#] The presence of a MIME type does not imply the respective files
       should be published on the Internet. In particular, you will never
       want to expose files containing private keys (.p8, .p12).

.. [#] Since OpenSSL defaults to PEM encoding, virtually all open-source
       software uses PEM encoded .crt files locally. See Apache mod_ssl,
       stunnel, etc.

