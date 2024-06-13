import click
import pandas as pd
from dataprep.eda import create_report


@click.command()
@click.option('--path_to_csv', type=click.Path(exists=True),
              default='data/raw/heart_cleveland_upload.csv')
@click.option('--path_to_report', type=click.Path(exists=False),
              default='reports/eda_report.html')
def create_eda_report(path_to_csv: str, path_to_report: str):
    data = pd.read_csv(path_to_csv)
    report = create_report(data)
    report.save(path_to_report)


if __name__ == '__main__':
    create_eda_report()
