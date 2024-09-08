from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
import os
import requests
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import LoginView, SignupView
from .models import Video
from .utils import extract_audio, audio_to_text, text_to_pdf
from .forms import VideoForm

# class based view


class UserLogin(LoginView):
    """user login view"""
    success_url = reverse_lazy("video_app:profile")


class UserSignupView(SignupView):
    """user signup view"""
    template_name = "account/signup.html"
    success_url = reverse_lazy("video_app:login")

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(reverse('account_login'))


# class GoogleSignUpView(View):
#     """SignUp and get access and refresh token with Google Account"""

#     def get(self, request, access_token):
#         user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
#         user_info_response = requests.get(
#             user_info_url, headers={"Authorization": f"Bearer {access_token}"}, timeout="100000"  # noqa
#         )
#         user_info = user_info_response.json()

        # user, created = User.objects.get_or_create(
        #     email=user_info["email"],
        #     defaults={
        #         "name": user_info["name"],
        #         "profile_pic": user_info["picture"],
        #         "user_id": User.objects.last().user_id + 1,
        #         "account_varified": True,
        #     },
        # )
        # social_account_password = settings.SOCIAL_ACCOUNT_PASSWORD
        # user.set_password(social_account_password)
        # user.save()

        # return redirect('video_app:login') 


class HomepageView(CreateView):

    """This is home page and also to save video """

    model = Video
    form_class = VideoForm
    template_name = 'index.html'
    success_url = reverse_lazy('video_app:process_video')

    def get_success_url(self):
        video = Video.objects.last()
        return reverse_lazy('video_app:process_video', kwargs={'pk': video.id})


class ProfileView(LoginRequiredMixin, CreateView):

    """ User profile page after login"""

    template_name = "account/profile.html"

    model = Video
    form_class = VideoForm
    success_url = reverse_lazy('video_app:process_video')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        video = Video.objects.last()
        return reverse_lazy('video_app:process_video', kwargs={'pk': video.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user 
        return context


class ProcessVideoView(View):
    
    """View to process uploaded video in these steps: 
    1. Get audio,
    2. Convert this audio to text,
    3. Format the text according to PDF page fit,
    4. Draw PDF title and text extracted from video,
    5. Generate the PDF
    """

    def get(self, *args, **kwargs):
        """get"""
        pk = kwargs.get('pk')
        video = get_object_or_404(Video, pk=pk)
        video_path = video.video_file.path
        video_title = video.title.title()
        video_ext = os.path.splitext(video_path)[1].lower()
        audio_path = video_path.replace(video_ext, '.wav')
        pdf_filename = f"{video.title.replace(' ', '_')}.pdf"
        pdf_filename = os.path.join('pdf', pdf_filename)
        pdf_path = os.path.join(os.path.dirname(video_path), pdf_filename)

        # Extract audio
        extract_audio(video_path, audio_path)

        # Convert audio to text
        text = audio_to_text(audio_path)

        # Generate PDF
        text_to_pdf(video_title, text, pdf_path)

        # Save PDF file path to the model
        video.pdf_file = f"files/{pdf_filename}"
        video.status = 'completed'
        video.save()

        return redirect('video_app:download_pdf', pk=video.pk) 


class DownloadPdfView(TemplateView):
    """ get pdf url to download pdf """

    template_name = 'video/process_video.html'

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        video = get_object_or_404(Video, pk=pk)
        context['pdf_url'] = video.pdf_file.url
        return context


# class ProcessVideoView(TemplateView):
    
#     """view to process uploaded video in this setps: 
#     1. get audio , 
#     2. convert this audio to text
#     3. format the text according to pdf page fit
#     4. draw pdf title and text extracted form video
#     5. generate the pdf
#     """

#     template_name = 'video/process_video.html'

#     def get_context_data(self, pk, **kwargs):
#         context = super().get_context_data(**kwargs)
#         video = get_object_or_404(Video, pk=pk)
#         print('➡ video_processor/video_app/views.py:42 video:', video.video_file)
#         print('➡ video_processor/video_app/views.py:42 video:', video.video_file.path)
#         video_path = video.video_file.path
#         video_title = video.title.title()
#         audio_path = video_path.replace('.mp4', '.wav')
#         pdf_filename = f"{video.title.replace(' ', '_')}.pdf"
#         pdf_filename = os.path.join('pdf', pdf_filename)
#         pdf_path = os.path.join(os.path.dirname(video_path), pdf_filename)

#         # Extract audio
#         extract_audio(video_path, audio_path)

#         # Convert audio to text
#         text = audio_to_text(audio_path)

#         # Generate PDF
#         text_to_pdf(video_title, text, pdf_path)

#         # Save PDF file path to the model
#         # import ipdb
#         # ipdb.set_trace()

#         video.pdf_file = f"files/{pdf_filename}"
#         video.status = 'completed'
#         video.save()

#         context['pdf_url'] = video.pdf_file.url
#         return context
    

# code function based view

# from django.shortcuts import render, redirect
# from .forms import VideoForm

# import os
# from django.shortcuts import render, get_object_or_404
# from .models import Video
# from .utils import extract_audio, audio_to_text, text_to_pdf



# def home_page(request):

#     """Home page of video processor site"""

#     if request.method == 'GET':
#         return render(request, 'video/index.html')

# def upload_video(request):
#     """fucntion to get uploaded video"""
#     if request.method == 'POST':
#         form = VideoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('video_app:process_video')
#     else:
#         form = VideoForm()
#     return render(request, 'video/upload_video.html', {'form': form})


# def process_video(request, pk):
#     """fucntion to process uploaded video"""
#     video = Video.objects.get(id=pk)
#     video_path = video.video_file.path
#     video_title = video.title
#     audio_path = video_path.replace('.mp4', '.wav')
#     pdf_path = video_path.replace('.mp4', '.pdf')
#     # Extract audio
#     extract_audio(video_path, audio_path)

#     # Convert audio to text
#     text = audio_to_text(audio_path)

#     # Generate PDF
#     text_to_pdf(video_title, text, pdf_path)

#     return render(request, 'video/process_video.html', {'pdf_url': pdf_path})
