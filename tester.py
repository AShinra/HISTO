

x = 'https://www.manilarepublic.com/back-to-school-with-lenovo-2025-voucher-promo'

x = x.split('/')[2]
print(x)
if x[:4] == 'www.':
    x = x[4:]
    print(x)