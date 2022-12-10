import math, random

# split array <list> to chunks given length <n>
def chunks(list, n):
  return [list[i:i + n] for i in range(0, len(list), n)]

def generateOtpCode(len = 5):
    digits = '0123456789'
    otp = ''

    for i in range(len) :
      otp += digits[math.floor(random.random() * 10)]

    return otp

# find nth index of string in string
def find_nth(string, substring, n):
  if (n == 1):
    return string.find(substring)
  else:
    return string.find(substring, find_nth(string, substring, n - 1) + 1)
