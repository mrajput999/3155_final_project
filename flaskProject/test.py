
import unittest
import requests


class FlaskTest(unittest.TestCase):

    def test_index(self):
        response = requests.get("http://127.0.0.1:5000/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(
            '<p class="home-title">Welcome to the Event Planner</p>' in response.text, True)

    def test_login(self):
        response = requests.get("http://127.0.0.1:5000/login")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        self.assertEqual('Password' and 'Email' in response.text, True)

    def test_register(self):
        response = requests.get("http://127.0.0.1:5000/register")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(
            'First Name' and "Last Name" and "Email" and "Password" and "Confirm Password" in response.text, True)

    def test_home(self):
        response = requests.get("http://127.0.0.1:5000/home")
        statuscode = response.status_code
        print(response.text)
        self.assertEqual(statuscode, 200)
        self.assertEqual(
            '<label for="email">Email</label><input id="email" name="email" required type="text" value="">' in response.text, True)

   #  def test_delete(self):
   #      response = requests.get('http://127.0.0.1:5000/notes/delete')
   #      statuscode = response.status_code
   #      self.assertEqual(statuscode, 500)


if __name__ == " __main__":
    unittest.main()
