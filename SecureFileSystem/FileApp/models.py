from django.db import models
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator

class Material(models.Model):
    Material_Title = models.CharField(max_length=200)
    Material_Contributor = models.CharField(max_length=200)
    Material_Summary = models.TextField()
    Material_Last_Updated_Date = models.DateTimeField(auto_now=True)
    Materail_Created_Date = models.DateTimeField(auto_now_add=True)
    Material_Published_Status=models.CharField(max_length=20, choices=[("Published", "Published"), ("Unpublished", "Unpublished")], default="Unpublished")
    Material_Slug=models.SlugField(max_length=10, blank=True, null=True)
    Material_Document_File=models.FileField(upload_to="FileApp/Document",
                         validators=[FileExtensionValidator(['pdf', 'zip', 'csv', 'xls', 'ppt', 'html'])],null=True, blank=True)
    Material_File_Size=models.CharField(max_length=30),
    
    class Meta:
        verbose_name_plural = "Material"
        
    def __str__(self):
        return self.name
