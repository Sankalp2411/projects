global HyperTrade

def Watchlist_Alcn_41IDJ865_1_begin(contextId):
    globals()['Alcn_41IDJ865'] = {}
    return


def Watchlist_Alcn_41IDJ865_1_row(HTPy):

    total_portfolio_value = 100000

    qty = 50

    ltp = HTPy.sm.LastTradePrice

    if ltp is None or ltp == 0:
        return "No Data"

    position_value = qty * ltp

    if position_value <= 0:
        return "No Position"

    allocation_pct = (position_value / total_portfolio_value) * 100

    if allocation_pct > 20:
        return "Overweight"
    else:
        return "OK"


def Watchlist_Alcn_41IDJ865_1_end(contextId):
    return
