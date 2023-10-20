class BankFormat():
    def Quater(self, tmp):
        return tmp

    def num_to_col_letters(self, num):
        letters = ''
        while num:
            mod = (num - 1) % 26
            letters += chr(mod + 65)
            num = (num - 1) // 26
        return ''.join(reversed(letters))

    def find_colname(self, colName):
        initNum = 1

        while True:
            tmpName = self.num_to_col_letters(initNum)

            if tmpName == colName:
                print(f"Find : {initNum}")
                return initNum
            else:
                initNum += 1
