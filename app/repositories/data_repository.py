from app.models.data import Data


class DataRepository:
    @staticmethod
    def get_sample_data_by_id(sample_id):
        """        
        :param sample_id: Integer representing the data to be fetched.
        :return: the sample data.
        """
        query = Data.query
        return query.filter(Data.id == sample_id).first()
