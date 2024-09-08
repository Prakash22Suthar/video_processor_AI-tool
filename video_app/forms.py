from django.core.exceptions import ValidationError
from django import forms
from allauth.account.forms import SignupForm
from .models import Video


class CustomSignupForm(SignupForm):
    """ user signup form """
    def save(self, request=True):
        user = super(CustomSignupForm, self).save(request=False)
        # Customize user here
        if request:
            user.save()
        return user


class VideoForm(forms.ModelForm):
    """upload video form class"""

    class Meta:
        """ meta class of model"""
        model = Video
        fields = ['title', 'video_file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(VideoForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = "Title For PDF"

    def clean_video_file(self):
        """
        validate video file before upload
        """
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            # Check if the file extension is allowed
            allowed_extensions = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', '3gp', 'mpeg'] # noqa
            file_extension = video_file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError('Only video files are allowed.')
            
            # Check the file size for unauthorized users
            if self.user is None and video_file.size > 10000000:  # 10MB
                raise ValidationError('Video size limit exceeded for unauthorized users, login/signup to get more limit.') # noqa

            # Check the file size for authorized users
            elif self.user is not None and video_file.size > 100000000:  # 100MB  # noqa
                raise ValidationError('Video size limit exceeded for authorized users.') # noqa

        return video_file
