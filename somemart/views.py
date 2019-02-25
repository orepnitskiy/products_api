import json
import base64
from django.contrib.auth import authenticate
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Length, Range
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from .models import Item, Review


class AddItemView(View):
    """ View для создания товара """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AddItemView, self).dispatch(request, *args, **kwargs)
	
	
    def post(self, request):
        try:
            document = json.loads(request.body)
            schema = AddItemReview(strict=True)
            valid_data = schema.load(document)
            auth = valid_data.data['Authorization'].split()
            user = None
            if len(auth) == 2 and auth[0].lower() == "basic":
                username, password = base64.b64decode(auth[1]).split(":")
                user = authenticate(username=username, password=password)
                try:
                    if not user.is_staff: 
                        return HttpResponse(status=403)
                except AttributeError:
                    return HttpResponse(status=401)
            else:
                return HttpResponse(status=401)
                item = Item(title=valid_data.data['title'], description=valid_data.data['description'], price=valid_data.data['price'])
                item.save()
                data = {'id': item.id}
                return JsonResponse(data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'error': exc.messages}, status=400)


class PostReviewView(View):
    """ View для создания отзыва о товаре """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PostReviewView, self).dispatch(request, *args, **kwargs)
    def post(self, request, item_id):
        try:
            req = json.loads(request.body)
            schema = PostItemReview(strict=True)
            valid_data = schema.load(req)
            review = Review(text=valid_data.data['text'], grade=valid_data.data['grade'],
                            item=Item.objects.get(pk=item_id))
            review.save()
            data = {'id': item_id}
            return JsonResponse(data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)
        except Exception:
            return JsonResponse({'error': 'no user with that id'}, status=404)


class GetItemView(View):
    """
    View для получения информации о товаре.
    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.

    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GetItemView, self).dispatch(request, *args, **kwargs)
    def get(self, request, item_id):
        try:
            entries = []
            req_item = Item.objects.get(pk=item_id)
            for x in Review.objects.all():
                if x_item == req_item:
                    entries.append(x)
            data = model_to_dict(item)
            data["reviews"] = []
            if len(entries) > 5:
                entries = entries[:5]
            for entry in entries:
                    data["reviews"].append(model_to_dict(entry))
            return JsonResponse(data, status=200)
        except Exception:
            return JsonResponse({'error': 'no such id'}, status=404)


class AddItemReview(Schema):
    Authorization = fiels.Str(required=True)
    title = fields.Str(validate=Length(1, 64), required=True)
    description = fields.Str(validate=Length(1, 1024), required=True)
    price = fields.Int(validate=Range(1, 1000000), required=True)


class PostItemReview(Schema):
    text = fields.Str(validate=Length(1, 1024), required=True)
    grade = fields.Int(validate=Range(1, 10), required=True)
