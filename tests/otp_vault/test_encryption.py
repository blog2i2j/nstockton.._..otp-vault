# Copyright (C) 2025 Nick Stockton
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Future Modules:
from __future__ import annotations

# Built-in Modules:
from unittest import TestCase

# OTP Vault Modules:
from otp_vault.encryption import (
	InvalidEncryptedDataError,
	InvalidHashError,
	WrongPasswordError,
	decode_base64,
	decrypt,
	encode_base64,
	encrypt,
)


class TestEncryption(TestCase):
	def test_base64_encode_and_decode(self) -> None:
		decoded: str = "Hello world!"
		decoded_bytes: bytes = bytes(decoded, "utf-8")
		encoded: str = "SGVsbG8gd29ybGQh"
		encoded_bytes: bytes = bytes(encoded, "utf-8")
		self.assertEqual(decode_base64(encoded), decoded)
		self.assertEqual(decode_base64(encoded_bytes), decoded_bytes)
		self.assertEqual(encode_base64(decoded), encoded)
		self.assertEqual(encode_base64(decoded_bytes), encoded_bytes)

	def test_encryption_decryption(self) -> None:
		password: str = "test_password"  # NOQA: S105
		unencrypted: bytes = b"Some data in plain text."
		# Test encrypt.
		pw_hash, encrypted_data = encrypt(password, unencrypted)
		self.assertTrue(pw_hash.startswith("$argon2"))
		self.assertNotEqual(encrypted_data, unencrypted)
		# Test decrypt with valid password, hash, and data.
		self.assertEqual(decrypt(password, pw_hash, encrypted_data), (unencrypted, False))
		# Test decrypt with invalid password.
		with self.assertRaises(WrongPasswordError):
			self.assertEqual(decrypt("invalid_password", pw_hash, encrypted_data), (unencrypted, False))
		# Test decrypt with invalid hash.
		with self.assertRaises(InvalidHashError):
			self.assertEqual(decrypt(password, "invalid_hash", encrypted_data), (unencrypted, False))
		# Test decrypt with invalid encrypted data.
		with self.assertRaises(InvalidEncryptedDataError):
			self.assertEqual(decrypt(password, pw_hash, b"invalid_encrypted_data"), (unencrypted, False))
