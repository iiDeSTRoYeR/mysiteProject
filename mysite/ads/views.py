from .models import Ad, Comment
from .forms import CreateForm, CommentAd
from django.views import View
from myarts.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.http import FileResponse


class AdListView(OwnerListView):
    model = Ad
    # By convention:
    # template_name = "myarts/article_list.html"


class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    def get(self, request, pk) :
        x = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_ad = CommentAd()
        context = { 'ad' : x, 'comments': comments, 'comment_ad': comment_ad }
        return render(request, self.template_name, context)

class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get (self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        if request.FILES:
            pic.picture = request.FILES['picture']
        pic.save()
        return redirect(self.success_url)

class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        if request.FILES:
            pic.picture = request.FILES['picture']
        pic.save()

        return redirect(self.success_url)

class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad

    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(AdDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):         #overrides delete method to delete actual file from disk
        self.object = self.get_object()
        if self.object.picture:
            self.object.picture.delete()                #removes pic from disk
        self.object.delete()                            #removes object from database
        return redirect(reverse_lazy('ads:all'))

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])


def stream_file(request, pk):                   #organizes urls of pictures stored on disk
    pic = get_object_or_404(Ad, id=pk)
    response = FileResponse(pic.picture)
    return response

def load_ads(request):
    ad_id = request.GET.get('ad_id')
    ad = Ad.objects.get(id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})