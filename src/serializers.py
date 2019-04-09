import csv, json, os

HIST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'histograms')

def json_serializer(histogram):
    fname = str(histogram) + '.json'
    with open(HIST_DIR + os.sep + fname, 'w') as f:
        json.dump(histogram.values, f, sort_keys=True)

def csv_serializer(histogram):
    fname = str(histogram) + '.csv'
    with open(HIST_DIR + os.sep + fname, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(histogram.values.items())