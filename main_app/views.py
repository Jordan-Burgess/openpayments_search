from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .documents import PaymentDocument
import pandas as pd

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

def export_to_excel(request):
    query = request.GET.get('q', '')
    if query:
        search = PaymentDocument.search().query('multi_match', query=query, fields=['doctor_first_name', 'doctor_last_name'], type='phrase_prefix')
        response = search.execute()
        results = [hit.to_dict() for hit in response.hits]

        df = pd.DataFrame(results)

        response_obj = HttpResponse(
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        response_obj['Content-Disposition'] = 'attachment; filename="openpayments-search-results.xlsx"'

        with pd.ExcelWriter(response_obj, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        return response_obj
        
