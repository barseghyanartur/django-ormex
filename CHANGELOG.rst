Release history and notes
=========================
`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: none

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.2
---
2017-05-21

- Tested against Python 3.7 and 3.8.
- Tested against Django 2.2 and 3.0.
- Drop Python 3.4 support.
- Drop Django support for old Django versions.
  Supported for version is 1.11 and onwards.

0.2
---
2017-05-21

- The ``sort_results`` argument added to ``aggregations.GroupConcat``.
- Make sure ``separator`` argument of ``aggregations.GroupConcat`` is always
  passed along in case of PostgreSQL, since then it's an obligatory argument.
- Tests added.
- Added explicit testing against sqlite, mysql and postgresql in tox.

0.1.1
-----
2017-05-18

- Changes in the example and demo installer script.
- Re-upload under 0.1.1, due to accidentally uploaded statics.

0.1
---
2017-05-17

- Initial release.
