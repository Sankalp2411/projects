global HyperTrade

# called at start of iteration
def Watchlist_Allocations_41IDJ865_1_begin(contextId):
    globals()['Allocations_41IDJ865'] = {}
    return

# called for every row
def Watchlist_Allocations_41IDJ865_1_row(HTPy):

    total_portfolio_value = 100000

    qty = 100
    ltp = HTPy.sm.LastTradePrice

    if ltp is None or ltp == 0:
        return "No Data"

    current_value = qty * ltp

    if current_value <= 0:
        return "No Pos"

    allocation = (current_value / total_portfolio_value) * 100

    return f"{allocation:.1f}%"
  

def Watchlist_Allocations_41IDJ865_1_end(contextId):
    return
