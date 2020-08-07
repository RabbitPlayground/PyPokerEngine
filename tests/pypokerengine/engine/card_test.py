from tests.base_unittest import BaseUnitTest
from pypokerengine.engine.card import Card


class CardTest(BaseUnitTest):

    def setUp(self):
        pass

    def test_to_string(self):
        self.eq(str(Card(Card.CLUB, 1)), '2c')
        self.eq(str(Card(Card.CLUB, 2)), '3c')
        self.eq(str(Card(Card.HEART, 10)), 'Jh')
        self.eq(str(Card(Card.SPADE, 11)), 'Qs')
        self.eq(str(Card(Card.DIAMOND, 12)), 'Kd')
        self.eq(str(Card(Card.DIAMOND, 13)), 'Ad')

    def test_to_id(self):
        self.eq(Card(Card.HEART, 3).to_id(), 29)
        self.eq(Card(Card.SPADE, 1).to_id(), 40)

    def test_from_id(self):
        self.eq(Card.from_id(1), Card(Card.DIAMOND, 1))
        self.eq(Card.from_id(29), Card(Card.HEART, 3))
        self.eq(Card.from_id(40), Card(Card.SPADE, 1))

    def test_from_str(self):
        self.eq(Card(Card.CLUB, 13), Card.from_str('Ac'))
        self.eq(Card(Card.HEART, 9), Card.from_str('Th'))
        self.eq(Card(Card.SPADE, 8), Card.from_str('9s'))
        self.eq(Card(Card.DIAMOND, 11), Card.from_str('Qd'))
