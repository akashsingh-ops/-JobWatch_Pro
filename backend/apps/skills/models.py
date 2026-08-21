from django.db import models

class Skill(models.Model):
    CATEGORY_CHOICES = (
        ('languages', 'Programming Languages'),
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Databases'),
        ('cloud_devops', 'Cloud & DevOps'),
        ('ai_ml', 'AI & Machine Learning'),
        ('security', 'Security'),
        ('mobile', 'Mobile'),
        ('general', 'General'),
    )

    name = models.CharField(max_length=100, unique=True, db_index=True)
    normalized_name = models.CharField(max_length=100, db_index=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.normalized_name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
