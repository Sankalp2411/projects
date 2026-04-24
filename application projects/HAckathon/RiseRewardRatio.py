global HyperTrade

def Watchlist_RiskRewardRatio_41IDJ865_1_begin(contextId):
    globals()['RiskRewardRatio_41IDJ865'] = {}
    return


def Watchlist_RiskRewardRatio_41IDJ865_1_row(HTPy):

    ltp = HTPy.sm.LastTradePrice

    if ltp is None or ltp == 0:
        return "No Data"

    target_price = ltp * 1.05
    stoploss_price = ltp * 0.98

    risk = ltp - stoploss_price
    reward = target_price - ltp

    if risk <= 0 or reward <= 0:
        return "Invalid"

    rr_value = reward / risk

    rr_text = f"1:{rr_value:.2f}"
    return rr_text


def Watchlist_RiskRewardRatio_41IDJ865_1_end(contextId):
    return
