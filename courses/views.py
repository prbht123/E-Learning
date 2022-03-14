from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from braces.views import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
# Create your views here.

""" 
class ManageCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'
    def get_queryset(self):
        qs = super(ManageCourseListView, self).get_queryset()
        print(qs.__dict__)
        return qs.filter(owner=self.request.user) """

class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        print(qs.filter(owner=self.request.user))
        return qs.filter(owner=self.request.user)



class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    model = Course
    

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    #success_url = reverse('manage_course_list')
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'

class CourseCreateView(PermissionRequiredMixin,OwnerCourseEditMixin, CreateView):
    #pass
    permission_required = 'courses.add_course'

class CourseUpdateView(PermissionRequiredMixin,OwnerCourseEditMixin, UpdateView):
    template_name = 'courses/manage/course/form.html'
    permission_required = 'courses.change_course'

class CourseDeleteView(PermissionRequiredMixin,OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    #success_url = reverse('manage_course_list')
    permission_required = 'courses.delete_course'



class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,id=pk,owner=request.user)
        return super(CourseModuleUpdateView,self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,'formset': formset})


    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,'formset': formset})


