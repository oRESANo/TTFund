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