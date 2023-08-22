from django.db import models
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator

# class DownloadMaterial(models.Model):
#     Material_title = models.CharField(max_length=500),
#     Material_contributors = models.CharField(max_length=500),
#     Material_summary = models.TextField(),
#     # Material_creationDate=models.DateField(auto_now_add=True),
#     # Material_lastUpdatedDate=models.DateField(auto_now=True),
#     # Material_publishedStatus=models.CharField(
#     #         max_length=20, choices=[("Published", "Published"), ("Unpublished", "Unpublished")], default="Unpublished"),
#     # Material_slug=models.SlugField(max_length=2000, blank=True, null=True),
#     # # Material_documentFile=models.FileField(upload_to="FileApp/Document",
#     # #                                            validators=[
#     # #                                                FileExtensionValidator(['pdf', 'zip', 'csv', 'xls', 'ppt', 'html'])],
#     # #                                            null=True, blank=True),
#     # Material_fileSize=models.CharField(max_length=30),

#     class Meta:
#         verbose_name_plural = "Material"

#     def __str__(self):
#         return self.Material_title or ''
    
class Test(models.Model):
    Test_title = models.CharField(max_length=500),
    Test_contributors = models.CharField(max_length=500),

    class Meta:
        verbose_name_plural = "Tests1"

    # def __str__(self):
    #     return self.Test_title
    

