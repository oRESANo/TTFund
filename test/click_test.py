import click


@click.command()
@click.option('--fund_type', required=True, type=str)
@click.option('--headless', default=True, type=bool)
@click.option('--specific_fund', default=None, type=str)
def x(fund_type, headless, specific_fund):
    print(fund_type)
    print(headless)
    if specific_fund:
        print(123)
    elif not specific_fund:
        print(999)
        
if __name__ == '__main__':
    x()