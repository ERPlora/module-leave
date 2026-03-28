"""Scheduled task handlers for leave module."""
import logging
logger = logging.getLogger(__name__)

def reset_annual_quotas(payload):
    """Reset annual leave balances at start of fiscal year."""
    logger.info('leave.reset_annual_quotas called')
    return {'status': 'not_implemented'}
