from fastapi import APIRouter, Request
from models import *
from tortoise.queryset import QuerySet
from pydantic import BaseModel, Field, field_validator
from typing import List, Union
from fastapi.exceptions import HTTPException
import os
import pandas as pd
import h5py

api = APIRouter()


@api.get("/gene/{key}")
async def GetOneGene(key: str):
    print('gene', key)
    geneData = await JTKValue.filter(gene__name=key).order_by('JTK_pvalue')  # 升序
    return geneData


def get_matrix(file, key):
    full_path = []

    def print_attrs(name, obj):
        # isinstance(obj, h5py.Dataset) and
        if name.endswith("data") and name.startswith(key):
            full_path.append(name)

    with h5py.File(file, 'r') as f:
        f.visititems(print_attrs)
    return full_path


@api.get("/gse/{key}")
async def getGSE(key: str):
    h5_path = './data/merged.h5'
    print('gse', key)
    index = 65

    full_path = get_matrix(h5_path, key)
    data = []
    # str_array = list(map(str, float_array))
    with h5py.File(os.path.join(h5_path), 'r') as f:
        for t in full_path:
            tmp = {}
            dset = f[t]
            tmp['attr'] = t
            tmp['data'] = [str(num) for num in list(dset[()])[index]]
            tmp['col'] = list(f['/'.join(t.split('/')[0:-1])].attrs['col'])
            data.append(tmp)
    print(data)
    return data


@api.get("/{omics}")
async def GetOmicsData(omics: str):
    omics_mapping = {'trans': 'RNA-Seq', '1': 's2', '2': 's3', '3': 's3'}
    result = omics_mapping.get(omics, '')
    omics = await JTKValue.filter(omics=result).values('GSE_id', 'tissue')
    unique_dict_list = [dict(t) for t in {tuple(d.items()) for d in omics}]
    print(unique_dict_list)
    data = {}
    for i in unique_dict_list:
        if i['tissue'] in data:
            data[i['tissue']] += 1
        else:
            data[i['tissue']] = 1
    return data


@api.get("/{omics}/{tissue}")
async def GetOmicsAndTissueData(omics: str, tissue: str):
    omics_mapping = {'trans': 'RNA-Seq', '1': 's2', '2': 's3', '3': 's3'}
    result = omics_mapping.get(omics, '')
    print(omics, tissue)

    # GseData = await JTKValue.filter(omics=result, tissue=tissue).values('GSE__GSE', 'GSE__title')
    # unique_dict_list = [dict(t) for t in {tuple(d.items()) for d in GseData}]
    # print(unique_dict_list)

    GseData = await JTKValue.filter(omics=result, tissue=tissue).distinct().values('GSE__GSE', 'GSE__title')
    return GseData
