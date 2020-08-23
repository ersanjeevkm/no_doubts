from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    QUESTION_CHOICE = [('Engg - UG (BE/B.Tech)', (
        ('BM', 'Bio-Medical Engg.'),
        ('CI', 'Civil Engg.'),
        ('CSE', 'Comp. Sci/ IT Engg.'),
        ('EEE', 'Elec. & Electronics Engg.'),
        ('ECE', 'Electronics & Comm Engg.'),
        ('GE', 'Geo Informatics'),
        ('IE', 'Industrial Engg.'),
        ('MF', 'Manufacturing Engg.'),
        ('MS', 'Material Science & Engg.'),
        ('MH', 'Mechanical Engg'),
        ('MI', 'Mining Engg.'),
        ('PT', 'Printing Tech.'),
    )),
     ('Engg - PG (ME/M.Tech)', (
        ('AEM', 'Applied Electronics'),
        ('BMM', 'Bio-Medical Engineering (M.E.)'),
        ('CMM', 'Coastal Management'),
        ('CSM', 'Communication Systems'),
        ('CAM', 'Computer Aided Design'),
        ('CIM', 'Computer Integrated Manuf.'),
        ('CSM', 'Computer Science & Engg. (M.E.)'),
        ('CEM', 'Construction Engg. & Management'),
        ('CNM', 'Control & Instrumentation Engg.'),
        ('ESM', 'Embedded Systems Tech.'),
        ('EEM', 'Energy Engineering'),
        ('EDM', 'Engineering Design'),
        ('ENM', 'Environmental Engineering'),
        ('EMM', 'Environmental Management'),
        ('GIM', 'Geo-Informatics (M.E.)'),
        ('HVM', 'High Voltage Engineering'),
        ('HWM', 'Hydrology & Water Resources Engg.'),
        ('IEM', 'Industrial Engineering'),
        ('ITM', 'Information Technology (M.E.)'),
        ('ICM', 'Internal Combustion Engg.'),
        ('IWM', 'Irrigation Water Management'),
        ('MSM', 'Manufacturing System & Management'),
        ('MEM', 'Medical Electronics'),
        ('MTM', 'Multimedia Technology'),
        ('NSM', 'Nano Science and Technology'),
        ('OCM', 'Optical Communication Engg.'),
        ('POM', 'Polymer Science and Engineering'),
        ('PEM', 'Power Electronics and Drives'),
        ('PSM', 'Power Systems Engineering'),
        ('PTM', 'Printing Technology (M.E.)'),
        ('PDM', 'Product Design & Development'),
        ('QEM', 'Quality Engg. and Management'),
        ('RAM', 'Refrigeration & Air Conditioning'),
        ('RSM', 'Remote Sensing'),
        ('SEM', 'Software Engineering'),
        ('SMM', 'Soil Mechanics & Foundation Engg.'),
        ('STM', 'Structural Engineering'),
        ('SOR', 'System Engg. & Operation Research'),
        ('UEM', 'Urban Engineering'),
        ('VDM', 'VLSI Design'),
     ))]
    field = models.CharField(max_length=3, choices=QUESTION_CHOICE)
    CHOICE = [
        (True, 'Notify Me'),
        (False, 'Don\'t Notify Me')
    ]
    notifications = models.BooleanField(choices=CHOICE, default=True)
    image = models.ImageField(upload_to='profile pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.username}\'s profile'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            resize = (300, 300)
            img.thumbnail(resize)
            img.save(self.image.path)
