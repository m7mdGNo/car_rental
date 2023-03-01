from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from users.models import Company



@method_decorator(login_required(login_url='company_login'), name='dispatch')
class CompanyRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated) and Company.objects.filter(user=request.user).exists():
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)