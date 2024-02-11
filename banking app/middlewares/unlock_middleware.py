from errors.lock_exception import *
def require_unlocked_account(func):
    """Decorator to ensure that the account is unlocked before calling the method."""

    def wrapper(self, *args, **kwargs):
        try:
            self.is_account_locked()
            return func(self, *args, **kwargs)
        except LockException as error:
            print(error)

    return wrapper
