from external import *
import command

# instantiation of external connection singleton
external = External()

# views to display requested data and retrieve user input


class View():

    # menu selection
    def main_page(self):
        print("\n(1) Rank stocks by finacial metric")
        print("(2) View trending stock")
        print("(3) Exit")
        menu_selection = input("Selection: ")
        return menu_selection

    # ui to retrieve stock list and finacial metric input
    def search_page(self):
        stocks = []
        print("\nEnter stock symbols, enter '0' to stop")

        while True:
            stock = input("Stock Symbol: ")
            if (stock == '0'):
                break
            stocks.append(stock.upper())

        print("Enter financial metric")
        metric = input("Financial Metric: ")
        print("")
        return stocks, metric

    # presents trending stock from redis cloud database
    def trending_stock_page(self, stock):
        print(f"\nThe trending stock is: {stock}")
        input("Enter any key to go back to the main menu...")


# controller to retrive data, communicate with model, and update view
class Controller():

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        while True:
            menu_selection = self.view.main_page()
            if (menu_selection == '1'):
                self.fetch_result()
            elif (menu_selection == '2'):
                self.fetch_trending_stock()
            else:
                print("\nGoodbye\n")
                exit()

    # retrieves requested data via command pattern, sorts by financial metric, prints result
    def fetch_result(self):
        stocks, metric = self.view.search_page()
        self.model.record_search(stocks)
        metric_details = metric.split()

        stock_command_receiver = command.StockReceiver(external.api_key)
        stock_command_invoker = command.Invoker()

        # create command objects, load invoker, retrieve data
        for i in range(len(stocks)):
            stock_command = command.StockCommand(
                stock_command_receiver, stocks[i], metric_details[0])
            stock_command_invoker.add_command(stock_command)
        result = stock_command_invoker.execute_commands()

        # sort list of dictionaries by finacial metric and print
        ratio_lookup = {"quick-ratio": ["quickRatioTTM", True],
                        "debt-to-equity": ["debtEquityRatioTTM", False],
                        "price-to-earnings": ["peRatioTTM", False],
                        "price-to-book": ["priceToBookRatioTTM", False],
                        "return-on-equity": ["returnOnEquityTTM", True],
                        "net-profit-margin": ["netProfitMarginTTM", True]}

        if (metric_details[0] == "price"):
            sorted_result = sorted(
                result, key=lambda x: x["price"], reverse=True)
            for i in range(len(sorted_result)):
                print(
                    f"{sorted_result[i]['symbol']} price is ${sorted_result[i]['price']}")

        elif (metric_details[0] == "ratio"):
            dictionary_key, reverse = ratio_lookup[metric_details[1]]
            sorted_result = sorted(
                result, key=lambda x: x[dictionary_key], reverse=reverse)

            for i in range(len(sorted_result)):
                ratio = round(sorted_result[i][dictionary_key], 4)
                ratio = "N/A" if ratio == 0 else ratio
                print(
                    f"{sorted_result[i]['symbol']} {metric_details[1]} is {ratio}")

        input("Enter any key to go back to the main menu...")

    # retrives trending stock and passes to view
    def fetch_trending_stock(self):
        self.view.trending_stock_page(self.model.get_trending_stock())


# redis cloud database functions
class Model():

    # records each search in a list by incrementing counter
    # records search in leaderboard by searches
    def record_search(self, stocks):
        if (external.dbconn.exists("count") == 0):
            external.dbconn.set("count", 0)
            current_count = 0
        else:
            current_count = int(external.dbconn.get("count"))

        for stock in stocks:
            external.dbconn.rpush(f"query[{current_count}]", stock)
            if (external.dbconn.hget("stock_leaderboard", stock) == None):
                external.dbconn.hset("stock_leaderboard", stock, 1)
            else:
                stock_count = int(external.dbconn.hget("stock_leaderboard", stock))
                stock_count += 1
                external.dbconn.hset("stock_leaderboard", stock, stock_count)

        current_count += 1
        external.dbconn.set("count", current_count)

    # finds top stock in leaderboard and returns it
    def get_trending_stock(self):
        most_searches = 0
        trending_stock = ""

        stock_leaderboard = external.dbconn.hgetall("stock_leaderboard")

        for stock in stock_leaderboard:
            stock_searches = int(stock_leaderboard[stock])
            if (stock_searches > most_searches):
                most_searches = stock_searches
                trending_stock = stock
        return trending_stock
