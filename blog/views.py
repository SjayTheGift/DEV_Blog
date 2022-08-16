from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import generic

from .forms import CommentForm
from .models import Post


class PostList(generic.ListView):
    queryset = Post.objects.filter(status="publish").order_by('-created')
    paginate_by = 10
    template_name = "blog/home.html"


class PostDetailsView(generic.View):
    template_name = 'post_detail.html'
    new_comment = None

    def get(self, request, slug, *args, **kwargs):
        comment_form = CommentForm()
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(active=True)

        context = {
            'post': post,
            'comments': comments,
            'new_comment': self.new_comment,
            'comment_form': comment_form
        }

        return render(request, self.template_name, context)

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(active=True)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            self.new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            self.new_comment.post = post
            # Save the comment to the database
            self.new_comment.save()

        context = {
            'post': post,
            'comments': comments,
            'new_comment': self.new_comment,
            'comment_form': comment_form
        }

        return render(request, self.template_name, context)


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'body', 'status']
    template_name = "post_form.html"
    # redirect = 'blog:post_list'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'body', 'status']
    template_name = "post_form.html"
    success_message = 'Post Updated successfully!!!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Post
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy('blog:post_list')
    success_message = 'Post Deleted successfully!!!'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
