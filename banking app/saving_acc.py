from interest_reward_acc import *
from errors.balance_exception import *
from errors.lock_exception import *
from middlewares.unlock_middleware import *

class SavingAcc(InterestRewardAcc):
    def __init__(self, initial_amount, acc_name,password):
        super().__init__(initial_amount, acc_name,password)
        self.fee = 5

        
    @require_unlocked_account
    def withdraw(self, amount):
        try:
            self.viable_transactions(amount + self.fee)
            self.balance -= amount + self.fee
            print('Withdraw Complete.')
            self.get_balance()
            return True
        except BalanceException as error:
            print(error)


