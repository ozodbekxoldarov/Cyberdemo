
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.views.generic import ListView, DetailView
# from django.views.generic.edit import UpdateView, DeleteView, CreateView
# from django.urls import reverse_lazy

# from .models import Article

# from django.views.generic.edit import FormMixin
# from .forms import CommentForm
# class ArticleListView(ListView):
#     model = Article
#     template_name = 'article_list.html'

# # class ArticleDetailView(DetailView):
# #     model = Article
# #     template_name = 'article_detail.html'


# class ArticleDetailView(FormMixin, DetailView): # FormMixin qo'shildi
#     model = Article
#     template_name = 'article_detail.html'
#     form_class = CommentForm # Formani klassga bog'laymiz

#     def get_success_url(self):
#         # Izoh yozilgandan keyin yana shu maqolaning o'ziga qaytaradi
#         return reverse_lazy('article_detail', kwargs={'pk': self.object.id})

#     def post(self, request, *args, **kwargs):
#         # POST so'rovi kelganda (izoh tugmasi bosilganda) ishlaydi
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         # Forma validatsiyadan o'tganda ma'lumotlarni saqlaymiz
#         comment = form.save(commit=False)
#         comment.article = self.object # Izohni shu maqolaga biriktiramiz
#         comment.author = self.request.user # Izoh egasini aniqlaymiz
#         comment.save()
#         return super().form_valid(form)




# class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Article
#     fields = ('title','summary', 'body','photo',)
#     template_name = 'article_edit.html'

#     def test_func(self):
#         obj = self.get_object()
#         return obj.author == self.request.user

# class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Article
#     template_name = 'article_delete.html'
#     success_url = reverse_lazy('article_list')

#     def test_func(self):
#         obj = self.get_object()
#         return obj.author == self.request.user

# class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Article
#     template_name = 'article_new.html'
#     fields = ('title','summary','body','photo')

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     # user superuser ekanini tekshirish
#     def test_func(self):
#         return self.request.user.is_superuser


import pickle
import os
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.conf import settings

from .models import Article
from django.views.generic.edit import FormMixin
from .forms import CommentForm

# Model va vectorizer yuklash
MODEL_PATH = os.path.join(settings.BASE_DIR, 'sentiment_model.pkl')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'vectorizer.pkl')

with open(MODEL_PATH, 'rb') as f:
    sentiment_model = pickle.load(f)

with open(VECTORIZER_PATH, 'rb') as f:
    vectorizer = pickle.load(f)


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'


class ArticleDetailView(FormMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user

        # Sentiment aniqlash
        vec = vectorizer.transform([comment.comment])
        prob = sentiment_model.predict_proba(vec)[0]
        if prob[1] >= 0.5:
            comment.sentiment = 'Ijobiy'
            comment.sentiment_foiz = round(prob[1] * 100, 1)
        else:
            comment.sentiment = 'Salbiy'
            comment.sentiment_foiz = round(prob[0] * 100, 1)

        comment.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'summary', 'body', 'photo',)
    template_name = 'article_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'summary', 'body', 'photo')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser