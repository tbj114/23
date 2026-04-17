import numpy as np
import pandas as pd
import os


class DataManagement:
    @staticmethod
    def import_data(file_path, file_type=None):
        """
        导入数据
        
        参数:
        file_path: str - 文件路径
        file_type: str - 文件类型 ('csv', 'excel', 'json', 'txt')
        
        返回:
        DataFrame - 导入的数据
        """
        try:
            if file_type is None:
                # 根据文件扩展名自动判断
                ext = os.path.splitext(file_path)[1].lower()
                if ext == '.csv':
                    file_type = 'csv'
                elif ext in ['.xlsx', '.xls']:
                    file_type = 'excel'
                elif ext == '.json':
                    file_type = 'json'
                elif ext == '.txt':
                    file_type = 'txt'
                else:
                    return {'error': 'Unknown file type'}
            
            if file_type == 'csv':
                data = pd.read_csv(file_path)
            elif file_type == 'excel':
                data = pd.read_excel(file_path)
            elif file_type == 'json':
                data = pd.read_json(file_path)
            elif file_type == 'txt':
                data = pd.read_csv(file_path, delimiter='\t')
            else:
                return {'error': 'Unsupported file type'}
            
            return data
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def export_data(data, file_path, file_type=None):
        """
        导出数据
        
        参数:
        data: DataFrame - 要导出的数据
        file_path: str - 文件路径
        file_type: str - 文件类型 ('csv', 'excel', 'json', 'txt')
        
        返回:
        dict - 导出结果
        """
        try:
            if file_type is None:
                # 根据文件扩展名自动判断
                ext = os.path.splitext(file_path)[1].lower()
                if ext == '.csv':
                    file_type = 'csv'
                elif ext in ['.xlsx', '.xls']:
                    file_type = 'excel'
                elif ext == '.json':
                    file_type = 'json'
                elif ext == '.txt':
                    file_type = 'txt'
                else:
                    return {'error': 'Unknown file type'}
            
            if file_type == 'csv':
                data.to_csv(file_path, index=False)
            elif file_type == 'excel':
                data.to_excel(file_path, index=False)
            elif file_type == 'json':
                data.to_json(file_path, orient='records')
            elif file_type == 'txt':
                data.to_csv(file_path, sep='\t', index=False)
            else:
                return {'error': 'Unsupported file type'}
            
            return {'success': True, 'message': f'Data exported successfully to {file_path}'}
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def clean_data(data, remove_duplicates=True, drop_na=False, na_threshold=0.5):
        """
        数据清洗
        
        参数:
        data: DataFrame - 输入数据
        remove_duplicates: bool - 是否移除重复行
        drop_na: bool - 是否删除含有缺失值的行
        na_threshold: float - 缺失值阈值，超过此比例的列将被删除
        
        返回:
        DataFrame - 清洗后的数据
        """
        try:
            cleaned_data = data.copy()
            
            # 移除重复行
            if remove_duplicates:
                cleaned_data = cleaned_data.drop_duplicates()
            
            # 删除缺失值比例过高的列
            if na_threshold > 0:
                na_ratio = cleaned_data.isna().mean()
                columns_to_drop = na_ratio[na_ratio > na_threshold].index
                cleaned_data = cleaned_data.drop(columns=columns_to_drop)
            
            # 删除含有缺失值的行
            if drop_na:
                cleaned_data = cleaned_data.dropna()
            
            return cleaned_data
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def handle_missing_values(data, method='mean', columns=None):
        """
        缺失值处理
        
        参数:
        data: DataFrame - 输入数据
        method: str - 处理方法 ('mean', 'median', 'mode', 'drop')
        columns: list - 要处理的列名列表
        
        返回:
        DataFrame - 处理后的数据
        """
        try:
            handled_data = data.copy()
            
            if columns is None:
                columns = handled_data.columns
            
            for col in columns:
                if handled_data[col].isna().any():
                    if method == 'mean':
                        handled_data[col] = handled_data[col].fillna(handled_data[col].mean())
                    elif method == 'median':
                        handled_data[col] = handled_data[col].fillna(handled_data[col].median())
                    elif method == 'mode':
                        handled_data[col] = handled_data[col].fillna(handled_data[col].mode()[0])
                    elif method == 'drop':
                        handled_data = handled_data.dropna(subset=[col])
                    else:
                        return {'error': 'Unknown method'}
            
            return handled_data
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def transform_data(data, transformations):
        """
        数据转换
        
        参数:
        data: DataFrame - 输入数据
        transformations: dict - 转换规则，格式为 {'column': {'method': '...', 'params': {...}}}
        
        返回:
        DataFrame - 转换后的数据
        """
        try:
            transformed_data = data.copy()
            
            for column, transformation in transformations.items():
                if column not in transformed_data.columns:
                    continue
                
                method = transformation.get('method')
                params = transformation.get('params', {})
                
                if method == 'log':
                    transformed_data[column] = np.log(transformed_data[column] + params.get('offset', 0))
                elif method == 'sqrt':
                    transformed_data[column] = np.sqrt(transformed_data[column])
                elif method == 'square':
                    transformed_data[column] = transformed_data[column] ** 2
                elif method == 'normalize':
                    mean = transformed_data[column].mean()
                    std = transformed_data[column].std()
                    transformed_data[column] = (transformed_data[column] - mean) / std
                elif method == 'min_max':
                    min_val = transformed_data[column].min()
                    max_val = transformed_data[column].max()
                    transformed_data[column] = (transformed_data[column] - min_val) / (max_val - min_val)
                elif method == 'one_hot':
                    dummies = pd.get_dummies(transformed_data[column], prefix=column)
                    transformed_data = pd.concat([transformed_data, dummies], axis=1)
                    transformed_data = transformed_data.drop(column, axis=1)
                elif method == 'label_encode':
                    from sklearn.preprocessing import LabelEncoder
                    le = LabelEncoder()
                    transformed_data[column] = le.fit_transform(transformed_data[column])
                else:
                    return {'error': f'Unknown transformation method: {method}'}
            
            return transformed_data
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def reshape_data(data, id_vars, value_vars, var_name, value_name):
        """
        数据重塑
        
        参数:
        data: DataFrame - 输入数据
        id_vars: list - 标识符变量
        value_vars: list - 值变量
        var_name: str - 变量名
        value_name: str - 值名
        
        返回:
        DataFrame - 重塑后的数据
        """
        try:
            reshaped_data = pd.melt(data, id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)
            return reshaped_data
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def aggregate_data(data, group_by, aggregations):
        """
        数据聚合
        
        参数:
        data: DataFrame - 输入数据
        group_by: list - 分组变量
        aggregations: dict - 聚合规则，格式为 {'column': 'aggregation_function'}
        
        返回:
        DataFrame - 聚合后的数据
        """
        try:
            aggregated_data = data.groupby(group_by).agg(aggregations).reset_index()
            return aggregated_data
        except Exception as e:
            return {'error': str(e)}
