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
from utils import DataTrans
import json

api = APIRouter()


# @api.get("/gene/{key}")
# async def GetOneGene(key: str):
#     print('gene', key)
#     geneData = await JTKValue.filter(gene__name=key).order_by('JTK_pvalue').values('GSE__GSE', 'GSE__title',
#                                                                                    'JTK_pvalue', 'JTK_BH_Q')  # 升序
#     print(geneData)
#     return respone_code.resp_200(data=geneData)

@api.get("/{species}/gene/{key}")
async def GetOneGene(species: str, key: str):
    print('gene', key)
    if species == 'Mus':
        geneData = await (MusValue.filter(gene__name=key, gene__type=species).order_by('pvalue')
                          .values('GEOAccession__GSE', 'GEOAccession__title', 'pvalue', 'R2'))
    elif species == 'Homo':
        geneData = await (HomoValue.filter(gene__name=key, gene__type=species).order_by('pvalue')
                          .values('GEOAccession__GSE', 'GEOAccession__title', 'pvalue', 'R2'))
    else:
        return respone_code.resp_400(message="Species not found")

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


# # "Kirrel2","Hmcn1" 暂时不用
# @api.post("/gse/{key}")
# async def getGSE(key: str, gene: Optional[List[str]] = []):
#     h5_path = './data/merged.h5'
#
#     gene_id = await Gene.filter(name__in=gene).values('id', 'name')
#     print(gene_id)
#
#     full_path = get_matrix(h5_path, key)
#     data = []
#     # str_array = list(map(str, float_array))
#     with h5py.File(os.path.join(h5_path), 'r') as f:
#         for t in full_path:
#             tmp = {}
#             dset = f[t]
#             tmp['attr'] = t  # h5路径
#             for dict in gene_id:
#                 tmp[dict['name']] = [str(num) for num in list(dset[()])[dict['id']]]
#             tmp['col'] = list(f['/'.join(t.split('/')[0:-1])].attrs['col'])
#             data.append(tmp)
#     print(data)
#     return respone_code.resp_200(data=data)


@api.get("/{species}/gse/gene")
async def getGSE(species: str, gse: str, gene: str):
    h5_path = './data/merged.h5'
    species_dict = {
        'mouse': 'Mus',
        'human': 'Homo'
    }
    species = species_dict.get(species, '')

    gene_id = await Gene.filter(name=gene, type=species).values('id', 'name')
    print(f'species={species},name={gene} ==> gene_id={gene_id}')

    if species == 'Homo':
        gene_id[0]['id'] -= 25239

    print(f'species={species},name={gene} ==> gene_id={gene_id}')
    full_path = get_matrix(h5_path, gse)
    data = []
    with h5py.File(os.path.join(h5_path), 'r') as f:
        for t in full_path:
            tmp = {}
            dset = f[t]
            tmp['attr'] = t  # h5路径
            # ?
            for dict in gene_id:
                tmp[dict['name']] = [str(num) for num in list(dset[()])[dict['id'] - 1]]
            tmp['col'] = list(f['/'.join(t.split('/')[0:-1])].attrs['col'])
            print(tmp)
            data.append(tmp)
    result, xAxis, condition_data = DataTrans.getGseGeneData(data, gene)
    if species == 'Mus':
        DetialData = await MusValue.filter(GEOAccession__GSE=gse, gene__name=gene).values('GEOAccession__GSE',
                                                                                          'gene__name', 'tissue',
                                                                                          'condition',
                                                                                          'pvalue', 'R2', 'amp',
                                                                                          'phase',
                                                                                          'peakTime', 'offset')
    elif species == 'Homo':
        DetialData = await (
            HomoValue.filter(GEOAccession__GSE=gse, gene__name=gene).values('GEOAccession__GSE', 'gene__name', 'tissue',
                                                                            'condition',
                                                                            'pvalue', 'R2',
                                                                            'amp', 'phase', 'peakTime', 'offset'))
    else:
        return respone_code.resp_400(message="Data not found")

    res = {}
    res['data'] = result
    res['xAxis'] = xAxis
    res['condition'] = condition_data
    res['DetialData'] = DetialData
    print(res)
    print(res['DetialData'])
    return respone_code.resp_200(data=res)


# @api.get("/analyse/{species}/gse/gene/tissue/condition")
# async def getCosLine(species: str, gse: str, gene: str, tissue: str, condition: str):
#     h5_path = './data/merged.h5'
#     species_dict = {
#         'mouse': 'Mus',
#         'human': 'Homo'
#     }
#     species = species_dict.get(species, '')
#
#     gene_id = await Gene.filter(name=gene, type=species).values('id', 'name')
#     print(f'species={species},name={gene} ==> gene_id={gene_id}')
#
#     if species == 'Homo':
#         gene_id[0]['id'] -= 25239
#
#     print(f'species={species},name={gene} ==> gene_id={gene_id}')
#     full_path = get_matrix(h5_path, gse)
#     data = []
#     with h5py.File(os.path.join(h5_path), 'r') as f:
#         for t in full_path:
#             tmp = {}
#             dset = f[t]
#             tmp['attr'] = t  # h5路径
#             # ?
#             for dict in gene_id:
#                 tmp[dict['name']] = [str(num) for num in list(dset[()])[dict['id'] - 1]]
#             tmp['col'] = list(f['/'.join(t.split('/')[0:-1])].attrs['col'])
#             print(tmp)
#             data.append(tmp)
#     result, xAxis, condition_data = DataTrans.getGseGeneData(data, gene)
#     if species == 'Mus':
#         DetialData = await MusValue.filter(GEOAccession__GSE=gse, gene__name=gene).values('GEOAccession__GSE',
#                                                                                           'gene__name', 'tissue',
#                                                                                           'condition',
#                                                                                           'pvalue', 'R2', 'amp',
#                                                                                           'phase',
#                                                                                           'peakTime', 'offset')
#     elif species == 'Homo':
#         DetialData = await (
#             HomoValue.filter(GEOAccession__GSE=gse, gene__name=gene).values('GEOAccession__GSE', 'gene__name', 'tissue',
#                                                                             'condition',
#                                                                             'pvalue', 'R2',
#                                                                             'amp', 'phase', 'peakTime', 'offset'))
#     else:
#         return respone_code.resp_400(message="Data not found")
#
#     res = {}
#     res['data'] = result
#     res['xAxis'] = xAxis
#     res['condition'] = condition_data
#     res['DetialData'] = DetialData
#     print(res)
#     print(res['DetialData'])
#     return respone_code.resp_200(data=res)


@api.get("/{species}/omics")
async def GetOmicsData(species: str, omics: str):
    if species == 'mouse':
        omics = await MusValue.filter(omics=omics).values('GEOAccession__GSE', 'tissue')
    elif species == 'human':
        omics = await HomoValue.filter(omics=omics).values('GEOAccession_id', 'tissue')
    else:
        print('Omic Search Error')
        return respone_code.resp_400(message="Omic Error")

    unique_dict_list = [dict(t) for t in {tuple(d.items()) for d in omics}]

    tissue_count = {}
    for i in unique_dict_list:
        if i['tissue'] in tissue_count:
            tissue_count[i['tissue']] += 1
        else:
            tissue_count[i['tissue']] = 1
    data = {}
    data['tissue_count'] = tissue_count
    print(data)
    return respone_code.resp_200(data=data)


@api.get("/{species}/omics/tissue")
async def GetTissueData(species: str, omics: str, tissue: str):
    print(species, omics, tissue)

    if species == 'mouse':
        GseData = await MusValue.filter(omics=omics, tissue=tissue).distinct().values('GEOAccession__GSE',
                                                                                      'GEOAccession__title')
    elif species == 'human':
        GseData = await HomoValue.filter(omics=omics, tissue=tissue).distinct().values('GEOAccession__GSE',
                                                                                       'GEOAccession__title')
    else:
        print('Omic-Tissue Search Error')
        return respone_code.resp_400(message="Omic-Tissue Error")
    print(GseData)
    return respone_code.resp_200(data=GseData)


@api.get("/{species}/omics/tissue/gene")
async def GetDetailData(species: str, omics: str, gene: str, tissue: Union[str, None] = None):
    print(species, omics, tissue, gene)
    species_dict = {
        'mouse': 'Mus',
        'human': 'Homo'
    }
    species = species_dict.get(species, '')

    if tissue is None:
        if species == 'Mus':
            GseData = await MusValue.filter(omics=omics, gene__name=gene, gene__type=species).distinct().order_by(
                'pvalue').values('GEOAccession__GSE', 'GEOAccession__title', 'gene__name', 'condition', 'pvalue', 'amp',
                                 'R2', 'phase', 'peakTime', 'offset')
            print('no tissue Mus', GseData)
        elif species == 'Homo':
            GseData = await HomoValue.filter(omics=omics, gene__name=gene, gene__type=species).distinct().order_by(
                'pvalue').values('GEOAccession__GSE', 'GEOAccession__title', 'gene__name', 'condition', 'pvalue', 'amp',
                                 'R2', 'phase', 'peakTime', 'offset')
            print('no tissue human', GseData)
        else:
            print('Detail Search Error')
            return respone_code.resp_400(message="Detail Error")

        # GseData = await JTKValue.filter(omics=omics, gene__name=gene).distinct().order_by('JTK_pvalue').values(
        #     'GSE__GSE', 'GSE__title', 'gene__name', 'condition', 'JTK_pvalue', 'JTK_BH_Q')
        # print('no tissue', GseData)
    else:
        if species == 'Mus':
            GseData = await MusValue.filter(omics=omics, tissue=tissue, gene__name=gene,
                                            gene__type=species).distinct().order_by(
                'pvalue').values('GEOAccession__GSE', 'GEOAccession__title', 'gene__name', 'condition', 'pvalue', 'amp',
                                 'phase', 'R2', 'peakTime', 'offset')
            print('tissue Mus', GseData)
        elif species == 'Homo':
            GseData = await HomoValue.filter(omics=omics, tissue=tissue, gene__name=gene,
                                             gene__type=species).distinct().order_by(
                'pvalue').values('GEOAccession__GSE', 'GEOAccession__title', 'gene__name', 'condition', 'pvalue', 'amp',
                                 'phase', 'R2', 'peakTime', 'offset')
            print('tissue human', GseData)
        else:
            print('Detail Search Error')
            return respone_code.resp_400(message="Detail Error")

        # GseData = await JTKValue.filter(omics=result, tissue=tissue, gene__name=gene).distinct().order_by(
        #     'JTK_pvalue').values('GSE__GSE', 'GSE__title', 'gene__name', 'condition', 'JTK_pvalue', 'JTK_BH_Q')
        # print(GseData)
    return respone_code.resp_200(data=GseData)


@api.get("/download/")
async def getAllGEO():
    homoData = await (
        HomoValue.all().values('GEOAccession__GSE', 'GEOAccession__title', 'condition', 'tissue'))
    musData = await (
        MusValue.all().values('GEOAccession__GSE', 'GEOAccession__title', 'condition', 'tissue'))

    homo_data_unique = list({tuple(d.items()) for d in homoData})
    mus_data_unique = list({tuple(d.items()) for d in musData})
    combined_data = homo_data_unique + mus_data_unique


    json_data_list = [dict(data) for data in combined_data]
    print(json_data_list)
    # alldata = {}
    # for i in combined_data:
    #     json_data = {key: value for key, value in i}
    #     print(json_data)
    #     # # 转换为 JSON 格式
    #     # json_string = json.dumps(json_data, indent=4)
    #     alldata.

    # combined_data = json.dumps(combined_data)
    print(json_data_list)
    return respone_code.resp_200(data=json_data_list)
