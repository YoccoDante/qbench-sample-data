import logging
from app.repositories.data_repository import DataRepository
from app.utils.response_builder import ResponseBuilder

logger = logging.getLogger(__name__)


def get_sample_data_by_id(sample_id: int):
    try:
        logger.info(f"Getting data from sample_id: {sample_id}")
        sample_data = DataRepository.get_sample_data_by_id(sample_id)
        
        if not sample_data:
            logger.warning(f"No sample data for id: {sample_id}")
            return ResponseBuilder.fail(message=f"No sample data for id: {sample_id}")
        
        logger.info(f"Data obtained successfully for sample_id: {sample_id}")
        return ResponseBuilder.success(data=sample_data)
    except Exception:
        logger.error(f"Something went wrong while fetching data for sample_id: {sample_id}")
        return ResponseBuilder.error(
            message=f"Something went wrong while fetching data for sample_id: {sample_id}"
        )
        