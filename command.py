from abc import ABC, abstractmethod
from requests import get

# command pattern implementation
# creates command objects to be executed by the invoker via the receiver
# also used for request book keeping


class Command(ABC):
    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        pass

# creates command object for each stock in list


class StockCommand(Command):
    def __init__(self, receiver, stock_symbol, financial_metric):
        self.stock_symbol = stock_symbol
        self.financial_metric = financial_metric
        super().__init__(receiver)

    def execute(self):
        return self.receiver.stock_data(self.stock_symbol, self.financial_metric)

# stock receiver used by invoker to retrieve data


class StockReceiver():
    def __init__(self, api_key):
        self.api_key = api_key

    def stock_data(self, stock_symbol, metric):
        if metric == "price":
            endpoint = f"https://financialmodelingprep.com/api/v3/quote-short/{stock_symbol}?apikey={self.api_key}"
        elif metric == "ratio":
            endpoint = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{stock_symbol}?apikey={self.api_key}"
        response = get(endpoint)
        response_dict = response.json()
        response_dict[0].update({'symbol': stock_symbol})
        for key in response_dict[0].keys():
            if response_dict[0][key] == None:
                response_dict[0].update({key: 0})
        return response_dict[0]

# calls each stock command object execute method
# request book keeping


class Invoker():
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def execute_commands(self):
        stock_report = []
        i = 1
        total = len(self.commands)
        for command in self.commands:
            command_output = command.execute()
            stock_report.append(command_output)
            percentage = round((i / total) * 100, 2)
            formatted_percentage = "{:.2f}".format(percentage)
            print("\r" + str(i) + " of " + str(total) + " responses " +
                  "[" + formatted_percentage + "%]", end="")
            i += 1
        print("")
        return stock_report
