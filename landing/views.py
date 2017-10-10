from django.shortcuts import render
from navProved.models import *
from django.shortcuts import redirect

# Create your views here.
def landing(request):
	if request.method == 'POST':
		ticker_name = request.POST.get('ticker')
		tickers = Ticker.objects.filter(name__icontains = ticker_name).all()
		if not tickers:
			error = 'There is no Ticker you wanna get.'
			return render(request, 'landing.html', {'error' : error})
		for element in tickers:
			ticker = element
		request.session['ticker_id'] = ticker.id
		request.session['play_id'] = 1
		return redirect('navTotal')

	return render(request, 'landing.html')