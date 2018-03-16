from passlib.handlers.sha2_crypt import sha256_crypt


class CryptoEngine:
    @staticmethod
    def encrypt_password(raw_password):
        return sha256_crypt.encrypt(raw_password)

    @staticmethod
    def verify_password(row_password, encrypted_password):
        return sha256_crypt.verify(row_password, encrypted_password)
