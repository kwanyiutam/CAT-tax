##### check_input.py #####
## Code which checks the quality of inputs

## Error exceptions
class NotDict(Exception):
    pass

class IncorrectStockDetails(Exception):
    pass

class NoSuchStock(Exception):
    pass

## check_int
## Function: Checks whether the input was an integer
## Input: num - Number to check
## Output: Return number, or raised an exception
def check_int(num):
    if isinstance(num, int):
        return(num)
    else:
        raise ValueError("The input is not an integer")
    

## check_stocks_in
## Function: Checks whether the stock inputs were valid
## Input: stocks - stocks inputs
## Output: Return dictionary, or raised an exception
def check_stocks_in(stocks, default_in, default_in_type):
    # Checks whether the input was dictionary
    if isinstance(stocks, dict):
        # For each stock element
        for stock in list(stocks.keys()):
            # Get the list of keys in the nested dictionary
            stock_keys = list(stocks[stock].keys())
            # Sort the keys
            stock_keys.sort()
            
            # The list must contain everything required, if not, throw exception
            if default_in == stock_keys:
                # Check all elements
                for element in default_in:
                    # For integer inputs, check whether they are valid shares
                    if default_in_type[element] == int:
                        check_shares(stocks[stock][element])
                    # If the inputs are float, check whether they are positive
                    elif default_in_type[element] == float:
                        check_pos(stocks[stock][element])
                return(stocks)
            else:
                raise IncorrectStockDetails(f"The details provided for {stock} are not correct, please check!")
    else:
        raise NotDict("The input is not a dictionary")
    
## check_pos
## Function: Checks whether the input is positive (including zero)
## Input: num - Number to check
## Output: Return number, or raised an exception
def check_pos(num):
    if isinstance(num, (int, float)) == False:
        raise ValueError("Number is not numeric")
    elif num >= 0:
        return(num)
    else:
        raise ValueError("Number must be at or above zero")

## check_pos
## Function: Checks whether the probability is valid
## Input: p - Probability input
## Output: Return number, or raised an exception
def check_prob(p):
    if isinstance(p, (int, float)) == False:
        raise ValueError("Number is not numeric")
    elif p >= 0 and p <= 1:
        return(p)
    else:
        raise ValueError("Not a valid probability")

def check_shares(shares):
    shares = check_int(shares)
    shares = check_pos(shares)
    
    return(shares)
    