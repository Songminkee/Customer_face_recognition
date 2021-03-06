from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UploadMultiImageForm
from .models import Borrower, UserBorrower, User
from .face_recognition import face_recognition, save_features

from io import BytesIO
from PIL import Image
import base64
import cv2
import numpy as np


def get_str_to_img(b64_str):
    imgdata = base64.b64decode(b64_str)
    image = Image.open(BytesIO(imgdata))

    return np.array(image)


def get_img_to_str(img):
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode('ascii')

    return img_str


class RegistrationView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    template_name = 'registration/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class FaceRecognitionView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    template_name = 'registration/face_selection.html'

    def post(self, request, *args, **kwargs):

        form = UploadMultiImageForm(request.POST, request.FILES)
        if form.is_valid():
            img_raw = form.cleaned_data['img']
            print(np.array(img_raw).shape)
            # for img_raw in form.cleaned_data['img']:
            img = Image.open(img_raw).convert('RGB')

            # reshape
            will_reshape = False
            if will_reshape:
                w, h = img.size
                ratio = w / h
                new_w = int(ratio * 480)
                new_h = 480
                img = img.resize((new_w, new_h))
        else:
            img_str = request.POST['img'].split(',')[-1]
            img_raw = get_str_to_img(img_str)
            print(img_raw.shape)
            img = Image.fromarray(img_raw).convert('RGB')

        print(img.size)

        img_origin = get_img_to_str(img)
        img_strs = list()

        imgs = face_recognition(img)
        for img in imgs:
            img_str = get_img_to_str(Image.fromarray(img))
            img_strs.append(img_str)

        context = self.get_context_data(**kwargs)
        context['img_origin'] = img_origin
        context['zip_range'] = zip(range(len(img_strs)), img_strs)

        return self.render_to_response(context)


class FaceSaveView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    template_name = 'registration/save_face.html'

    def post(self, request, *args, **kwargs):
        # print(request.POST, request.FILES)
        data = request.POST
        print(data.keys())
        b_names = request.POST.getlist('b_name')
        checklist = request.POST.getlist('images')
        images = request.POST.getlist('hidden_image')
        origin_img = request.POST['origin_img']

        checklist = list(map(int, checklist))
        images = list(map(get_str_to_img, images))
        saved_images = list()
        saved_names = list()
        saved_size = list()
        for i in checklist:
            b_names[i] = b_names[i].lstrip().rstrip()
            save_features(images[i], b_names[i], request.user.uid)

            # if not Borrower.objects.filter(b_name=b_names[i]).exists():
            if not Borrower.objects.filter(userborrower__uid=request.user.uid, b_name=b_names[i]).exists():
                borrower = Borrower(b_name=b_names[i])
                user = User.objects.get(uid=request.user.uid)
                print(user.uid)
                print(type(user))
                userborrower = UserBorrower(uid=user, bid=borrower)
                borrower.save()
                userborrower.save()

            saved_images.append(get_img_to_str(Image.fromarray(images[i])))
            saved_names.append(b_names[i])
            saved_size.append(images[i].shape)
            print(images[i].shape)

        context = self.get_context_data(**kwargs)
        context['img_origin'] = origin_img
        context['zip_range'] = zip(range(len(saved_images)), saved_images, saved_names, saved_size)

        return self.render_to_response(context)
