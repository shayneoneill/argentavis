from django.shortcuts import render, redirect

# Create your views here.
from assets.forms import MediaTypeForm
from assets.models import MediaType




def media_types(request):
    mt = MediaType.objects.all()
    mtf = MediaTypeForm()
    return render(request,
                  'asset_types.html',
                  {'media_types': mt,
                   'media_type_form':mtf})

def media_types_post(request):
    mtf = MediaTypeForm(request.POST)
    model = mtf.save()
    return redirect('media_types')