from django.shortcuts import render,redirect

from django.views import View
from .models import Topic

from django.db.models import Q





class BbsView(View):

    def get(self, request, *args, **kwargs):


        #検索はできるが、これではスペース区切りの複数検索に対応できていない
        """
        if "search" in request.GET:
            topics  = Topic.objects.filter(comment__contains=request.GET["search"]).order_by("-dt")
        else:
            topics  = Topic.objects.all().order_by("-dt")
        """

        if "search" in request.GET:

            #(1)キーワードが空欄もしくはスペースのみの場合、ページにリダイレクト
            if request.GET["search"] == "" or request.GET["search"].isspace():
                return redirect("bbs:index")

            #(2)キーワードをリスト化させる(複数指定の場合に対応させるため)
            search      = request.GET["search"].replace("　"," ")
            search_list = search.split(" ")

            #(3)クエリを作る
            query       = Q()
            for word in search_list:
                #TIPS:AND検索の場合は&を、OR検索の場合は|を使用する。

                if "option" in request.GET:
                    query |= Q(comment__contains=word)
                else:
                    query &= Q(comment__contains=word)


            #(4)作ったクエリを実行
            topics      = Topic.objects.filter(query)
        else:
            topics      = Topic.objects.all().order_by("-dt")



        context = { "topics":topics }

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        posted  = Topic( comment = request.POST["comment"] )
        posted.save()

        return redirect("bbs:index")

index   = BbsView.as_view()

