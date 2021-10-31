import pymssql
from collections import OrderedDict

###装饰器，用于装饰各种查询
def select_operator(operator_func):
    def select_execute(self, table_name, field_name, dict_condition=None, log_str='and'):
        try:
            self.cur = self.get_cur()
            # field_name = ['count(1)']
            sql_str = self.get_select_str(table_name, field_name, dict_condition, log_str)
            dict_condition = OrderedDict(dict_condition)
            if dict_condition != None and isinstance(dict_condition, dict):
                list_condition_value = []
                for value in dict_condition.values():
                    if isinstance(value, list):
                        list_condition_value += value
                    # elif isinstance(value, str):
                    else:
                        list_condition_value.append(value)
                self.cur.execute(sql_str, tuple(list_condition_value))
            elif dict_condition == None:
                self.cur.execute(sql_str)

            return operator_func(self, table_name, field_name, dict_condition=None, log_str='and')

        except Exception as e:
            print(e)

    return select_execute


class Mssql_Utils:

    def __init__(self, host, user, password, database):
        Mssql_Utils.create_connection(host, user, password, database)

    def __del__(self):
        Mssql_Utils.close_connection()

    @staticmethod
    def create_connection(host, user, password, database):
        try:
            Mssql_Utils.conn = pymssql.connect(host, user, password, database)
        except Exception as e:
            print(e)

    @staticmethod
    def close_connection():
        try:
            Mssql_Utils.conn.close()
        except Exception as e:
            print(e)

    def get_conn(self):
        return Mssql_Utils.conn

    def get_cur(self):
        return Mssql_Utils.conn.cursor()

    '''
        方法：get_select_str
        功能：组装sql语句字符串
        参数：
            table_name：表名
            list_field_name：要查的字段名，以列表形式传入
            codition：where条件，以字典形式传入
            log_str：where多条件逻辑（本方法只针对where条件同为and或同为or时使用）
        返回：SQL查询字符串
    '''

    def get_select_str(self, table_name, list_field_name, dict_condition=None, log_str='and'):
        return_str = 'select ' + ",".join(list_field_name) + ' from ' + table_name
        # dict_condition = OrderedDict(dict_condition)
        if dict_condition != None and isinstance(dict_condition, dict):
            # list_codition_key = [key for key in dict_condition.keys()]
            list_condition_key = []
            for key in dict_condition.keys():
                if isinstance(dict_condition[key], list):
                    for value in (dict_condition[key]):
                        list_condition_key.append(key)
                # elif isinstance(dict_condition[key], str):
                else:
                    list_condition_key.append(key)
            if log_str == 'and':
                return_str = return_str + ' where ' + '=%s  and '.join(list_condition_key) + '=%s'
            elif log_str == 'or':
                return_str = return_str + ' where ' + '=%s  or '.join(list_condition_key) + '=%s'
            print(return_str)
        return return_str

    '''
    方法：__get_insert_str
    参数:
        table_name 表名
        list_values 要插入表的记录列表
    返回：
        插入表SQL字符串
    '''

    def __get_insert_str(self, table_name, list_values):
        li = []
        for i in list_values:
            li.append('%s')
        sql_str = 'insert into %s values(%s)' % (str(table_name), ','.join(li))
        return sql_str

    def __get_update_str(self, table_name, dict_new_value, dict_condition, log_str='and'):
        sql_str = 'update %s set ' % (table_name)
        # dict_new_value = OrderedDict(dict_new_value)
        # dict_condition = OrderedDict(dict_condition)

        if dict_new_value != None and isinstance(dict_new_value, dict):
            list_new_field_and_value_str = []
            for key in dict_new_value:
                if isinstance(key, str):
                    list_new_field_and_value_str.append(str(key) + '=\'' + str(dict_new_value[key]) + '\'')
                else:
                    list_new_field_and_value_str.append(str(key) + '=' + str(dict_new_value[key]))
            sql_str += ','.join(list_new_field_and_value_str)

        if dict_condition != None and isinstance(dict_condition, dict):
            list_condition_key = []
            for key in dict_condition.keys():
                if isinstance(dict_condition[key], list):
                    for value in (dict_condition[key]):
                        list_condition_key.append(key)
                # elif isinstance(dict_condition[key], str):
                else:
                    list_condition_key.append(key)
            if log_str == 'and':
                sql_str = sql_str + ' where ' + '=%s  and '.join(list_condition_key) + '=%s'
            elif log_str == 'or':
                sql_str = sql_str + ' where ' + '=%s  or '.join(list_condition_key) + '=%s'

        return sql_str

    '''
    方法：exist_content
    功能：判断在table_name中满足dict_condition条件的记录是否存在
    参数:
        table_name 表名
        list_field_name 在这必须填['count(1)']
        dict_condition where条件 以字典类型传入
        dict_condition 如果条件名有重复，请将值用列表传入
            例如：{考号：['535022502209', '435022502615']}
    返回：如果dict_condition=None或者一条记录都没有，返回None
         否则返回记录数
    '''

    @select_operator
    def exist_content(self, table_name, list_field_name=['count(1)'], dict_condition=None, log_str='and'):
        count = self.cur.fetchone()[0]
        if count > 0:
            return count
        else:
            return None

    '''
    方法：fetch_all_from_table
    功能：返回在table_name中满足dict_condition条件的list_field_name
    参数:
        table_name 表名
        list_field_name 要显示的字段名
        dict_condition where条件 以字典类型传入
        dict_condition 如果条件名有重复，请将值用列表传入
            例如：{考号：['535022502209', '435022502615']}
    返回：在满足dict_condition条件的字段记录
    '''

    @select_operator
    def fetch_all_from_table(self, table_name, list_field_name, dict_condition=None, log_str='and'):
        return self.cur.fetchall()

    '''
    方法：insert_to_table
    功能：插入一条或多条记录到指定表中
    参数：
        table_name 表名
        list_values 数据列表名（注意：每条记录必须是元组，整个列表为多个元组组成的列表）
    返回：如果执行成功，返回True;如果发生错误，返回False
    '''

    def insert_to_table(self, table_name, list_values):
        try:
            sql_str = self.__get_insert_str(table_name, list_values)
            self.cur = self.get_cur()
            self.cur.executemany(sql_str, list_values)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def update_to_table(self, table_name, dict_new_value, dict_condition):
        try:
            dict_new_value = OrderedDict(dict_new_value)
            dict_condition = OrderedDict(dict_condition)
            sql_str = self.__get_update_str(table_name, dict_new_value, dict_condition)
            self.cur = self.get_cur()
            print(sql_str)

            if dict_condition != None and isinstance(dict_condition, dict):
                list_condition_value = []
                for value in dict_condition.values():
                    if isinstance(value, list):
                        list_condition_value += value
                    # elif isinstance(value, str):
                    else:
                        list_condition_value.append(value)
                        print(list_condition_value)
                self.cur.execute(sql_str, tuple(list_condition_value))
            elif dict_condition == None:
                self.cur.execute(sql_str)

            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    test = Mssql_Utils('192.168.5.130:1433', 'sa', 'Xmksxmks.jb666', 'temp')
    # print(test.exist_content('total', {'姓名': '安妮', '考号': '535022502209'}))
    # print(test.opeerator(exist_content(Mssql_Utils(),'total', {'姓名': '安妮', '考号': '535022502209'}))
    # print(test.exist_content('total', ['count(1)'], {'姓名': '安妮'}))
    # print(test.fetch_all_from_table('total',['姓名','考号'], {'考号': ['535022502209','435022502615']}, 'or'))
    # test.insert_to_table('test', [('aaa', 123), ('bbb', 456)])
    test.update_to_table('test',{'test2':789},{'test1':'dcc'})
