from hstest.stage_test import List
from hstest import *
import re
from string import punctuation
from spacy.lang.en.stop_words import STOP_WORDS


class NaiveBayesClassifier(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="", attach=("", ""), time_limit=900000)
        ]

    def check(self, reply: str, attach):

        df = reply.split('\n')

        if len(df[1:-1]) != 200:
            return CheckResult.wrong(
                f"The DataFrame length is {len(df[1:-1])}. The correct length is 200. Set pd.options.display.")

        if ["target", 'sms'] != df[0].lower().split():
            return CheckResult.wrong(f"Check the column names and their order.")

        if int(df[-2].split()[0]) != 199:
            return CheckResult.wrong(f"Print the first 200 rows")

        for oneRow in df[1:-1]:

            dfSplit = oneRow.split()
            isCapitalized = re.findall("[A-Z]", oneRow)

            if isCapitalized:
                return CheckResult.wrong(
                    f"There are capitalized words in your DataFrame. For example, row number {dfSplit[0]}")

            isNumber = re.findall("[0-9]+", " ".join(dfSplit[1:]))
            if isNumber:
                return CheckResult.wrong(
                    f"There are numbers in your DataFrame. For example, row number {dfSplit[0]}. Convert numbers to xnumbers")

            isPunctuation = re.findall("[" + punctuation + "]+", " ".join(dfSplit[1:-1]))
            if isPunctuation:
                return CheckResult.wrong(f"Remove punctuations from SMS. For example, row number {dfSplit[0]}.")

            for oneWord in dfSplit[1:]:
                if oneWord in STOP_WORDS:
                    return CheckResult.wrong(f"Remove stopwords from SMS. For example, row number {dfSplit[0]}.")

        return CheckResult.correct()


if __name__ == '__main__':
    NaiveBayesClassifier().run_tests()
