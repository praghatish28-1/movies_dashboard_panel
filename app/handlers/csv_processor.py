import csv

class CSVProcessor:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_csv(self, batch_size):
        """ Generator that yields batches of CSV rows """
        with open(self.filepath, newline='') as file:
            reader = csv.DictReader(file)
            batch = []
            for row in reader:
                batch.append(row)
                if len(batch) >= batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch
