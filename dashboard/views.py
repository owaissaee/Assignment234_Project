from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from applications.models import JobApplication
from resume_builder.models import Resume
from jobs.models import Job
from django.utils import timezone

@login_required(login_url='/accounts/login/')
def dashboard(request):
    user = request.user
    recent_applications = JobApplication.objects.filter(applicant=user).order_by('-applied_date')[:5]
    recent_resumes = Resume.objects.filter(user=user).order_by('-last_modified')[:5]

    recent_activities = []

    for app in recent_applications:
        recent_activities.append({
            'time': app.applied_date.strftime('%b %d'),
            'type': 'success',
            'content': f'You applied for {app.job.title}'
        })

    for resume in recent_resumes:
        recent_activities.append({
            'time': resume.last_modified.strftime('%b %d'),
            'type': 'info',
            'content': f'You updated resume: {resume.title}'
        })

    recent_activities.sort(key=lambda x: x['time'], reverse=True)

    context = {
        'total_resumes': Resume.objects.filter(user=user).count(),
        'total_applications': JobApplication.objects.filter(applicant=user).count(),
        'total_jobs': Job.objects.count(),
        'recent_applications': recent_applications,
        'recent_resumes': recent_resumes,
        'recent_activities': recent_activities,
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='/accounts/login/')
def settings_view(request):
    return render(request, 'dashboard/settings.html')

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('settings')

    return render(request, 'dashboard/edit_profile.html', {'user': user})
