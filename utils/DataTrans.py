import pandas as pd
import numpy as np
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
    print('transformed_data',transformed_data)

    result = []
    # num = len(transformed_data[0])
    xAxis = list(transformed_data[0].keys())
    for item in transformed_data:
        # 找到最长的值数组
        max_length = max([len(v) for v in item.values()])

        # 填充缺失的值为每个数组对应位置的平均值
        for key, value in item.items():
            if len(value) < max_length:
                avg_value = str(np.mean([float(val) for val in value]))
                item[key] += [avg_value] * (max_length - len(value))

        # 转换为DataFrame
        tdf = pd.DataFrame(item)
        # 转数值
        tdf = tdf.apply(pd.to_numeric, errors='coerce')

        new_arrays = []
        for index, row in tdf.iterrows():
            new_array = row.tolist()
            new_arrays.append(new_array)
        result.append(new_arrays)
        # tmp = []
        # for key in item:
        #     tmp.extend([float(value) for value in item[key]])
        # result.append([tmp[i:i + num] for i in range(0, len(tmp), num)])
    print('conditionData',condition_data)
    print('result',result)
    return result, xAxis, condition_data