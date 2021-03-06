from card_type import CardType


class Card:
    def __init__(self, num=None, color=None, card_type=None, is_the_initial_card_on_table=False):
        self.num = num
        self.color = color
        self.card_type = card_type
        self.is_the_initial_card_on_table = is_the_initial_card_on_table

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        if self.card_type == CardType.Switch_Color_Card:
            if self.color:
                return f"Switch Color to {self.color}"
            else:
                return f"Switch Color"
        elif self.card_type == CardType.Stop_Card:
            return f"Stop Card-{self.color}"
        elif self.card_type == CardType.Switch_Direction_Card:
            return f"Switch Direction-{self.color}"
        else:
            return f"{self.num}-{self.color}"

