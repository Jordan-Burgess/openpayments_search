from django.http import JsonResponse
from django.shortcuts import render
from .documents import PaymentDocument

def search_page(request):
    return render(request, 'search.html')

def api_search(request):
    query = request.GET.get('q', '')
    if query:
        search = PaymentDocument.search().query('multi_match', query=query, fields=['doctor_first_name', 'doctor_last_name'], type='phrase_prefix')
        response = search.execute()
        results = [hit.to_dict() for hit in response.hits]
        return JsonResponse(results, safe=False)
    return JsonResponse({'message': 'No Query'})