from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from ..forms import *
from ..models import *
from ..serializers import *
import json
import openai
from django.db.models import Q

# Create your views here.
def main(request):
    return render(request, 'main.html')
def index(request):
    return render(request, 'index.html')


# 게시글 작성 화면
def write(request):
    return render(request, 'write.html')
   


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hanwooplz_app:login')  # You can change 'login' to the name of your login view.
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            user_id = request.user.id
            return redirect(reverse('hanwooplz_app:myinfo', args=[user_id]))  # Change 'profile' to your actual profile URL name
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'edit_profile.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {"form": form}
        return render(request, "registration/login.html", context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")  # Redirect to the main page
            else:
                # 로그인 실패 메시지를 추가하고 다시 로그인 페이지를 렌더링
                messages.error(request, "로그인에 실패했습니다. 올바른 아이디와 비밀번호를 입력하세요.")

        context = {"form": form}
        return render(request, "registration/login.html", context)

def log_out(request):
    logout(request)
    return redirect(reverse("hanwooplz_app:login"))

def myinfo(request, user_id):
    userinfo = UserProfile.objects.get(id=user_id)
    user_posts = Post.objects.filter(author=userinfo)

    selected_category = request.GET.get('category', 'postportfolio')

    posts = []

    for post in user_posts:
        if selected_category == 'postportfolio':
            category = 'portfolio'
            postcategory = PostPortfolio.objects.filter(post=post).first()
        elif selected_category == 'postproject':
            category = 'project'
            postcategory = PostProject.objects.filter(post=post).first()
        elif selected_category == 'postquestion':
            category = 'question'
            postcategory = PostQuestion.objects.filter(post=post).first()

        if postcategory:
            posts.append({
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'post_id': postcategory.id,
                "category": category,
            })

    context = {
        "user_id": userinfo.id,
        "username": userinfo.username,
        "full_name": userinfo.full_name,
        "job": userinfo.job,
        "tech_stack": userinfo.tech_stack,
        "career": userinfo.career,
        "career_detail": userinfo.career_detail,
        "introduction": userinfo.introduction,
        "posts": posts,
        "github_link": userinfo.github_link,
        "linkedin_link": userinfo.linkedin_link,
        "selected_category": selected_category,
        
    }
    return render(request, "myinfo.html", context)


def get_posts_by_category(request):
    category = request.GET.get('category')
    if category == 'post':
        posts = Post.objects.all()  # Post 모델의 게시물을 가져옵니다.
    elif category == 'postportfolio':
        posts = PostPortfolio.objects.all()  # PostPortfolio 모델의 게시물을 가져옵니다.
    elif category == 'postproject':
        posts = PostProject.objects.all()  # PostProject 모델의 게시물을 가져옵니다.
    elif category == 'postquestion':
        posts = PostQuestion.objects.all()  # PostQuestion 모델의 게시물을 가져옵니다.

    # 가져온 게시물을 템플릿에 전달하여 HTML로 렌더링합니다.
    context = {'posts': posts}
    return render(request, 'posts_by_category.html', context)

def post(request):
    return render(request, "post.html")

def post_list(request):
    return render(request, "post_list.html")


class ChatBot():
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model
        self.messages = []

    def ask(self, question):
        self.messages.append({
            'role': 'user',
            'content': question
        })
        res = self.__ask__()
        return res

    def __ask__(self):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        response = completion.choices[0].message['content']
        self.messages.append({
            'role': 'assistant',
            'content': response
        })
        return response

    def show_messages(self):
        return self.messages

    def clear(self):
        self.messages.clear()

def execute_chatbot(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        question = data.get('question')
        chatbot = ChatBot()
        response = chatbot.ask(question)
        chat_messages = chatbot.show_messages()
        
        chat_messages_json = [{'role': message['role'], 'content': message['content']} for message in chat_messages]
        
        return JsonResponse({"response": response, "chat_messages": chat_messages_json})
    
    return HttpResponse("Invalid Request")


def send_application(request):
    if request.method == 'POST':
        # 클라이언트로부터 전달받은 데이터 처리
        post_id = request.POST.get('postId')
        author_id = request.POST.get('authorId')

        # 실제로 여기서 게시물 작성자에게 참가 요청을 보내는 로직을 추가해야 합니다.

        # 요청이 성공적으로 처리되었다면 success를 true로 설정
        success = True
    else:
        success = False

    return JsonResponse({'success': success})

def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notifications.objects.filter(user=request.user).order_by('-created_at')

        notifications_list = []
        for notification in notifications:
            postinfo = Post.objects.get(id=notification.post.id)
            senderinfo = UserProfile.objects.get(id=notification.sender.id)
            notifications_list.append({
                'title': postinfo.title,
                'sender': senderinfo.username,
                'created_at': notification.created_at,
                'accept_or_not': notification.accept_or_not,
            })

        context = {
        "notifications_list": notifications_list,
        }
        return JsonResponse({'notifications': context})
    else:
        return JsonResponse({'notifications': []})
    
def accept_reject_notification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notification_id = data.get('notificationId')
            result = data.get('result')

            if notification_id is not None and result is not None:
                # 알림을 처리하고 결과를 저장하거나 다른 작업 수행
                try:
                    notification = Notifications.objects.get(id=notification_id)
                    if result == '수락':
                        notification.accept_or_not = True
                        notification.save()
                    if result == '거절':
                        notification.accept_or_not = False
                        notification.save()
                    # ...

                    response_data = {'success': True}
                    return JsonResponse(response_data)

                except Notifications.DoesNotExist:
                    response_data = {'success': False, 'error': '알림을 찾을 수 없습니다.'}
                    return JsonResponse(response_data)

            else:
                response_data = {'success': False, 'error': '잘못된 데이터 요청입니다.'}
                return JsonResponse(response_data)

        except json.JSONDecodeError as e:
            response_data = {'success': False, 'error': str(e)}
            return JsonResponse(response_data)

    else:
        response_data = {'success': False, 'error': 'POST 요청이 필요합니다.'}
        return JsonResponse(response_data)