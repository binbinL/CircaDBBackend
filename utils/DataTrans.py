def getGseGeneData(raw_data,name):
    transformed_data = []
    condition_data = []
    for item in raw_data:
        ct_data = {}
        condition_data.append('_'.join(item["attr"].split('/')[2:4]))
        for col, expra in zip(item["col"], item[name]):
            ct = col.split('_')[1]
            if ct not in ct_data:
                ct_data[ct] = []
            ct_data[ct].append(expra)
        transformed_data.append(ct_data)

    result = []
    num = len(transformed_data[0])
    xAxis = list(transformed_data[0].keys())
    for item in transformed_data:
        tmp = []
        for key in item:
            tmp.extend([float(value) for value in item[key]])
        result.append([tmp[i:i + num] for i in range(0, len(tmp), num)])

    return result, xAxis, condition_data