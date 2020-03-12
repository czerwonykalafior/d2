from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponse, StreamingHttpResponse
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
import pandas as pd
from io import StringIO

from sql_builder import build_sql


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def get_data(request):
    table_name = request.query_params['table_name']
    columns = request.query_params.get('columns', '').split(',')
    filters = {k: v for k, v in request.query_params.items() if k not in ['limit', 'offset', 'sortBy']}
    order_by = request.query_params.get('sortBy', '').split(',')
    limit = request.query_params.get('limit', None)
    offset = request.query_params.get('offset', 0)

    sql = build_sql(table_name, columns, filters, order_by, limit, offset)
    print(sql)

    data = pd.read_sql(sql, connection)
    j = data.to_json(orient='split')

    return HttpResponse(j)


def db_paginator(query, sample_size):
    limit = 1000
    offset = 0
    is_header_sent = False
    while offset <= sample_size:
        sql = f"{query} LIMIT {limit} OFFSET {offset}"
        print(sql)
        data = pd.read_sql(sql, connection)
        if data.empty:
            break
        offset += limit

        is_last_iteration = (offset > sample_size)
        if is_last_iteration:
            s = sample_size % limit
            data = data[:s]

        if not is_header_sent:
            is_header_sent = True
            yield data.to_csv(header=True)
        else:
            yield data.to_csv(header=False)


@api_view(['GET'])
def some_streaming_csv_view(request):
    """A view that streams a large CSV file.
    65536 the range is based on the maximum number of rows that
    can be handled by a single sheet in most spreadsheet applications. """
    table_name = request.query_params['table_name']
    sample_size = int(request.query_params.get('sample_size', 65536))
    query = f"SELECT * FROM {table_name}"
    response = StreamingHttpResponse(db_paginator(query, sample_size),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    return response
