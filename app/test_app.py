import unittest

from app import saudacao, versao


class TestApp(unittest.TestCase):
    def test_saudacao(self):
        self.assertEqual(saudacao("Maria"), "Olá, Maria!")

    def test_versao_padrao(self):
        self.assertEqual(versao(), "dev")


if __name__ == "__main__":
    unittest.main()
