from functools import wraps


def commit_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.session.commit()

    return wrapper
