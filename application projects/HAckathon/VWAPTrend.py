global HyperTrade

def Watchlist_VWAPTrend_41IDJ865_1_begin(contextId):
    globals()['VWAPTrend_41IDJ865'] = {}
    return

def Watchlist_VWAPTrend_41IDJ865_1_row(HTPy):

    ltp = HTPy.sm.LastTradePrice
    vwap = HTPy.sm.VwapAveragePrice   

    if ltp is None or vwap is None or vwap == 0:
        return "No Data"

    if ltp > vwap:
        return "Bullish"
    elif ltp < vwap:
        return "Bearish"
    else:
        return "Neutral"

def Watchlist_VWAPTrend_41IDJ865_1_end(contextId):
    return

