from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, View
from webapp.models import Issue
from webapp.forms import IssueForm


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issues = Issue.objects.all()
        context['issues'] = issues
        return context


class IssueView(TemplateView):
    template_name = 'issue_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issue = get_object_or_404(Issue, pk=self.kwargs.get('pk'))
        context['issue'] = issue
        return context


class IssueCreatView(TemplateView):
    template_name = 'issue_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IssueForm()
        return context

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            issue = Issue.objects.create(
                summary=form.cleaned_data['summary'],
                description=form.cleaned_data['description'],
                status=form.cleaned_data['status'],
                type=form.cleaned_data['type']
            )
            return redirect('issue_view', pk=issue.pk)
        return render(request, 'issue_create.html', {'form': form})


class IssueUpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        self.issue = get_object_or_404(Issue, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,  *args, **kwargs):
        form = IssueForm(initial={
            'summary':self.issue.summary,
            'description':self.issue.description,
            'status': self.issue.status,
            'type': self.issue.type
        })
        return render(request, 'issue_update.html', {'form': form})
    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            self.issue.summary = form.cleaned_data.get('summary')
            self.issue.description = form.cleaned_data.get('description')
            self.issue.status = form.cleaned_data.get('status')
            self.issue.type = form.cleaned_data.get('type')
            self.issue.save()
            return redirect('issue_view', pk=self.issue.pk)
        return render(request, 'issue_update.html', {'form': form})

class IssueDeleteView(TemplateView):
    template_name = 'issue_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issue = get_object_or_404(Issue, pk=self.kwargs.get('pk'))
        context['issue'] = issue
        return context

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=self.kwargs.get('pk'))
        issue.delete()
        return redirect('index')

