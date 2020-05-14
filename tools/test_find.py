import csv


def write_csv_file(path, head, data):
    try:
        with open(path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            if head is not None:
                writer.writerow(head)

            for row in data:
                print(row)
                writer.writerow(row)

            print("Write a CSV file to path %s Successful." % path)
    except Exception as e:
        print("Write an CSV file to path: %s, Case: %s" % (path, e))
if __name__ == '__main__':
    path = 'dog.csv'
    head = None
    data = [('这里真好，'),('这里不咋地'),('这里真破')]
    write_csv_file(path,head,data)
