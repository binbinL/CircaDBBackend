from fastapi import APIRouter, Request
from models import *
from tortoise.queryset import QuerySet
from pydantic import BaseModel, Field, field_validator
from typing import List, Union, Optional
from fastapi.exceptions import HTTPException
import os
import pandas as pd
import h5py
from utils import respone_code

api = APIRouter()


@api.get("/gene/{key}")
async def GetOneGene(key: str):
    print('gene', key)
    geneData = await JTKValue.filter(gene__name=key).order_by('JTK_pvalue').values('GSE__GSE', 'GSE__title',
                                                                                   'JTK_pvalue', 'JTK_BH_Q')  # 升序
    print(geneData)
    return respone_code.resp_200(data=geneData)


def get_matrix(file, key):
    full_path = []

    def print_attrs(name, obj):
        # isinstance(obj, h5py.Dataset) and
        if name.endswith("data") and name.startswith(key):
            full_path.append(name)

    with h5py.File(file, 'r') as f:
        f.visititems(print_attrs)
    return full_path


# "Kirrel2","Hmcn1" 暂时不用
@api.post("/gse/{key}")
async def getGSE(key: str, gene: Optional[List[str]] = []):
    h5_path = './data/merged.h5'

    gene_id = await Gene.filter(name__in=gene).values('id', 'name')
    print(gene_id)

    full_path = get_matrix(h5_path, key)
    data = []
    # str_array = list(map(str, float_array))
    with h5py.File(os.path.join(h5_path), 'r') as f:
        for t in full_path:
            tmp = {}
            dset = f[t]
            tmp['attr'] = t  # h5路径
            for dict in gene_id:
                tmp[dict['name']] = [str(num) for num in list(dset[()])[dict['id']]]
            tmp['col'] = list(f['/'.join(t.split('/')[0:-1])].attrs['col'])
            data.append(tmp)
    print(data)
    return respone_code.resp_200(data=data)


@api.get("/gse/gene")
async def getGSE(gse: str, gene: str):
    h5_path = './data/merged.h5'

    gene_id = await Gene.filter(name=gene).values('id', 'name')
    print(gene_id)

    full_path = get_matrix(h5_path, gse)
    data = []
    with h5py.File(os.path.join(h5_path), 'r') as f:
        for t in full_path:
            tmp = {}
            dset = f[t]
            tmp['attr'] = t  # h5路径
            for dict in gene_id:
                tmp[dict['name']] = [str(num) for num in list(dset[()])[dict['id']]]
            tmp['col'] = list(f['/'.join(t.split('/')[0:-1])].attrs['col'])
            data.append(tmp)
    print(data)
    return respone_code.resp_200(data=data)


@api.get("/omics")
async def GetOmicsData(omics: str):
    omics_mapping = {'Transcriptome': 'RNA-Seq', '1': 's2', '2': 's3', '3': 's3'}
    result = omics_mapping.get(omics, '')
    omics = await JTKValue.filter(omics=result).values('GSE_id', 'tissue')
    unique_dict_list = [dict(t) for t in {tuple(d.items()) for d in omics}]

    tissue_count = {}
    for i in unique_dict_list:
        if i['tissue'] in tissue_count:
            tissue_count[i['tissue']] += 1
        else:
            tissue_count[i['tissue']] = 1
    # genenames = await Gene.filter(type='Mus').values('name')
    data = {}
    data['tissue_count'] = tissue_count
    # data['genenames'] = [{'value': item['name'], 'name': item['name']} for item in genenames]
    print(data)
    return respone_code.resp_200(data=data)


@api.get("/omics/tissue")
async def GetTissueData(omics: str, tissue: str):
    omics_mapping = {'Transcriptome': 'RNA-Seq', '1': 's2', '2': 's3', '3': 's3'}
    result = omics_mapping.get(omics, '')
    print(omics, tissue)

    # GseData = await JTKValue.filter(omics=result, tissue=tissue).values('GSE__GSE', 'GSE__title')
    # unique_dict_list = [dict(t) for t in {tuple(d.items()) for d in GseData}]
    # print(unique_dict_list)

    GseData = await JTKValue.filter(omics=result, tissue=tissue).distinct().values('GSE__GSE', 'GSE__title')
    return respone_code.resp_200(data=GseData)


@api.get("/omics/tissue/gene")
async def GetJTKData(omics: str, gene: str, tissue: Union[str, None] = None):
    omics_mapping = {'Transcriptome': 'RNA-Seq', '1': 's2', '2': 's3', '3': 's3'}
    result = omics_mapping.get(omics, '')
    print(omics, tissue, gene)
    print(tissue)
    if tissue is None:
        GseData = await JTKValue.filter(omics=result, gene__name=gene).distinct().order_by('JTK_pvalue').values(
            'GSE__GSE', 'GSE__title', 'gene__name', 'condition', 'JTK_pvalue', 'JTK_BH_Q')
        print('no tissue', GseData)
    else:
        GseData = await JTKValue.filter(omics=result, tissue=tissue, gene__name=gene).distinct().order_by(
            'JTK_pvalue').values('GSE__GSE', 'GSE__title', 'gene__name', 'condition', 'JTK_pvalue', 'JTK_BH_Q')
        print(GseData)
    return respone_code.resp_200(data=GseData)
