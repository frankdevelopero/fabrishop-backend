from django.shortcuts import render, redirect
from django.views.generic.base import View


class IndexView(View):
    def get(self, request):
        # host = request.get_host()
        # slug = host.split('.')[0]
        # if slug and slug != "127":
        #     print(slug)
        #     return redirect('index_store')
        return render(request, 'core/index.html')
