from typing import Dict


def update_engine_info(table_name, where_dict: Dict, set_dict: Dict):
    set_sql = dict_to_sql(set_dict, middle_key=',')
    where_sql = dict_to_sql(where_dict, middle_key='AND')

    where_list = []
    for key, val in where_dict.items():
        where_list.append(f"{key} = '{val}'")
    update_sql = f"UPDATE {table_name} " \
                 f"SET {set_sql} " \
                 f"WHERE {where_sql}"
    return update_sql


def dict_to_sql(input_dict: Dict, middle_key):
    """
    dict안의 아이템들을 sql형태로 변환
    :param middle_key: 각 item사이에 들어갈 단어 - where==and, set==,
    :param input_dict:
    :return:
    """
    result_list = []
    for key, val in input_dict.items():
        if type(val) is int or type(val) is float:
            result_list.append(f"{key} = {val}")
        else:
            result_list.append(f"{key} = '{val}'")
    result_sql = f' {middle_key} '.join(result_list)
    return result_sql
