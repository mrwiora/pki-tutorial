=======================
Appendix B: CA Database
=======================

Index File
----------

The index file consists of zero or more lines,
each containing the following fields separated by tab characters:

#. Certificate status flag (V=valid, R=revoked, E=expired).
#. Certificate expiration date in YYMMDDHHMMSSZ format.
#. Certificate revocation date in YYMMDDHHMMSSZ[,reason] format. Empty if not
   revoked.
#. Certificate serial number in hex.
#. Certificate filename or literal string 'unknown'.
#. Certificate distinguished name.

The ``openssl ca`` command uses this file as certificate database.

Attribute File
--------------

The attribute file contains a single line: ``unique_subject = no``. It
reflects the setting in the CA section of the configuration file at the time
the first record is added to the database.

Serial Number Files
-------------------

The ``openssl ca`` command uses two serial number files:

#. Certificate serial number file.
#. CRL number file.

The files contain the next available serial number in hex.

Limitations
-----------

#. The entire database must fit into memory.
#. There are no provisions for concurrency handling.
