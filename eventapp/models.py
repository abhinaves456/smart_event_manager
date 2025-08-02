from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File

# Model to add an 'is_admin' role to the standard User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Model for creating events - CHECK THIS CLASS NAME
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Model for tickets that links a User to an Event
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

    def __str__(self):
        return f"Ticket for {self.user.username} at {self.event.title}"

    # Automatically generate QR code when a ticket is saved
    def save(self, *args, **kwargs):
        # The QR code generation is currently commented out to simplify debugging.
        # We will re-enable this in a later step.
        # if not self.qr_code:
        #     qr_content = f"Ticket ID: {self.id}\nEvent: {self.event.title}\nUser: {self.user.username}"
        #     qr_image = qrcode.make(qr_content)
        #     buffer = BytesIO()
        #     qr_image.save(buffer, format='PNG')
        #     file_name = f'ticket_{self.id}_qr.png'
        #     self.qr_code.save(file_name, File(buffer), save=False)
        super().save(*args, **kwargs)