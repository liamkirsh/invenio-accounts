# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Legacy Invenio hash support."""

import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from passlib.utils.compat import str_to_uascii
from passlib.utils.handlers import GenericHandler, HasSalt, parse_mc2, \
    render_mc2
from six import PY3, binary_type, text_type

__all__ = ('InvenioAesEncryptedEmail', )


def _to_binary(val):
    """Convert to binary."""
    if isinstance(val, text_type):
        return val.encode('utf-8')
    assert isinstance(val, binary_type)
    return val


def _to_string(val):
    """Convert to text."""
    if isinstance(val, binary_type):
        return val.decode('utf-8')
    assert isinstance(val, text_type)
    return val


def _mysql_aes_key(key):
    """Format key."""
    final_key = bytearray(16)
    for i, c in enumerate(key):
        final_key[i % 16] ^= key[i] if PY3 else ord(key[i])
    return bytes(final_key)


def _mysql_aes_pad(val):
    """Padding."""
    val = _to_string(val)
    pad_value = 16 - (len(val) % 16)
    return _to_binary('{0}{1}'.format(val, chr(pad_value) * pad_value))


def _mysql_aes_unpad(val):
    """Reverse padding."""
    val = _to_string(val)
    pad_value = ord(val[-1])
    return val[:-pad_value]


def _mysql_aes_engine(key):
    """Create MYSQL AES cipher engine."""
    return Cipher(algorithms.AES(key), modes.ECB(), default_backend())


def mysql_aes_encrypt(val, key):
    """Mysql AES encrypt value with secret key."""
    assert isinstance(val, binary_type) or isinstance(val, text_type)
    assert isinstance(key, binary_type) or isinstance(key, text_type)
    k = _mysql_aes_key(_to_binary(key))
    v = _mysql_aes_pad(_to_binary(val))
    e = _mysql_aes_engine(k).encryptor()

    return e.update(v) + e.finalize()


def mysql_aes_decrypt(encrypted_val, key):
    """Mysql AES decrypt value with secret key."""
    assert isinstance(encrypted_val, binary_type) \
        or isinstance(encrypted_val, text_type)
    assert isinstance(key, binary_type) or isinstance(key, text_type)
    k = _mysql_aes_key(_to_binary(key))
    d = _mysql_aes_engine(_to_binary(k)).decryptor()
    return _mysql_aes_unpad(d.update(_to_binary(encrypted_val)) + d.finalize())


class InvenioAesEncryptedEmail(HasSalt, GenericHandler):
    """Invenio AES encryption of user email using password as secret key.

    Invenio 1.x was AES encrypting the users email address with the password
    as the secret key and storing it in a blob column. This e.g. caused
    problems when a user wanted to change email address.
    This hashing engine, differs from Invenio 1.x in that it sha256 hashes the
    encrypted value as well to produce a string in the same length instead of
    a binary blob. It is not done for extra security, just for convenience of
    migration to using passlib's sha512.
    An upgrade recipe is provided to migrated existing binary password hashes
    to hashes of this engine.
    """

    name = "invenio_aes_encrypted_email"
    setting_kwds = "salt"
    ident = u"$invenio-aes$"

    @classmethod
    def from_string(cls, hash, **context):
        """Parse instance from configuration string in Modular Crypt Format."""
        salt, checksum = parse_mc2(hash, cls.ident, handler=cls)

        return cls(salt=salt, checksum=checksum)

    def to_string(self):
        """Render instance to configuration string in Modular Crypt Format."""
        return render_mc2(self.ident, self.salt, self.checksum)

    def _calc_checksum(self, secret):
        """Calculate string."""
        return str_to_uascii(
            hashlib.sha256(mysql_aes_encrypt(self.salt, secret)).hexdigest()
        )
