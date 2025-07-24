

xxx = ['https://makingtrendz.com/business-and-entertainment/07/16/2025/making-life-good-for-the-next-generation-lg-ambassador-challenge-2025-winner-supports-mothers-and-children/','https://www.manilarepublic.com/back-to-school-with-lenovo-2025-voucher-promo']

for i in xxx:
    x = i.split('/')
    if x[2][:4] == 'www.':
        print(x[2][5:])
    else:
        print(x[2])
