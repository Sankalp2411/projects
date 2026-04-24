global HyperTrade
def Watchlist_GapUpDown_41IDJ865_1_begin(contextId):
    globals()['GapUpDown_41IDJ865'] = {}
    return
# called for every row,
def Watchlist_GapUpDown_41IDJ865_1_row(HTPy):

    today_open = HTPy.sm.OpenPrice
    yesterday_close = HTPy.sm.PrvClose

    if today_open is None or yesterday_close is None or yesterday_close == 0:
        return "No Data"

    gap_percent = ((today_open - yesterday_close) / yesterday_close) * 100

    if gap_percent > 1:
        return "#00FF00"    
    elif gap_percent < -1:
        return "#FF0000"     
    else:
        return "Neutral"

def Watchlist_GapUpDown_41IDJ865_1_end(contextId):
    
    return

