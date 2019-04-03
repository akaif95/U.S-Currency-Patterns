import re, os, pickle


class WatchList:
    def __init__(self, filename=""):
        self.bills = {"5":[], "10":[], "20":[], "50":[], "100":[]}

        if filename == '':
            self.is_sorted = True
        else:
            mystery_filename = open(filename, 'r').readlines()
            self.is_sorted = False

            for line in mystery_filename:
                line = line.split()
                self.bills[line[-1]].append(line[0])

        self.validator = re.compile(r'^[A-M][A-L](?!00000000)\d{8}(?![OZ])[A-Z]''$')
        serial_num_file = open('bill_file_77.txt', 'r').readlines()



    def insert(self, bill_string):
        bill_string_dm = bill_string.split()

        #print(bill_string_dm)

        #Bill is split now like so ["serial number", "denominator"]
        denominator = bill_string_dm[1]
        #print(denominator)

        serial_bill_string = bill_string_dm[0]
        #print(serial_bill_string)

        specific_bill_values = self.bills[denominator]
        #print(specific_bill_values)

        if self.is_sorted and serial_bill_string not in specific_bill_values:
            i = 0
            for i in range(len(specific_bill_values)):
                if serial_bill_string < specific_bill_values[i]:
                    specific_bill_values.insert(i, serial_bill_string)
                    return
            specific_bill_values.append(serial_bill_string)

        elif not self.is_sorted and serial_bill_string not in specific_bill_values:
            specific_bill_values.append(serial_bill_string)


    def sort_bills(self):
        #correct = pickle.load(open('bill_file_77_sorted.pkl', 'rb'))
        for key in self.bills:
            self.bills[key].sort()
        self.is_sorted = True



    def linear_search(self, bill_string):
        bill_string_dm = bill_string.split()

        denominator = bill_string_dm[1]

        serial_bill_string = bill_string_dm[0]

        dictionary_lists = self.bills[denominator]

        if serial_bill_string in dictionary_lists:
            return True
        else:
            return False

    
    def binary_search(self, bill_string):
        bill_string_dm = bill_string.split()

        denomination = bill_string_dm[1]
        serial_bill_string = bill_string_dm[0]

        dictionary_list = self.bills[denomination]

        low_indice = 0
        high_indice = len(dictionary_list) - 1

        
        while low_indice <= high_indice:
            mid = (high_indice + low_indice) // 2
            if dictionary_list[mid] == serial_bill_string:
                return True
            if dictionary_list[mid] > serial_bill_string:
                high_indice = mid - 1
            else:
                low_indice = mid + 1
        return False    




    def check_bills(self, filename, bool_val=False):

        if bool_val and not self.is_sorted:
            self.sort_bills()

        search = self.binary_search if self.is_sorted else self.linear_search

        serial_watchlist = WatchList()
        opened_serial_file = open(filename, 'r')

        bad_bills = []
        for line in opened_serial_file:
            sn = line.split()[0]
            dm = line.split()[1]
            sn_dm = sn + " " + dm
            if search(line) or not self.validator.match(sn):
                bad_bills.append(sn_dm)
        return bad_bills





 
