def fund_rank_4_convert(rank_4):
    if rank_4 == '优秀':
        return 4
    elif rank_4 == '良好':
        return 3
    elif rank_4 == '一般':
        return 1
    elif rank_4 == '不佳':
        return 0
    # lack data
    elif rank_4 == '--':
        return 0

def clean_fund_networth_data(net_worth):
    net_worth.unit_net_worth = net_worth.unit_net_worth.astype(float)
    net_worth.accumulated_net_worth = net_worth.accumulated_net_worth.astype(float)
    net_worth.daily_return = net_worth.daily_return.replace(r'(.*)%',  r'\1', regex=True).replace('--', '0').astype(float)/100
    return net_worth

def order_fund_by_score(old_fund_list):
    old_fund_list_score = []
    new_fund_list = []
    for fund in old_fund_list:
        old_fund_list_score.append(fund.fund_rank_score)
    while old_fund_list:
        max_index = old_fund_list_score.index(max(old_fund_list_score))
        old_fund_list_score.pop(max_index)
        new_fund_list.append(old_fund_list.pop(max_index))
    return new_fund_list