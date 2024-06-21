from tortoise.models import Model
from tortoise import fields


class Gene(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32, description='基因名')
    type = fields.CharField(max_length=32, description='种类')


class GSETable(Model):
    id = fields.IntField(pk=True)
    GSE = fields.CharField(max_length=32, description='GSE号')
    title = fields.CharField(max_length=255, description='对应文章名')


class JTKValue(Model):
    id = fields.IntField(pk=True)

    GSE = fields.ForeignKeyField('models.GSETable')

    omics = fields.CharField(max_length=32, description='组学')
    tissue = fields.CharField(max_length=32, description='取样组织')
    condition = fields.CharField(max_length=32, description='条件')

    gene = fields.ForeignKeyField('models.Gene')

    JTK_pvalue = fields.FloatField(description='JTK_value')
    JTK_BH_Q = fields.FloatField(description='JTK_BH_Q')
    JTK_period = fields.FloatField(description='JTK_period')
    JTK_adjphase = fields.FloatField(description='JTK_adjphase')
    JTK_amplitude = fields.FloatField(description='JTK_amplitude')
    meta2d_Base = fields.FloatField(description='meta2d_Base')
    meta2d_AMP = fields.FloatField(description='meta2d_AMP')
    meta2d_rAMP = fields.FloatField(description='meta2d_rAMP')
