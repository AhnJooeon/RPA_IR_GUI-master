from Model.RPA_Processor import RPAProcessor
import time

inst = RPAProcessor()
out = '/Users/jooeonahn/Desktop/대구은행/국내은행IR DATA(2023.2Q)_test_04.xlsx'
fact = '/Users/jooeonahn/Desktop/대구은행/Factbook'
rule = './Data/Rule_Format.csv'

inst.Set_Path(out, fact, rule)
start = time.time()
inst.run()
end = time.time()
print(f"{end - start:.5f} sec")
