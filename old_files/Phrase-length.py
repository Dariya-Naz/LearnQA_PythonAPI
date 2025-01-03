import requests
import pytest

class TestPhraseLength:
    def test_check_phrase(self):
        phrase = input("Please, enter any phrase shorter, than 15 characters : ")
        assert len(phrase) < 15, "Your phrase is longer than 15 characters or equal to 15"