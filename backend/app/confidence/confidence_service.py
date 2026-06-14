import re


class ConfidenceService:

    @staticmethod
    def extract_confidence(text):

        patterns = [
            r"Confidence Score.*?([0-9]*\.?[0-9]+)",
            r"Confidence.*?([0-9]*\.?[0-9]+)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE | re.DOTALL
            )

            if match:

                try:
                    return float(match.group(1))
                except:
                    pass

        return 0.50