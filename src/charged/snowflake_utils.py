import os
from snowflake.snowpark import Session


def create_session():
    """ "Create Snowflake session."""
    # create snowpark session
    params = {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "role": os.environ["SNOWFLAKE_ROLE"],
        "database": os.environ["SNOWFLAKE_DATABASE"],
        "schema": os.environ["SNOWFLAKE_SCHEMA"],
        "warehouse": os.environ["SNOWFLAKE_WAREHOUSE"],
        "user": os.environ["SNOWFLAKE_USER"],
        "password": os.environ["SNOWFLAKE_PASSWORD"],
        "authentication": "snowflake",
        "session_parameters": {
            "QUERY_TAG": "hack4rail",
        },
    }
    return Session.builder.configs(params).create()
