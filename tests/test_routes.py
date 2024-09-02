import unittest
from app import app, db
from app.models import Vehicle

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_vehicle(self):
        response = self.app.post('/vehicle', json={'name': 'Test Vehicle'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Vehicle successfully added', response.data)

if __name__ == '__main__':
    unittest.main()
