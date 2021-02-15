import argparse
import csv
import os.path


class Invoice:
    def __init__(self, csv_data):
        self.member_id = csv_data[1].split()[1]
        self.amount = float(csv_data[3].replace(',', '.'))
        self.transactions = list()
        self.annotation = ''

    def __str__(self):
        return f'{self.member_id} - {self.amount}'


class Transaction(object):
    def __init__(self, csv_data):
        self.date = csv_data[0]
        self.name = csv_data[3]
        self.subject = csv_data[4]
        self.amount = float(csv_data[7].replace('.', '').replace(',', '.'))

    def __str__(self):
        return f'{self.date} - {self.amount} - {self.name} - {self.subject}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--invoices-path', required=True)
    parser.add_argument('-t', '--transactions-path', required=True)
    args = parser.parse_args()

    for file_path in [args.invoices_path, args.transactions_path]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'No such file or directory: "{file_path}"')


    invoices = list(get_invoices(args.invoices_path))
    transactions = get_transactions(args.transactions_path)

    update_invoice_data_with_transaction_data(invoices, transactions)

    with open("result.csv", "w") as fh:
        writer = csv.writer(fh, delimiter=";")
        writer.writerow("MitgliederID Rechnungsbetrag Ueberweisungbetrag Differenzbetrag Anmerkung".split())

        for invoice in invoices:
            amount = sum([t.amount for t in invoice.transactions])
            diff =  amount - invoice.amount
            writer.writerow([invoice.member_id, invoice.amount, amount, "{:.2f}".format(diff), invoice.annotation])


def get_invoices(file_path):
    csv_rows = get_csv_file_rows(file_path)
    return convert_csv_to_invoices(csv_rows)


def get_transactions(file_path):
    csv_rows = get_csv_file_rows(file_path)
    return convert_csv_to_transactions(csv_rows)


def get_csv_file_rows(file_path):
    with open(file_path, encoding="ISO-8859-1") as fh:
        for row in csv.reader(fh, delimiter=";"):
            yield row


def convert_csv_to_invoices(rows):
    for row in rows:
        yield Invoice(row)


def convert_csv_to_transactions(rows):
    skip_rows(rows, 7)
    for row in rows:
        if row[2] == "Gutschrift":
            yield Transaction(row)


def skip_rows(rows, count):
    for _ in range(count):
        next(rows)


def update_invoice_data_with_transaction_data(invoices, transactions):
    for transaction in transactions:
        assign_transaction_and_update_invoice_data(invoices, transaction)


def assign_transaction_and_update_invoice_data(invoices, transaction):
    for invoice in invoices:
        if invoice.member_id in transaction.subject:
            invoice.transactions.append(transaction)
            return


if __name__ == '__main__':
    main()
