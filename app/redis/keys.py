class RedisKeys:

    @staticmethod
    def document(document_id):

        return f"document:{document_id}"

    @staticmethod
    def status(document_id):

        return f"status:{document_id}"

    @staticmethod
    def ocr(document_id):

        return f"ocr:{document_id}"

    @staticmethod
    def embedding(document_id):

        return f"embedding:{document_id}"