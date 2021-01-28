RECORDS_LIST = 'additional/records_list.txt'


class RecordsHolder:

    def __init__(self):
        with open(RECORDS_LIST, mode='r', encoding='utf8') as file:
            self.records = [el.rstrip().split() for el in file.readlines()]

    def add_new_record(self, new_record):
        for i in range(-10, 1, -1):
            if i == -10 and new_record[1] < int(self.records[i][2]):
                break
            elif new_record[1] <= int(self.records[i][2]):
                records = self.records[:i + 1] + [self.records[i + 1]] + self.records[i + 1:]
                records = records[:10]
                for j in range(10):
                    records[j][0] = f'{j + 1}.'
                break

        with open(RECORDS_LIST, mode='w', encoding='utf8') as file:
            for i in range(10):
                file.write(" ".join(self.records[i]))
        self.records = records
