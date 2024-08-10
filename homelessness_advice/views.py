from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Homeless

"""
Handles the display of the list of homelessness advice posts.
Only published posts are shown, ordered by creation date in descending order.
"""


class HomelessList(View):
    def get(self, request, *args, **kwargs):
        homeless_posts = Homeless.objects.filter(
            status='published').order_by('-created_on')
        return render(
            request,
            'homelessness_advice/homelessness_advice_list.html',
            {'homeless_posts': homeless_posts}
        )


"""
Handles the display of a single homelessness advice post's detail view.
Fetches the post using its slug and displays it.
"""


class HomelessDetail(View):
    def get(self, request, slug, *args, **kwargs):
        homeless_post = get_object_or_404(Homeless, slug=slug)
        return render(
            request,
            'homelessness_advice/homelessness_advice_detail.html',
            {'homeless_post': homeless_post}
        )
