import csv
import datetime as dt
from pathlib import Path

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LIST_HEADER = ('Status', 'Amount')
PARENT_DIR = Path(__file__).parents[1]


class PepParsePipeline:

    def open_spider(self, spider):
        self.status_amount = {}

    def process_item(self, item, spider):
        if self.status_amount.get(item['status'], 0) == 0:
            self.status_amount[item['status']] = 1
        else:
            self.status_amount[item['status']] += 1
        return item

    def close_spider(self, spider):
        total_amount = sum(self.status_amount.values())
        results = list(self.status_amount.items())
        # results.insert(0, LIST_HEADER)
        # results.append(('Total', total_amount))

        results_dir = PARENT_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = results_dir / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow(LIST_HEADER)
            writer.writerows(results)
            writer.writerow(('Total', total_amount))
