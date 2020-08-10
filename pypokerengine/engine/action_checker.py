from functools import reduce


class ActionChecker:

    @classmethod
    def correct_action(self, players, player_pos, sb_amount, action, amount=None):
        if self.is_allin(players[player_pos], action, amount):
            amount = players[player_pos].stack + players[player_pos].paid_sum()

        elif self.__is_illegal(players, player_pos, sb_amount, action, amount):
            raise Exception(f'Invalid action (player {player_pos}, {action} {amount}, {sb_amount} sb, {players[player_pos].stack} stack and {players[player_pos].paid_sum()} paid)')
            action, amount = 'fold', 0

        return action, amount

    @classmethod
    def is_allin(self, player, action, bet_amount):
        if action == 'call':
            return bet_amount >= player.stack + player.paid_sum()
        elif action == 'raise':
            return bet_amount == player.stack + player.paid_sum()
        else:
            return False

    @classmethod
    def need_amount_for_action(self, player, amount):
        return amount - player.paid_sum()

    @classmethod
    def agree_amount(self, players):
        last_raise = self.__fetch_last_raise(players)
        return last_raise['amount'] if last_raise else 0

    @classmethod
    def legal_actions(self, players, player_pos, sb_amount):
        min_raise = self.__min_raise_amount(players, sb_amount)
        max_raise = players[player_pos].stack + players[player_pos].paid_sum()
        if max_raise < min_raise:
            min_raise = max_raise = -1
        return [
            {'action': 'fold', 'amount': 0},
            {'action': 'call', 'amount': self.agree_amount(players)},
            {'action': 'raise', 'amount': {'min': min_raise, 'max': max_raise}}
        ]

    @classmethod
    def _is_legal(self, players, player_pos, sb_amount, action, amount=None):
        return not self.__is_illegal(players, player_pos, sb_amount, action, amount)

    @classmethod
    def __is_illegal(self, players, player_pos, sb_amount, action, amount=None):
        if action == 'fold':
            return False
        elif action == 'call':
            print(action, self.__is_short_of_money(players[player_pos], amount), self.__is_illegal_call(players, amount))

            return self.__is_short_of_money(players[player_pos], amount) or self.__is_illegal_call(players, amount)
        elif action == 'raise':
            print(action, self.__is_short_of_money(players[player_pos], amount), self.__is_illegal_raise(players, amount, sb_amount))

            return self.__is_short_of_money(players[player_pos], amount) or self.__is_illegal_raise(players, amount, sb_amount)

    @classmethod
    def __is_illegal_call(self, players, amount):
        return amount != self.agree_amount(players)

    @classmethod
    def __is_illegal_raise(self, players, amount, sb_amount):
        return self.__min_raise_amount(players, sb_amount) > amount

    @classmethod
    def __min_raise_amount(self, players, sb_amount):
        raise_ = self.__fetch_last_raise(players)
        # return raise_['amount'] + raise_['add_amount'] if raise_ else sb_amount * 2

        if (raise_ is not None):
            if (raise_['action'] == 'BIGBLIND'):
                print('Min Amount (1): ', sb_amount * 4)
                return sb_amount * 4
            else:
                print('Min Amount (2): ', raise_['amount'] + raise_['add_amount'])
                return raise_['amount'] + raise_['add_amount']
        else:
            print('Min Amount (3): ', sb_amount * 2)
            return sb_amount * 2

    @classmethod
    def __is_short_of_money(self, player, amount):
        return player.stack < amount - player.paid_sum()

    @classmethod
    def __fetch_last_raise(self, players):
        all_histories = [p.action_histories for p in players]
        all_histories = reduce(lambda acc, e: acc + e, all_histories)  # flatten
        raise_histories = [h for h in all_histories if h['action'] in ['RAISE', 'SMALLBLIND', 'BIGBLIND']]
        if len(raise_histories) == 0:
            return None
        else:
            return max(raise_histories, key=lambda h: h['amount'])  # maxby
