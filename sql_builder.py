from typing import Optional


def build_sql(table_name: str,
              filters: Optional[dict] = None,
              columns: Optional[list] = None,
              order_by: Optional[list] = None,
              limit: Optional[int] = None,
              offset: int = 0):
    columns = ", ".join(columns) if columns else '*'
    filters_sql = ' '.join([f'AND {col_name}="{value}"' for col_name, value in filters.items()]) if filters else ''
    order_by_sql = f'order by {", ".join(order_by)}' if order_by is not None else ''
    limit_offset_sql = f' LIMIT {limit} OFFSET {offset}' if limit else ''

    sql = f"SELECT {columns} FROM {table_name} where 1=1 {filters_sql} {order_by_sql} {limit_offset_sql}"
    print(sql)
    return sql


if __name__ == '__main__':
    # build_sql(
    #     table_name='sales_data',
    #     columns=['Region', 'Country'],
    #     filters={'Region': 'Asia'},
    #     order_by=['Country'],
    #     limit=10,
    #     offset=0
    # )

    build_sql(
        table_name='sales_data'
    )
