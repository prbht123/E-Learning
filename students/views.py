from django.shortcuts import render
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from braces.views import LoginRequiredMixin
from .forms import CourseEnrollForm
from students.forms import CourseEnrollForm
from courses.models import Course
from django.http import HttpResponseRedirect
# Create your views here.

class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    #success_url = reverse_lazy('student_course_list')
    def form_valid(self, form):
        result = super(StudentRegistrationView,self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],password=cd['password1'])
        login(self.request, user)
        return result

    def get_success_url(self):
        return reverse('student_course_list')



class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm
    template_name="form.html"
    #success_url = '/students/course/5/'
    def form_valid(self, form):
        print("0000000000000000000888888888888888888888")
        self.course = form.cleaned_data['course']
        print(self.course.id)
        self.course.students.add(self.request.user)
        print(self)
        #return super(StudentEnrollCourseView,self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        print("00000000000000000000000")
        return reverse('student_course_detail',args=[self.course.id])

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'
    def get_context_data(self, **kwargs):
        print("0000000000000000000000000")
        context = super(CourseDetailView,self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})
        return context

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'
    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'
    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView,self).get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
            id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        
        return context
        

