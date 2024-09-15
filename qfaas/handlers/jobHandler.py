from fastapi.encoders import jsonable_encoder
from datetime import datetime

from fastapi.encoders import jsonable_encoder

from qfaas.database.dbJob import (
    add_job,
)
from qfaas.models.job import (
    JobSchema,
)
from qfaas.utils.logger import logger


async def create_job(providerJobId, provider, backend, owner, function, jobRequest, result):
    logger.info("Creating job...")
    job = JobSchema(
        providerJobId=providerJobId,
        provider=provider,
        backend=backend,
        status="CREATED",
        lastUpdated=datetime.now(),
        owner=owner,
        function=function,
        submitTime=datetime.now(),
        jobRequest=jobRequest,
        result=result,
        jobInfo={},
    )
    job = jsonable_encoder(job)
    new_job = await add_job(job)
    logger.info("New job created successfully!")
    return new_job
