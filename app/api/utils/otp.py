from secrets import SystemRandom


def generate_random_otp():
    """OTP generated will be of 5 digits, and it's
       range will be 10000 to 99999 (including both).
    """
    random = SystemRandom()
    return random.randint(10000, 99999)
