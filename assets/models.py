from django.db import models

# Create your models here.

class MediaType(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False,unique=True)
    type_code = models.CharField(max_length=32,null=True, blank=True)
    notes = models.TextField(null=True,blank=True)
    parent_type = models.ForeignKey('MediaType',related_name='child_types',on_delete=models.CASCADE,null=True,blank=True)
    file_extension = models.CharField(max_length=16,null=True,blank=True)
    pattern = models.CharField(max_length=128,null=True, blank=True)
    def __str__(self):
        return "{} ({})".format(self.name, self.type_code)

class AssetContainer(models.Model):
    class CONTAINER_TYPES(models.IntegerChoices):
        INPUT = 0
        OUTPUT = 1
        STRUCTURAL = 2
    name = models.CharField(max_length=128,null=False,blank=False)
    path = models.CharField(max_length=128,null=False,blank=False,unique=True)
    parent_container = models.ForeignKey('AssetContainer',null=True,on_delete=models.CASCADE,related_name='child_containers')
    delete_on_process = models.BooleanField(default=False)
    container_type = models.IntegerField(choices=CONTAINER_TYPES.choices,default=CONTAINER_TYPES.STRUCTURAL)
    notes = models.TextField(null=True,blank=True)
    url = models.URLField()


class Asset(models.Model):
    container = models.ForeignKey(AssetContainer,null=False,on_delete=models.CASCADE,related_name='assets')
    name = models.CharField(max_length=128,null=False,blank=False)
    path = models.CharField(max_length=128,null=False,blank=False)
    notes = models.TextField(null=True,blank=True)
    media_type = models.ForeignKey(MediaType,on_delete=models.DO_NOTHING,null=True,related_name='assets')


class TransformerArchetype(models.Model):
    name = models.CharField(max_length=128,null=False,blank=False)
    notes = models.TextField(null=True,blank=True)
    class TransformerType(models.IntegerChoices):
        file = 1
        directory = 2
    class TransformationAutomationTypes(models.IntegerChoices):
        automatic = 0
        manual = 1
        automaicic_on_approval = 2
        manual_on_approval = 3
    media_type = models.ManyToManyField(MediaType,related_name='transformer_archetypes')
    transformer_type = models.IntegerField(choices=TransformerType.choices)
    transformer_automations = models.IntegerField(choices=TransformationAutomationTypes.choices)
    validation_script = models.TextField(null=True,blank=True)
    transformation_script = models.TextField(null=True,blank=True)
    cleanup_script = models.TextField(null=True,blank=True)
    notification_script = models.TextField(null=True,blank=True)
    script_variables = models.TextField(default='{"input","container","output","container"}')

class TransFormer(models.Model):
    transformer_archetype = models.ForeignKey(TransformerArchetype,on_delete=models.DO_NOTHING,related_name="transformers")
    media_type = models.ManyToManyField(MediaType,related_name='transformer')
    input_containers = models.ManyToManyField('AssetContainer',related_name='input_transformers')
    output_containers = models.ManyToManyField('AssetContainer',related_name='output_transformers')
    delete_on_process = models.BooleanField(default=False)
    script_variables = models.TextField(default='{"input","container","output","container"}')

class Jobs(models.Model):
    class JOB_STATUS(models.IntegerChoices):
        PREPARING = 0
        PENDING = 1
        PAUSED = 2
        SUCCEEDED = 3
        FAILED = 4
    transformer = models.ForeignKey(TransFormer,related_name='jobs',on_delete=models.CASCADE)
    input_container = models.ForeignKey('AssetContainer',related_name='jobs',on_delete=models.DO_NOTHING)
    output_containers = models.ManyToManyField('AssetContainer',related_name='job_outputs')
    script_variables = models.TextField(default='{"input","container","output","container"}')
    input_assets = models.ManyToManyField('Asset',related_name='jobs_input')
    output_paths = models.ManyToManyField('Asset',related_name='jobs_output')
    status = models.IntegerField(choices=JOB_STATUS.choices)
    notes = models.TextField(null=True,blank=True)
    prepared = models.DateTimeField(auto_created=True)
    pending_start = models.DateTimeField(null=True)
    pending_end = models.DateTimeField(null=True)
    finished_time = models.DateTimeField(null=True)
    paused_time = models.DateTimeField(null=True)
