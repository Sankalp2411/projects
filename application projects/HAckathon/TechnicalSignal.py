global HyperTrade
# called at start of iteration
def Watchlist_TechnicalSignal_41IDJ865_1_begin(contextId):
    globals()['TechnicalSignalsV21_24DVKLVK222'] = {}
    return

def Watchlist_TechnicalSignal_41IDJ865_1_row(HTPy):
    sig = ['','','']
    if HTPy.sm.RSI > 70:
        sig[0] = "Sell"
    elif HTPy.sm.RSI < 30:
        sig[0] = "Buy"
    else:
        sig[0] = "Neutral"
    
    if HTPy.sm.MACD > HTPy.sm.SignalLine:
        sig[1] = "Buy"
    elif HTPy.sm.MACD < HTPy.sm.SignalLine:
        sig[1] = "Sell"
    else:
        sig[1] = "Neutral"

    if HTPy.sm.SMA20 > HTPy.sm.SMA50:
        sig[2] = "Buy"
    elif HTPy.sm.SMA20 < HTPy.sm.SMA50:
        sig[2] = "Sell"
    else:
        sig[2] = "Neutral"

    if sig.count("Buy") > sig.count("Sell"):
        return "Buy"
    elif sig.count("Sell") > sig.count("Buy"):
        return "Sell"
    else:
        return "Neutral"

def Watchlist_TechnicalSignal_41IDJ865_1_end(contextId):

    return
