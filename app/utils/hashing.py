import hashlib


class FileHasher:

    @staticmethod
    def hash_text(text):

        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()