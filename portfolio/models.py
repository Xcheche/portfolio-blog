

# Create your models here.


from django.db import models


from Common.models import CommonModel
from Common.manager import CommonQuerySet, GeneralManager, AllObjectsManager
from accounts.models import CustomUser









class Category(CommonModel):
    name = models.CharField(max_length=255,db_index=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_category_slug')
        ]    


class Portfolio(CommonModel):

    class status_choices(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='portfolios')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='portfolios')

    title = models.CharField(max_length=255,db_index=True)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255, blank=True, null=True)
    image1 = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    
    project_link = models.URLField(blank=True, null=True)
    


    status = models.CharField(max_length=20, choices=status_choices.choices, default='draft', db_index=True)
    client = models.CharField(max_length=255, blank=True, null=True)

    #OBJECT
    objects = GeneralManager()
    all_objects = AllObjectsManager()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Portfolios"
        verbose_name = "Portfolio"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_portfolio_slug')
        ]

        #Composite index for faster lookups on published portfolios
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]