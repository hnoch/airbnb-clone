# from datetime import datetime
# from django.shortcuts import render
# from django.http import HttpResponse


# def all_rooms(request):
#     # return HttpResponse(content="<h1>hello</h1>")
#     now = datetime.now()
#     hungry = True
#     return render(request, "all_rooms.html", context={
#         "now": now, "hungry": hungry
#     })

# 수동적 페이지네이션 (~#11,3)
# from math import ceil   # ceil 올림
# from django.shortcuts import render
# from . import models


# def all_rooms(request):
#     page = int(request.GET.get("page", 1))
#     page = int(page or 1)                   # 페이지 디폴트 값 1 설정
#     page_size = 10
#     limit = page_size * page
#     offset = limit - page_size
#     all_rooms = models.Room.objects.all()[offset:limit]
#     page_count = ceil(models.Room.objects.count() / page_size)
#     return render(
#         request,
#         "rooms/home.html",
#         {
#             "rooms": all_rooms,
#             "page": page,
#             "page_count": page_count,
#             "page_range": range(1, page_count),

#         }
#     )


# 장고 페이지네이터 사용 (~#11,6)
# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage
# from . import models


# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()       # rooms > models 에서 방 리스트 반환
#     paginator = Paginator(room_list, 10, orphans=5)        # 방 리스트를 10개씩 나눔

#     try:
#         # 나눈 리스트의 개수 반환 (100이면 개수가 10)/ get_page 는 paginator에서 지원
#         rooms = paginator.page(int(page))
#         return render(request, "rooms/home.html", {"page": rooms, })
#     except EmptyPage:   # 빈 페이지를 url에 입력했을 경우
#         return redirect("/")   # / 경로로 리다이렉트(되넘겨줌)


# 클래스 리스트 뷰 (~#11.8)
from django.views.generic import ListView, DetailView, View
# from django.http import Http404
# from django.urls import reverse
from django.shortcuts import redirect, render
from django_countries import countries
from django.core.paginator import Paginator
from . import models, forms


class HomeView(ListView):
    """ HomeView Definition """

    model = models.Room
    paginate_by = 10        # 보여질 개수
    ordering = "created"    # 정렬순서 (필드 반환)
    context_object_name = "rooms"

# #12.4


class RoomDetail(DetailView):
    """ RoomDetail Definition """
    model = models.Room

# 13.9

    # 13.6~


def search(request):
    country = request.GET.get("country")

    if country:

        form = forms.SearchForm(request.GET)

        if form.is_valid():
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if beds is not None:
                filter_args["beds__gte"] = beds

            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                # models.py 에서의 host 를 fk 로 받아와서 사용
                filter_args["host__superhost"] = True

            for amenity in amenities:
                filter_args["amenities"] = amenity

            for facility in facilities:
                filter_args["facilities"] = facility

            qs = models.Room.objects.filter(
                **filter_args).order_by("-created")

            paginator = Paginator(qs, 10, orphans=5)

            page = request.GET.get("page", 1)

            rooms = paginator.get_page(page)

            return render(request, "rooms/search.html", {"form": form, "rooms": rooms})
    else:
        form = forms.SearchForm()

    return render(request, "rooms/search.html", {"form": form})


# #13.0~6


# def search(request):
#     # 검색창 city 값을 받아옴 / 디폴트값 any 설정
#     city = request.GET.get("city", "Anywhere")
#     city = str.capitalize(city)         # city 맨앞 대문자화
#     country = request.GET.get("country", "KR")
#     room_type = int(request.GET.get("room_type", 0))
#     price = int(request.GET.get("price", 0))
#     guests = int(request.GET.get("guests", 0))
#     bedrooms = int(request.GET.get("bedrooms", 0))
#     beds = int(request.GET.get("beds", 0))
#     baths = int(request.GET.get("baths", 0))
#     instant = bool(request.GET.get("instant", False))
#     superhost = bool(request.GET.get("superhost", False))
#     s_amenities = request.GET.getlist("amenities")
#     s_facilities = request.GET.getlist("facilities")

#     form = {
#         "city": city,
#         "s_country": country,
#         "s_room_type": room_type,
#         "price": price,
#         "guests": guests,
#         "bedrooms": bedrooms,
#         "beds": beds,
#         "baths": baths,
#         "s_amenities": s_amenities,
#         "s_facilities": s_facilities,
#         "instant": instant,
#         "superhost": superhost,

#     }

#     room_types = models.RoomType.objects.all()
#     amenities = models.Amenity.objects.all()
#     facilities = models.Facility.objects.all()
#     choice = {
#         "countries": countries,
#         "room_types": room_types,
#         "amenities": amenities,
#         "facilities": facilities,
#     }

#     # 검색 필터링! (#13.5 6)
#     filter_args = {}

#     if city != "Anywhere":
#         filter_args["city__startswith"] = city

#     filter_args["country"] = country

#     if room_type != 0:
#         filter_args["room_type__pk"] = room_type

#     if price != 0:
#         filter_args["price__lte"] = price

#     if guests != 0:
#         filter_args["guests__gte"] = guests

#     if bedrooms != 0:
#         filter_args["bedrooms__gte"] = bedrooms

#     if beds != 0:
#         filter_args["beds__gte"] = beds

#     if baths != 0:
#         filter_args["baths__gte"] = baths

#     if instant is True:
#         filter_args["instant_book"] = True

#     if superhost is True:
#         # models.py 에서의 host 를 fk 로 받아와서 사용
#         filter_args["host__superhost"] = True

#     if len(s_amenities) > 0:
#         for s_amenity in s_amenities:
#             filter_args["amenities__pk"] = int(s_amenity)

#     if len(s_facilities) > 0:
#         for s_facility in s_facilities:
#             filter_args["facilities__pk"] = int(s_facility)

#     rooms = models.Room.objects.filter(**filter_args)

#     return render(request, "rooms/search.html", {**form, **choice, "rooms": rooms})


# ~#12.4 함수형방식
# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {'room': room})
#     except models.Room.DoesNotExist:    # 페이지 존재 않을 경우
#         # return redirect(reverse("core:home"))      # 홈으로 이동
#         raise Http404()            # 404 에러 페이지로 이동 > 에러는 raise로 받음!

    # #11.8
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.now()
    #     context["now"] = now
    #     return context
