from django.contrib.auth.hashers import BCryptSHA256PasswordHasher


class CustomBCryptSHA256PasswordHasher(BCryptSHA256PasswordHasher):
    rounds = 10
