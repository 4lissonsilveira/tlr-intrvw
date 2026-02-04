""""Questions:
 

    1. Complete the `MiniVenmo.create_user()` method to allow our application to create new users.

    2. Complete the `User.pay()` method to allow users to pay each other. Consider the following: if user A is paying user B, user's A balance should be used if there's enough balance to cover the whole payment, if not, user's A credit card should be charged instead.

    3. Venmo has the Feed functionality, that shows the payments that users have been doing in the app. If Bobby paid Carol $5, and then Carol paid Bobby $15, it should look something like this
   

    Bobby paid Carol $5.00 for Coffee
    Carol paid Bobby $15.00 for Lunch

    Implement the `User.retrieve_activity()` and `MiniVenmo.render_feed()` methods so the MiniVenmo application can render the feed.

    4. Now users should be able to add friends. Implement the `User.add_friend()` method to allow users to add friends.
    5. Now modify the methods involved in rendering the feed to also show when user's added each other as friends.
"""

"""
MiniVenmo! Imagine that your phone and wallet are trying to have a beautiful
baby. In order to make this happen, you must write a social payment app.
Implement a program that will feature users, credit cards, and payment feeds.
"""

import re
import unittest
import uuid


class UsernameException(Exception):
    pass


class PaymentException(Exception):
    pass


class CreditCardException(Exception):
    pass


class Payment:

    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note
 

class User:

    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0
        self.payments = []

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid.')
        
    def add_balance(self, balance):
        self.balance = balance

    def add_credit_card_number(self, credit_card_number):
        self.credit_card_number = credit_card_number

    def retrieve_feed(self):
        # TODO: add code here
        res = []
        for payment in self.payments:
            res.append(
                (payment.actor, payment.target, payment.amount, payment.note)
            )
    
    def add_friend(self, new_friend):
        # TODO: add code here
        pass

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException('Only one credit card per user!')

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException('Invalid credit card number.')

    def pay(self, target, amount, note):
        if self.balance >= amount:
            payment = self.pay_with_balance(target, amount, note)
        else:
            payment = self.pay_with_card(target, amount, note)
        self.payments.append(payment)

    def pay_with_card(self, target, amount, note):
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')

        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')

        elif self.credit_card_number is None:
            raise PaymentException('Must have a credit card to make a payment.')

        self._charge_credit_card(self.credit_card_number)
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)

        return payment

    def pay_with_balance(self, target, amount, note):
        amount = float(amount)
        payment = Payment(amount, self, target, note)
        target.add_balance(amount)
        self.balance = self.balance - amount
        return payment

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)


    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass


class MiniVenmo:
    users: list = []

    def create_user(self, username, balance, credit_card_number):
        user = User(username=username)
        self.users.append(user)

    def render_feed(self, feed):
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch
        # TODO: add code here
        pass

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")
 
            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        bobby.add_friend(carol)


class TestUser(unittest.TestCase):

    def test_this_works(self):
        with self.assertRaises(UsernameException):
            raise UsernameException()
        
    def test_add_balance(self):
        user = User("Asl1-0")
        user.add_balance(10.0)

        self.assertEqual(user.balance, 10.0)

    def test_add_creditcard_number(self):
        user = User("Asl1-0")
        user.add_credit_card_number("1234-1234-1234-1234")

        self.assertEqual(user.credit_card_number, "1234-1234-1234-1234")

    def test_user_pays_with_balance(self):
        user_a = User("Asl1-0")
        user_b = User("Asl1-1")

        user_a.add_balance(10)
        user_a.pay(user_b, 9, "coffee")
        self.assertEqual(user_a.balance, 1)
        self.assertEqual(user_b.balance, 9)
        
    def test_user_pays_with_credit_card(self):
        user_a = User("Asl1-0")
        user_b = User("Asl1-1")
        user_a.add_credit_card_number("1234")

        user_a.add_balance(10)
        user_a.pay(user_b, 11, "coffee")
        self.assertEqual(user_a.balance, 10)
        self.assertEqual(user_b.balance, 11)


class TestMiniVenmo(unittest.TestCase):
    def test_adds_user_success(self):
        mini_venmo = MiniVenmo()
        mini_venmo.create_user(
            "Asl1-",
            10,
            "1234-1234-1234-1234"
        )
        self.assertEqual(len(mini_venmo.users), 1)
        self.assertEqual(mini_venmo.users[0].username, "Asl1-")
        


if __name__ == '__main__':
    unittest.main()