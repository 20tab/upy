"""
TODO
"""
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def img_preview(request):
    pass
    """
    if request.is_ajax():
        id = request.POST.get("id_img")
        try:
            image_mc = UPYImageMetaContent.g11nFilter.all_current(request, image__pk = id)[0] 
        except:
            dict = {"status": "ko",}
        else:
            dict = {"status": "ok", "url_thumb": image_mc.image.thumbnail_admin.url, "title": image_mc.title, "alt": image_mc.alt}
        finally:
            data = simplejson.dumps(dict)
            return HttpResponse(data)
    """

def get_img_preview():
    pass
    """
    def img_preview(fk_image):
        img = fk_image.preview_img
        return '<img src="%s" />' % img.admin_thumbnail.url
    img_preview.short_description = "Image Preview"
    img_preview.allow_tags = True
    return img_preview
    """