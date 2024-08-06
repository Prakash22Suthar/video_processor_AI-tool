from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from allauth.account.forms import SignupForm
from .models import Video

class CustomSignupForm(SignupForm):
    def save(self, commit=True):
        user = super(CustomSignupForm, self).save(commit=False)
        # Customize user here
        if commit:
            user.save()
        return user
    
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']

    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(VideoForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = "Title For PDF"
    
    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            # Check if the file extension is allowed
            allowed_extensions = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', '3gp', 'mpeg']
            file_extension = video_file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError('Only video files are allowed.')
            
            # Check the file size for unauthorized users
            if self.user is None and video_file.size > 10000000:  # 10MB
                raise ValidationError('Video size limit exceeded for unauthorized users, login/signup to get more limit.')

            # Check the file size for authorized users
            elif self.user is not None and video_file.size > 100000000:  # 100MB
                raise ValidationError('Video size limit exceeded for authorized users.')

        return video_file