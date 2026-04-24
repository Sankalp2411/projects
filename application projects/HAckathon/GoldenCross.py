global HyperTrade

def Watchlist_GoldenCross_41IDJ865_1_begin(contextId):
    globals()['GoldenCross_41IDJ865'] = {}
    return


def Watchlist_GoldenCross_41IDJ865_1_row(HTPy):

    sma50 = HTPy.sm.SMA50
    sma200 = HTPy.sm.SMA200

    if sma50 is None or sma200 is None:
        return "No Data"

    if sma50 > sma200:
        return "#00FF00"   

    elif sma50 < sma200:
        return "#FF0000"   

    else:
        return "Neutral"


def Watchlist_GoldenCross_41IDJ865_1_end(contextId):
    return


