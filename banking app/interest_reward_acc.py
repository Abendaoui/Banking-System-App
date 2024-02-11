from bank_accounts import *
from errors.lock_exception import *
from middlewares.unlock_middleware import *
class InterestRewardAcc(BankAccount):

    #OverRide
    @require_unlocked_account
    def deposit(self, amount):
            self.balance += amount * 1.05
            print('\nDeposit Complete.')
            self.get_balance()
            return True
