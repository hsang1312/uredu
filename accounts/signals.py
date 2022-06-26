from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from accounts import models

@receiver(post_save, sender=models.Users)
def create_profile(sender, instance, created, **kwargs):
    # Khi tạo user thì sẽ chạy điều kiện để đồng bộ hóa dữ liệu với profile
    if created:
        user = instance
        models.Profiles.objects.create(
            user=user,
            email=user.email,
            fullname=user.fullname,
            role=(models.Roles.objects.get(id=user.role))
        )
        
@receiver(post_save, sender=models.Profiles)
def update_profile(sender, instance, created, **kwargs):
    # Khi update profile thì sẽ chạy điêu kiện để đồng hóa dữ liệu với bảng User
    profile = instance
    user = profile.user
    
    if created == False:
        try:
            user.email = profile.email
            user.fullname = profile.fullname
            user.role = profile.role
            user.save()
        except:
            pass
  
@receiver(post_delete, sender=models.Profiles)
def delete_profile(sender, instance, **kwargs):
    # Xóa Profile thì sẽ xóa luôn cả User
    try:
        profile = instance
        user = profile.user
        user.delete()
    except:
        pass