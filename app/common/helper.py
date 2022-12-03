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
