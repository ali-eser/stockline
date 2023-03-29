import argparse, click, dataset, sys
from datetime import datetime
from pyfiglet import Figlet

import yfinance as yf


db = dataset.connect("sqlite:///assets.db")
table = db["assets"]

f = Figlet(font="smslant")

parser = argparse.ArgumentParser(
    prog="Stockline",
    description="Asset tracker and stock/currency calculator in CLI"
)


def main():
    click.clear()
    print(f.renderText("Stockline  0 . 0 . 1"))
    print("Stockline 0.0.1")
    while True:
        try:
            i = int(input("\n[1] for currency conversion\n\n[2] for stock prices\n\n[3] for adding to portfolio\n\n[4] for removing from portfolio\n\n[5] for viewing assets\n\n'CTRL + C' or 'COMMAND + .' to exit.\n\n"))
            match i:
                case 1:
                    click.clear()
                    while True:
                        try:
                            amount, base_cur, tar_cur = input("Enter amount, currency and target currency: ").upper().split()
                            convert_cur(amount, base_cur, tar_cur)
                            break
                        except (ValueError, KeyError):
                            click.clear()
                            print("Usage: 'amount' 'base currency symbol' 'target currency symbol' Amount must be larger than 0")
                case 2:
                    click.clear()
                    while True:
                        try:
                            amount, symbol = input("Enter amount and symbol: ").upper().split()
                            get_stock(amount, symbol)
                            break
                        except (ValueError, KeyError):
                            click.clear()
                            print("Usage: 'amount' 'US stock ticker' Amount must be larger than 0")
                case 3:
                    database_add()
                case 4:
                    database_remove()
                case 5:
                    database_view()
                case _:
                    raise ValueError
        except KeyboardInterrupt:
            click.clear()
            sys.exit(0)
        except ValueError:
            click.clear()
            print("Please enter a number from 1 to 5")


def convert_cur(amount, base_cur, tar_cur):
    click.clear()

    if base_cur == "USD":
        symbol = tar_cur + "=X"
    else:
        symbol = base_cur + tar_cur + "=X"

    rate = yf.Ticker(symbol).fast_info["lastPrice"]

    if float(amount) > 0:
        value = float(amount) * rate
        click.clear()
        print(f"{amount} {base_cur} equals to {value:.2f} {tar_cur} | {symbol} is {rate:.2f} as of {get_time()}")
        return True
    else:
        raise ValueError


def get_stock(amount, symbol):
    click.clear()

    if float(amount) <= 0:
        raise ValueError

    price = yf.Ticker(symbol).fast_info["lastPrice"]
    company_name = yf.Ticker(symbol).info["longName"]
    value = float(amount) * price
    click.clear()

    if float(amount) == 1:
        print(f"A share of {company_name} ({symbol.upper()}) is worth ${value:.2f} as of {get_time()}.")
        return True
    elif float(amount) > 1:
        print(f"{amount} shares of {company_name} ({symbol.upper()}) is worth ${value:.2f} as of {get_time()} (${price:.2f} per share).")
        return True


def database_add():
    click.clear()
    if len(table) == 0:
        print("You currently do not own any asset.\n")
    else:
        print("Your assets:\n")
        for row in table:
            company_name = yf.Ticker(row["symbol"]).info["longName"]
            print(f"{row['amount']} {company_name} ({row['symbol']}) ")
        print()
    try:
        amnt, sym = input("Enter amount and symbol to add: ").upper().split()
    except ValueError:
        print("Usage: 'amount' 'US stock/currency ticker' ")
    amnt = float(amnt)
    click.clear()
    for row in table:
        if row["symbol"] == sym:
            amnt += row["amount"]
            data = dict(symbol=sym, amount=amnt)
            table.update(data, ["symbol"])
            return True
    data = dict(symbol=sym, amount=amnt)
    table.insert(data)
    return True


def database_remove():
    click.clear()
    if len(table) == 0:
        print("You do not own any asset to remove!")
    else:
        print("Your assets:\n")
        for row in table:
            company_name = yf.Ticker(row["symbol"]).info["longName"]
            print(f"{row['amount']} {company_name} ({row['symbol']}) ")
        print()
        while True:
            try:
                amnt, sym = input("Enter amount and symbol to remove: ").upper().split()
                amnt = int(amnt)
                for row in table:
                    if row["symbol"] == sym:
                        if (row["amount"] - amnt == 0) or (row["amount"] - amnt < 0):
                            table.delete(symbol=sym)
                            click.clear()
                            return True
                        else:
                            new_amnt = row["amount"] - amnt
                            data = dict(symbol=sym, amount=new_amnt)
                            table.update(data, ["symbol"])
                            click.clear()
                            return True
                    else:
                        print("")
            except ValueError:
                print("Usage: 'amount' 'US stock/currency ticker'")


def database_view():
    click.clear()
    net_worth = 0
    if len(table) > 0:
        for row in table:
            price = yf.Ticker(row["symbol"]).fast_info["lastPrice"]
            company_name = yf.Ticker(row["symbol"]).info["longName"]
            if row["amount"] == 1:
                net_worth += price
                print(f"• You own a share of {company_name} ({row['symbol']}). Value: ${price:.2f} as of {get_time()}.")
            elif row["amount"] > 1:
                net_worth += row["amount"] * price
                print(f"• You own {row['amount']:.2f} shares of {company_name} ({row['symbol']}). Total value: ${row['amount'] * price:.2f} as of {get_time()} (${price:.2f} per share).")
        print(f"\nNet Worth: ${net_worth:.2f}")
        print("\n---------------")
    else:
        print("You currently do not own any asset.")
    return True


def get_time():
    day, mon, year, h, min = datetime.now().day, datetime.now().month, datetime.now().year, datetime.now().hour, datetime.now().minute
    return f"{day}/{mon}/{year} {h}:{min}"


if __name__ == "__main__":
    main()
