===============================
Appendix C: X.509v3 Extensions
===============================

The X.509v3 format allows to attach extensions to certificates,
certificate signing requests (CSR), and certificate revocation lists (CRL).

Such extensions:

a. Define type and purpose of a certificate, CSR, or CRL.
b. Provide pointers to issuer and revocation information for a
   certificate or CRL.
c. Carry other attributes associated with a certificate, CSR, or CRL.

The tutorial uses 9 different extensions which are discussed below.
For further details please refer to
:rfc:`5280#section-4.2`
and
the `OpenSSL documentation <http://www.openssl.org/docs/apps/x509v3_config.html>`_.

keyUsage
========

Present in all certificates and CSRs.
Always critical.

CA certificates use ``keyCertSign`` and ``cRLSign``. User certificates use
``digitalSignature`` and ``keyEncipherment``.

basicConstraints
================

Present in all certificates.
MAY be present in CSRs.
Critical in CA certificates.

The extension has two values:

* ``CA`` which is a boolean value set to TRUE for CA certificates and FALSE for
  user certificates. Always present. [#]_
* ``pathlen`` which is an integer value defining the number of CAs allowed
  below the CA carrying the extension. MAY be present in non-root CA
  certificates.

.. rubric:: Footnotes

.. [#] The RFC says not to include the extension in user certificates
       but is commonly ignored.

extendedKeyUsage
================

MAY be present in user certificates and CSRs.
Critical or not depending on purpose.

Together with keyUsage and basicConstraints this extension controls how the
certificate may be used.
Defined purposes are: ``emailProtection``, ``serverAuth``, ``clientAuth``,
``codeSigning``, ``timeStamping``, and ``OCSPSigning``.
The latter three MUST be marked critical.

subjectAltName
==============

MAY be present in user certificates and CSRs. Never critical.

Contains names associated with the certificate's subject, that can or should
not be part of the DN. This includes Internet domain names, email addresses,
and URIs.

subjectKeyIdentifier
====================

Present in all certificates and CSRs.
Never critical.

Key ID derived from the hash of the subject's public key.

authorityKeyIdentifier
======================

Present in all certificates and CRLs.
Never critical.

Key ID derived from the hash of the issuer's public key.

authorityInfoAccess
===================

Present in non-root certificates and CRLs.
Never critical.

The extension has two values:

* ``caIssuers`` points to certificates issued to the CA that has issued the certificate or CRL.
* ``OCSP`` points to an OCSP responder covering the CA that has issued the certificate.

crlDistributionPoints
=====================

Present in non-root certificates. Never critical.

Points to the CRL issued by the CA that has issued the certificate.

certificatePolicies
===================

MAY be present in non-root certificates.
Critical or not depending on preference.

Certificate policies are labels attached to the certificate
path: To be valid, a policy must be present in every certificate
along the path to the root CA. A policy
has no meaning outside of what the PKI-owner wants it to
mean. The extension MAY be marked critical, but usually
isn't out of compatibility concerns.

Self-signed root certificates are not considered in the policy
validation process and never have a certificatePolicies extension.

