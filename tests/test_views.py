import random
from unittest import TestCase, main
from app import app
from app.user import views


class TestUserViews(TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def test_user_list(self):
        res = self.client.get("users")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Users list", res.text)

    def test_user_detail(self):
        random_id = random.randint(1, 100)
        res = self.client.get(f"users/{random_id}")
        self.assertEqual(res.status_code, 200)
        self.assertIn(str(random_id), res.text)

    def test_user_detail_not_in_id(self):
        wrong_id = "wrong"
        res = self.client.get(f"users/{wrong_id}")
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    main()
