from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post, Profile
from .forms import CommentForm, EditUserForm, EditProfileForm
from django.urls import reverse_lazy
from django.contrib import messages


def landing_page(request):
    """
    Render the landing_page.html template
    """
    return render(request, "landing_page.html")


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostCreateView(generic.CreateView):
    model = Post
    template_name = "new_post.html"
    fields = ['title','slug', 'author', 'featured_image', 'excerpt', 'content', 'status']
    


class UpdatePostView(generic.UpdateView):
    model = Post
    template_name = "update_post.html"
    fields = ['title','slug', 'author', 'featured_image', 'excerpt', 'content', 'status']

class DeletePostView(generic.DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy('posts')
    fields = ['title','slug', 'author', 'featured_image', 'excerpt', 'content', 'status']    

class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

#def profile(request):
 #   """
  #  Render the landing_page.html template
   # """
    #return render(request, "profile.html")

def profile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        edit_user = EditUserForm(request.POST, instance=request.user)
        edit_profile = EditProfileForm(request.POST,
                                       request.FILES,
                                       instance=request.user.profile)
        if edit_user.is_valid() and edit_profile.is_valid():
            edit_user.save()
            edit_profile.save()
            messages.success(request, f'Profile updated successfully')
            return redirect('profile')
    else:
        profile = Profile.objects.get(user=request.user)
        edit_user = EditUserForm(instance=request.user)
        edit_profile = EditProfileForm(instance=request.user.profile)

    context = {
        'profile': profile,
        'edit_user': edit_user,
        'edit_profile': edit_profile
    }
    return render(request, 'profile.html', context)

