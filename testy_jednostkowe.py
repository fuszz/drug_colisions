import unittest
from main import sprawdz_kolizje, wczytaj_baze_lekow

class TestMedicineApp(unittest.TestCase):

    def test_drug_collision_check(self):
        baza_lekow = wczytaj_baze_lekow()
        apteczka = ['Aspiryna', 'Omeprazol']
        result = sprawdz_kolizje(baza_lekow, apteczka)

        expected_result = []
        self.assertEqual(result, expected_result)

    def test_load_drug_database(self):
        baza_lekow = wczytaj_baze_lekow()
        self.assertIsNotNone(baza_lekow)
        self.assertGreater(len(baza_lekow), 0)

    def test_drug_collision_with_nonexistent_drugs(self):
        baza_lekow = wczytaj_baze_lekow()
        apteczka = ['Lek69', 'Lek420']
        result = sprawdz_kolizje(baza_lekow, apteczka)
        expected_result = []  # Adjust based on expected behavior
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
