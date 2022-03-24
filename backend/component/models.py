from io import BytesIO
from PIL import Image

from django.db import models
from django.core.files import File
from django.db.models import Sum, Max

#base_url = "https://stock-manager-serverapi.herokuapp.com"
base_url = "http://localhost:8000"

def make_thumbnail(image, size=(300, 200)):
  """Renders thumbnail from image

  Args:
      image (PIL.Image): The input image
      size (tuple, optional): Expected thumbnail size. Defaults to (300, 200).

  Returns:
      django.core.files.File: Thumbnail file
  """
  img = Image.open(image)
  img.convert('RGB')
  img.thumbnail(size)
  thumb_bytes = BytesIO()
  img.save(thumb_bytes, 'PNG', quality=80)
  thumbnail = File(thumb_bytes, name=image.name)
  return thumbnail

class Category(models.Model):
  """Class representing a component category
  """
  name = models.CharField(max_length=255)
  slug = models.SlugField()
  thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
  thumbnail_processed = models.BooleanField(default=False, blank=True, editable=False)

  class Meta:
    ordering = ('name',)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    """Get the absolute url of category

    Returns:
        string: Absolute url
    """
    return '/%s/'%self.slug

  def get_thumbnail(self):
    """Get the category thumbnail and build it before if not already done before

    Returns:
        string: Thumbnail url
    """
    if self.thumbnail_processed:
      return base_url + self.thumbnail.url
    else:
      if self.thumbnail:
        self.thumbnail = make_thumbnail(self.thumbnail)
        self.thumbnail_processed = True
        self.save()
        return base_url + self.thumbnail.url
      else:
        return ''

  def get_nb_ref(self):
    """Get number of references for category

    Returns:
        int: number of references for category
    """
    return Component.objects.filter(category=self).count()

  def get_nb_units(self):
    """Get number of units for category

    Returns:
        int: number of units for category
    """
    return Component.objects.filter(category=self).aggregate(Sum('quantity')).get("quantity__sum")

class Compartment(models.Model):
  """Class representing a storage compartment
  """
  id = models.PositiveSmallIntegerField(primary_key=True)

  class Meta:
    ordering = ('id',)

  def get_absolute_url(self):
    """Get the absolute url of compartment

    Returns:
        string: Absolute url
    """
    return '/%s/'%self.id

  def get_nb_ref(self):
    """Get number of references for compartment

    Returns:
        int: number of references for compartment
    """
    return Component.objects.filter(compartment=self).count()

  def get_nb_units(self):
    """Get number of units for compartment

    Returns:
        int: number of units for compartment
    """
    qty_sum = Component.objects.filter(compartment=self).aggregate(Sum('quantity')).get("quantity__sum")
    return qty_sum or 0

  def get_filling_rate(self):
    """Get the filling rate of compartment. Filling rate is a percentage representing the number of units in compartment relative to the maximum number of units in other compartments

    Returns:
        int: Filling rate in percent
    """
    if(self.get_nb_units()):
      max_filling = Component.objects.aggregate(Max('quantity')).get("quantity__max")
      filling_rate = int(100*self.get_nb_units()/max_filling)
      return filling_rate
    return 0

class Component(models.Model):
  """Class representing a component
  """
  id = models.AutoField(primary_key=True)
  category = models.ForeignKey(Category, related_name='category', null=True, on_delete=models.SET_NULL)
  title = models.CharField(max_length=255)
  ref = models.CharField(max_length=255, blank=True ,null=True)
  desc = models.TextField(blank=True, null=True)
  image = models.ImageField(upload_to='uploads/', blank = True, null=True)
  thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True, editable=False)
  date_added = models.DateTimeField(auto_now_add=True)
  date_updated = models.DateTimeField(auto_now=True)
  quantity = models.IntegerField()
  compartment = models.ForeignKey(Compartment, related_name='components', null=True, on_delete=models.SET_NULL)
  datasheet_url = models.URLField(blank=True, null=True)

  class Meta:
    ordering = ('-date_updated',)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    """Get the absolute url of component

    Returns:
        string: Absolute url
    """
    return '/%s/%s/'%(self.category.slug, self.id)

  def get_image(self):
    """Get component image url

    Returns:
        string: The component image url
    """
    if self.image:
      return base_url + self.image.url
    return ''

  def get_thumbnail(self):
    """Get the component thumbnail and build it before if not already done before

    Returns:
        string: Thumbnail url
    """
    if self.thumbnail:
      return base_url + self.thumbnail.url
    else:
      if self.image:
        self.thumbnail = make_thumbnail(self.image)
        self.save()
        return base_url + self.thumbnail.url
      else:
        return ''

  
    