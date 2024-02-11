from errors.balance_exception import *
from errors.instance_exception import *
from errors.lock_exception import *
from errors.password_incorrect import *
from middlewares.unlock_middleware import *
class BankAccount:
    """Represents a bank account.

    Attributes:
        balance (float): The current balance of the account.
        name (str): The name of the account holder.
        transaction_list (list): List to store transaction history.
    """
    def __init__(self,initial_amount,acc_name,password):
        """Initializes a new BankAccount object.

        Args:
            initial_balance (float): The initial balance of the account.
            account_name (str): The name of the account holder.
            transaction_list (list): List to store transaction history.

        """
        self.balance = initial_amount
        self.name = acc_name
        self.password = password
        self.transaction_list = []
        self.account_status = False

    @property
    def account_name(self):
        print(self.name)

    @account_name.setter
    def account_name(self,new_name):
        self.name = new_name

    # Lock and Unlock Accounts

    def check_password(self,pwd):
        if self.password != pwd:
            raise PasswordIncorrect(f'\nPassword {pwd} is Incorrect\n')
        return True

    def lock(self):
       self.account_status = False


    def unlock(self,pwd):
        try:
            self.check_password(pwd)
            self.account_status = True
            return True
        except PasswordIncorrect as error:
            print(error)

    def is_account_locked(self):
        if self.account_status is False:
            raise LockException("\nAccount Locked\n")
        return True


    @require_unlocked_account
    def get_balance(self):
            print(f"Account '{self.name}'\nBalance : '${self.balance:.2f}'\n")

    @require_unlocked_account
    def deposit(self, amount):

            self.balance += amount
            print('\nDeposit Complete.')
            self.get_balance()
            return True

    # Custom Exceptions
    def viable_transactions(self,amount):
        if(self.balance >= amount):
            return
        else:
            raise BalanceException(f'Sorry, Insufficient Balance In {self.name} Account\n')

    def validate_receiver(self,account):
        if isinstance(account,BankAccount):
            return
        else:
            raise InstanceException(f'The Receiver Account Is Not Valid BankAccount\n')


    @require_unlocked_account
    def withdraw(self, amount):
        try:
            self.viable_transactions(amount)
            self.balance -= amount
            print('Withdraw Complete.')
            self.get_balance()
            return True
        except BalanceException as error:
            print(error)

    @require_unlocked_account
    def transaction_history(self):
        """Displays transaction history of the account."""
        if len(self.transaction_list) == 0:
            print('No Transaction History Found')
        else:
            for transaction in self.transaction_list:
                print('==>\t{} {} {} : ${}{}\n'.format(
                transaction['sender'],
                transaction['access'],
                transaction['receiver'],
                transaction['sign'],
                transaction['amount']
            ))

    def create_transaction(self,sender,receiver,amount,sign,access):
        """Adds a transaction to the transaction history.

        Args:
            sender (str): The name of the sender.
            receiver (str): The name of the receiver.
            amount (float): The amount of the transaction.
            sign (str): The sign of the transaction ('+' for deposit, '-' for withdrawal).
            access (str): The direction of the transaction ('-->' for outgoing, '<--' for incoming).
        """
        self.transaction_list.append({'sender':sender, 'receiver': receiver, 'amount':str(amount), 'sign':sign, 'access':access})

    @require_unlocked_account
    def transfer(self, amount,receiver):
            """Transfers money to another account.

            Args:
                amount (float): The amount to transfer.
                receiver (BankAccount): The recipient of the transfer.

            Raises:
                InstanceException: If the receiver is not a valid BankAccount object.
            """
            try:
                self.validate_receiver(receiver) # check
                if(self.withdraw(amount)):
                    receiver.deposit(amount)
                    print('Transfer Complete.\n')
                self.create_transaction(self.name,receiver.name,amount,'-','-->')
                receiver.create_transaction(receiver.name,self.name,amount,'+','<--')
            except InstanceException as error:
                print(error)



