import re


class MetadataExtractor:

    @staticmethod
    def extract(chunk: str):

        return {

            "word_count": len(chunk.split()),

            "character_count": len(chunk),

            "contains_table": "|" in chunk,

            "contains_number": bool(
                re.search(r"\d", chunk)
            ),

            "heading": chunk.split("\n")[0][:100],
        }