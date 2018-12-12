from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.views.generic.edit import FormView

from .forms import FileFieldForm


class FileFieldView(FormView):
    form_class = FileFieldForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        if form.is_valid():
            for f in files:
                with open(Path(settings.MEDIA_ROOT + "/" + f.name).resolve(), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

            return JsonResponse({'form': True})
        else:
            return JsonResponse({'form': False})


upload_files = FileFieldView.as_view()
