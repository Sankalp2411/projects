global HyperTrade

def Watchlist_BBSqueeze_41IDJ865_1_begin(contextId):
    globals()['BBSqueeze_41IDJ865'] = {
        "bandwidth_list": []
    }
    return


def Watchlist_BBSqueeze_41IDJ865_1_row(HTPy):

    try:
        bb = HTPy.sm.bbands(20, 2)  
        upper = bb['upper']
        middle = bb['middle']
        lower = bb['lower']
    except:
        return "No Data"

    if upper is None or lower is None or middle is None:
        return "No Data"

    bandwidth = upper - lower

    bw_list = globals()['BBSqueeze_41IDJ865']["bandwidth_list"]
    bw_list.append(bandwidth)

    if len(bw_list) > 50:
        bw_list.pop(0)

    if len(bw_list) < 20:
        return "Loading"

    avg_bandwidth = sum(bw_list) / len(bw_list)

    if bandwidth < (avg_bandwidth * 0.7): 
        return "SQUEEZE"
    else:
        return "Normal"


def Watchlist_BBSqueeze_41IDJ865_1_end(contextId):
    return


