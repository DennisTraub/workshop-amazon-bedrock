import boto3

def try_initialize_session(region=None):
    try:
        session = boto3.Session(region_name=region) if region else boto3.Session()
        sts = session.client('sts')
        sts.get_caller_identity()
        return session, None
    except Exception as error:
        return None, error
