from logzero import logger
from pandas import DataFrame, Series
from validation_decorators import ValidateArgType
from validation_decorators.errors import raise_error
from datetime import datetime
from curia.session import Session
import tempfile

type_validator = ValidateArgType(raise_error, logger=logger)


class Dataset():
    """Create a Curia dataset"""

    @type_validator(session=Session, name=str)
    def __init__(
            self,
            session,
            name: str,
            description: str = None,
            project_id: str = None,
            environment_id: str = None,
    ):

        self.session = session
        self.model_id = None
        self.model_type = 'risk'
        self.name = name

        super().__init__(
            session=self.session,
            name=name,
            description=description,
            project_id=project_id,
            environment_id=environment_id,
            model_type=self.model_type,
        )

    @type_validator(dataset=DataFrame)
    def upload(self, dataset: DataFrame):
        """

        Parameters
        ----------
        features: DataFrame :
            
        label: Series :
            

        Returns
        -------

        """

        df = features.copy()
        df['label'] = label

        self.set_job_type('train')

        self.model_dataset_upload(df)

        self.start()

        # TODO - how to handle wait=True param (check status every n seconds)

    @type_validator(features=DataFrame)
    def predict(self, features: DataFrame):
        """

        Parameters
        ----------
        features: DataFrame :
            

        Returns
        -------

        """

        df = features.copy()

        self.set_job_type('predict')

        self.model_dataset_upload(df)

        self.start()

        # TODO - how to handle wait=True param (check status every n seconds)

    @type_validator(data=DataFrame, name=str)
    def dataset_upload(self, data: DataFrame, name: str):
        """

        Parameters
        ----------
        data: DataFrame :


        Returns
        -------

        """

        self.session.logger.info('uploading DataFrame with shape %s',
                                 data.shape)

        dataset = self.session.api_instance.create_one_base_dataset_controller_dataset(
            self.session.api_client.Dataset(
                name=f'{self.name}',
                description='BYOD train dataset uploaded via curia-python-sdk',
                type=self._job_type,
                file_size=int(data.memory_usage(index=False).sum()),
                dataset_results={}
            )
        )

        self.session.logger.info('dataset data: %s', dataset)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            data.to_csv(temp, chunksize=1000)
        self.session.api_instance.dataset_controller_upload(
            temp.name,
            dataset.id
        )
        self.session.logger.info('upload successful')
        return dataset