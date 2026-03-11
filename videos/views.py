from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Video, Comment, Like
from .forms import VideoUploadForm, CommentForm

def home(request):
    videos = Video.objects.all()
    query = request.GET.get('q')
    if query:
        videos = videos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )
    
    context = {
        'videos': videos,
        'query': query
    }
    return render(request, 'home.html', context)

def video_detail(request, video_id):
    # ✅ Use primary key or slug consistently
    video = get_object_or_404(Video, video_id=video_id)
    video.increment_views()
    
    comments = Comment.objects.filter(video=video, parent_comment=None)
    related_videos = Video.objects.exclude(video_id=video_id)[:5]
    
    user_like = None
    if request.user.is_authenticated:
        user_like = Like.objects.filter(video=video, user=request.user).first()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.user = request.user
            comment.save()
            return redirect('video_detail', video_id=video_id)
    else:
        form = CommentForm()
    
    context = {
        'video': video,
        'comments': comments,
        'related_videos': related_videos,
        'comment_form': form,
        'user_like': user_like,
        'likes_count': video.get_likes_count(),
        'dislikes_count': video.get_dislikes_count(),
    }
    return render(request, 'video_detail.html', context)

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            
            # ✅ Process tags safely
            tags_string = request.POST.get('tags', '')
            if tags_string:
                video.tags = [tag.strip() for tag in tags_string.split(',')]
            
            video.save()
            return redirect('video_detail', video_id=video.video_id)
    else:
        form = VideoUploadForm()
    
    return render(request, 'upload.html', {'form': form})

@login_required
@require_POST
def like_video(request, video_id):
    video = get_object_or_404(Video, video_id=video_id)
    is_like = request.POST.get('is_like') == 'true'
    
    like, created = Like.objects.get_or_create(
        video=video,
        user=request.user,
        defaults={'is_like': is_like}
    )
    
    if not created:
        if like.is_like == is_like:
            like.delete()
            action = 'removed'
        else:
            like.is_like = is_like
            like.save()
            action = 'updated'
    else:
        action = 'added'
    
    return JsonResponse({
        'likes_count': video.get_likes_count(),
        'dislikes_count': video.get_dislikes_count(),
        'action': action
    })

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        video_id = comment.video.video_id
        comment.delete()
        return redirect('video_detail', video_id=video_id)
    return JsonResponse({'error': 'Unauthorized'}, status=403)
