from django.db import models


# Create your models here.

class GlycoOnto(models.Model):
    id = models.AutoField(primary_key=True)

    function = models.CharField(max_length=100)
    sub_function = models.CharField(max_length=100)
    sub_sub_function = models.CharField(max_length=100)
    sub_sub_sub_function = models.CharField(max_length=100)

    pathway = models.CharField(max_length=100)
    sub_pathway = models.CharField(max_length=100)
    sub_sub_pathway = models.CharField(max_length=100)
    sub_sub_sub_pathway = models.CharField(max_length=100)
    sub_sub_sub_sub_pathway = models.CharField(max_length=100)
    sub_sub_sub_sub_sub_pathway = models.CharField(max_length=100)

    gene_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'glycodb'
        managed = False
