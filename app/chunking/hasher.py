import hashlib


class ChunkHasher:

    @staticmethod
    def hash(content: str):

        return hashlib.sha256(
            content.encode()
        ).hexdigest()