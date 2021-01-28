RECORDS_LIST = 'additional/records_list.txt'


class RecordsHolder:

    def __init__(self):
        with open(RECORDS_LIST, mode='r', encoding='utf8') as file:
            self.records = [file.readline().rstrip().split() for _ in range(10)]

    def add_new_record(self, new_record):
        records = []
        for i in range(-1, -11, -1):
            if i == -1 and new_record[1] < int(self.records[i][2]):
                break
            elif new_record[1] <= int(self.records[i][2]):
                records = self.records[:i + 1] + [[f'{i + 12}.', new_record[0],
                                                   str(new_record[1])]] + self.records[i + 1:]
                records = records[:10]
                for _ in range(10):
                    records[_] = [f"{_ + 1}.", records[_][1], records[_][2]]
                self.records = records
                break
            elif new_record[1] > int(self.records[-10][2]):
                records = [['1.', new_record[0], str(new_record[1])]] + self.records[:9]
                for _ in range(10):
                    records[_] = [f"{_ + 1}.", records[_][1], records[_][2]]
                self.records = records
                break

        with open(RECORDS_LIST, mode='w', encoding='utf8') as file:
            for i in range(10):
                file.write(" ".join(self.records[i]))
                file.write('\n')
        self.records = records
