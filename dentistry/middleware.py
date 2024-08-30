from django.shortcuts import render, redirect
from dentistry.forms import FeedbackForm


class FeedbackFormMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and 'feedback-form' in request.POST:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                form.save()

            else:
                request.feedback_form = form
        else:
            request.feedback_form = FeedbackForm()

        response = self.get_response(request)
        return response
