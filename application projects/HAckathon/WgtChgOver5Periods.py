global HyperTrade
# called at start of iteration
def Watchlist_WgtChgOver5Periods_41IDJ865_2_begin(contextId):
    th = HyperTrade.get_theme()['theme']
    g = globals()
    prev_th = g.get('ChgTrack5Period_Theme', 'not set')
    if th != prev_th:
        print(f"Theme changed from {prev_th} to {th}")
        g['ChgTrack5Period_Theme'] = th
        
    if 'ChgTrack5Period_Context' not in g:
        g['ChgTrack5Period_Context'] = None
    if contextId != g['ChgTrack5Period_Context']:
        g['ChgTrack5Period_Context'] = contextId
        g['ChgTrack5Period'] = {}
    return

def Watchlist_WgtChgOver5Periods_41IDJ865_2_row(HTPy):
    g = globals()
    slab_size = input_float(0.0001, "Slab Size %", 0.00001, 0.01)
    num_slabs = input_int(10, "Slabs", 5, 15)
    periods   = input_int(5, "Periods", 3, 30)
    wgttype   = input_dropdown("Linear", "Weight Type", ["Linear", "Exponential"])
    wgtvalue  = input_float(1.2, "Exp Weight", 1, 10)
    slab_size = slab_size / 100.0 

    sym = HTPy.sm.Symbol

    if sym not in g['ChgTrack5Period']:
        ltp_list = [HTPy.sm.PrvClose]
    else:
        ltp_list = g['ChgTrack5Period'][sym]

    ltp_list.append(HTPy.sm.LastTradePrice)

    if len(ltp_list) > periods:
        ltp_list.pop(0)

    g['ChgTrack5Period'][sym] = ltp_list

    changes = []
    weights = []
    cur_weight = 1 if wgttype == "Linear" else wgtvalue
    for i in range(1, len(ltp_list)):
        changes.append((ltp_list[i] - ltp_list[i - 1]) / max(1e-12, ltp_list[i - 1]))
        weights.append(cur_weight)
        cur_weight = (cur_weight + 1) if wgttype == "Linear" else (cur_weight * wgtvalue)

    den = sum(weights)
    weighted_change = (sum(w * c for w, c in zip(weights, changes)) / den) if den else 0.0

    slab = int(abs(weighted_change) / slab_size)
    if slab > num_slabs:
        slab = num_slabs

    step = max(1, int(128/num_slabs))

    if g['ChgTrack5Period_Theme'] == 'light':
        sub_val = int(0xff - step * slab)
        main_val  = 0xff
    else:
        main_val = int(step * slab)
        sub_val  = 0x00

    if weighted_change < 0:
        r_val, g_val, b_val = main_val, sub_val,  sub_val
    else:
        r_val, g_val, b_val = sub_val,  main_val, sub_val

    return f"#{r_val:02x}{g_val:02x}{b_val:02x}"

def Watchlist_WgtChgOver5Periods_41IDJ865_2_end(contextId):
    return
