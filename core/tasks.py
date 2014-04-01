from __future__ import absolute_import

from celery import shared_task, task


@shared_task
def add(x, y):
    return x + y

import boto
import logging
import logging
logging.basicConfig()

from boto.elastictranscoder.exceptions import (
    InternalServiceException,
    LimitExceededException,
    ResourceInUseException,
)
from django.conf import settings
from core.models import Media


# TODO(paul): These IDs may or may not be stable across API versions
ELASTIC_TRANSCODER_PRESET_WEB = '1351620000001-100070'

logger = logging.getLogger(__name__)


def get_pipeline_id(et_conn, name):
    """Get the Elastic Transcoder pipeline ID for a named pipeline.

    If a given name has no matching pipeline, we return None.
    """
    result = et_conn.list_pipelines()
    ids = [pl['Id'] for pl in result['Pipelines'] if pl['Name'] == name]
    if ids:
        return ids[0]
    else:
        return None


@task(serializer='json', ignore_result=True)
def convert_media_elastic(media_id, pipeline_name, update_media=True):
    """Pass media to Elastic Transcoder.

    args:
        media_id: Media object to transcode
        update_media: if False, no changes will be made to the Media object
    """
    try:
        media = Media.objects.get(id=media_id)
    except Media.DoesNotExist, exc:
        logger.error("Media ID %s not found!", media_id, exc_info=exc)
        raiseu

    # No point in starting another transcode for the same media
    if media.status in ('I', 'Q'):
        logger.warning("Transcode in progress, %s, job in progress.",
                       media_id)
        return

    '''
    # Ensure we have the original key saved
    if update_media:
        media.update(set__original_s3_key=media.s3_key)
    '''

    try:
        transcoder = boto.connect_elastictranscoder(
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY,
        )
    except boto.exception.BotoServerError, exc:
        logger.error("Unable to connect to Elastic Transcoder!", exc_info=exc)
        if update_media:
            media.status = 'E'
            media.save()
        raise

    # Get the Pipeline ID for the named pipeline
    pipeline_id = get_pipeline_id(transcoder, pipeline_name)
    if not pipeline_id:
        raise KeyError("Elastic Transcoder pipeline %s not found!",
                       pipeline_name)

    input_name = {
        'Key': media.get_original_s3_key(),
        'FrameRate': 'auto',
        'Resolution': 'auto',
        'AspectRatio': 'auto',
        'Interlaced': 'auto',
        'Container': 'auto', }

    # Take the last path component, and use everything up to the first "."
    base_file_name = media.get_original_s3_key().split('/')[-1].split('.')[0]

    outputs = [{
        'Key': 'web/{}.m4a'.format(base_file_name),
        'ThumbnailPattern': '',
        'Rotate': 'auto',
        'PresetId': ELASTIC_TRANSCODER_PRESET_WEB,
        'Watermarks': [], }]

    if update_media:
        media.status = 'Q'
        media.save()

    try:
        resp = transcoder.create_job(
            output_key_prefix='media/et/{}/'.format(media_id),
            pipeline_id=settings.DD_ELASTIC_TRANSCODER_PIPELINE_ID,
            input_name=input_name,
            outputs=outputs
        )

        job = resp['Job']

    # Retry when we encounter transient failures
    except (InternalServiceException, LimitExceededException,
            ResourceInUseException), exc:
        logger.warning("Could not start elastic transcoder job, retrying...",
                       exc_info=exc)
        raise convert_media_elastic.retry(exc=exc)
    except boto.exception.JSONResponseError, exc:
        logger.error("Could not start elastic transcoder job", exc_info=exc)
        if update_media:
            media.status = 'E'
            media.save()
        raise

    poll_elastic_transcoder.apply_async(media_id, job['Id'], update_media)
    logger.warning("Polling in progress, %s, job in progress.",
                       media_id)

    return job['Id']


@task(serializer='json', ignore_result=True)
def poll_elastic_transcoder(media_id, job_id, update_media=True):
    """Watch an ET job and update the media status when it's done.

    args:
        media_id: Media object we're updating
        job_id: ET job ID to monitor
        update_media: if False, no changes will be made to the Media object
    """
    media = Media.objects.get(id=media_id)

    try:
        transcoder = boto.connect_elastictranscoder(
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY,
        )
    except boto.exception.BotoServerError, exc:
        logger.error("Unable to connect to Elastic Transcoder!", exc_info=exc)
        if update_media:
            media.status = 'E'
            media.save()
        raise

    job = transcoder.read_job(job_id)['Job']

    # outputs[0] is fine until we refactor Media for multiple targets
    output = job['Outputs'][0]

    if output['Status'] in ('Submitted', 'Progressing'):
        if media.status != 'I':
            if update_media:
                media.status = 'I'
                media.save()

        raise poll_elastic_transcoder.retry(countdown=60)
    elif job['Status'] == 'Complete':
        if update_media:
            set_internal_file_s3_key=job['OutputPrefix'] + output['Key']
            media.set_complete()
    else:
        logger.error('Transcode failed on media ID %s, job ID %s, details: %s',
                     media_id, job_id, output['StatusDetail'])
        if update_media:
            media.status = 'E'
            media.save()

    return
