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


@api.get("/gse/{key}")
async def getGSE(key: str):
    print('gse', key)
    return {
        'gse': key
    }


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
