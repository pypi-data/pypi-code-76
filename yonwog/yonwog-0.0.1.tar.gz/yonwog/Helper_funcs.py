


class HelperFuncs():


    def input_int_validation(self, message, low, high):

        input_data = input(message)

        while input_data.isalpha() or int(input_data) > int(high) or int(input_data) < int(low):
            print(message)
            input_data = input(message)

        return input_data


   