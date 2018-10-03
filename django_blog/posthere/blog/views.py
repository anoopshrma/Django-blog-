from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm
from django.views.generic import (TemplateView,ListView,
                                 DetailView,CreateView,UpdateView,DeleteView)
# Create your views here.

class AboutView(TemplateView):
    template_name='about.html'
    
class PostList(LoginRequiredMixin,ListView):
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetail(DetailView):
    model=Post


#LoginRequiredMixin works like  decorators.Decorators cannot be used inside generic templates
#as they are used in function views .Works similar to the decorator @login_required
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html' #afterthe login gets successful it redirects the user to this programmer designed url
    form_class=PostForm #imports and present the form in html page
    model=Post #imports the model to inherit model objects.


class UpdatePostView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html' #afterthe login gets successful it redirects the user to this programmer designed url
    form_class=PostForm #imports and present the form in html page
    model=Post #imports the model to inherit model objects.


class DeletePostView(LoginRequiredMixin,DeleteView):
        model=Post
        success_url=reverse_lazy('blog:post_list')

    
class DraftPostView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name='blog/post_list.html'

    model=Post
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if 'post_pics' in request.FILES:
        post.post_pic=request.FILES['post_pics']
    post.save()
    post.publish()
    return redirect('blog:post_detail',pk=pk)
#Views for Commment model

@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('blog:post_detail',pk=post.pk)
    else:
        form=CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blog:post_detail',pk=comment.post.pk)

@login_required
def comment_delete(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('blog:post_detail',pk=post_pk)
