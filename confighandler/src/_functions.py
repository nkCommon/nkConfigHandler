"""Database configuration and connection utilities for PostgreSQL."""

from configparser import ConfigParser
from typing import Any, LiteralString
from datetime import datetime
from pydantic import BaseModel, model_validator, Field, ConfigDict, StrictBool
import psycopg
import psycopg.sql as sql
from psycopg.rows import dict_row, DictRow
from ._models import Row


def load_config(
    filename: str = "database.ini", section: str = "postgresql"
) -> dict[str, Any]:
    """
    Purpose
    Used for loading configuration

    **Args:**
        **filename** (*str*): File containing connection values such as databaseserver, database, user and password
                            default database.ini
        **section** (*str*): Section name of ini file
                            default is postgresgl

    **Returns:**
        **config** (*dict*): Configuration dictionary

    **Raises:**
        **Exception**: Exception
    """
    try:
        parser = ConfigParser()
        parser.read(filename)
    except FileNotFoundError as e:
        raise e

    # get section, default to postgresql
    config = {}
    try:
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
            return config
        else:
            raise RuntimeError(f"Section {section} not found in the {filename} file")
    except Exception as exc:
        raise RuntimeError(
            f"Section {section} not found in the {filename} file"
        ) from exc


def connect(config: dict):
    """
    Purpose:
    Connect to the PostgreSQL database server

    **Args:**
        **config** (*dict*): Configuration dictionary

    **Returns:**
        **conn** (*psycopg.Connection*): Database connection

    **Raises:**
        **error** (*psycopg.DatabaseError*): Database error
    """
    try:
        # connecting to the PostgreSQL server
        conn = psycopg.connect(**config)
        return conn
    except (psycopg.DatabaseError, Exception) as error:
        raise error


def execute_query(
    conn: psycopg.Connection, query: LiteralString, params: dict | None = None
):
    """
    Execute a single query

    **Args:**
        **conn** (*psycopg.Connection*): Database connection
        **query** (*str*): Query to execute
        **params** (*dict|None*): Parameters to pass to the query

    """
    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()


def fetch_query(
    conn: psycopg.Connection, query: LiteralString, params: dict | None = None
):
    """Execute a query and fetch results

    **Args:**
        **conn** (*psycopg.Connection*): Database connection
        **query** (*str*): Query to execute
        **params** (*dict|None*): Parameters to pass to the query
    """
    with conn.cursor() as cur:
        cur.execute(query, params)
        result = cur.fetchall()
        return result


def select_with_conditions(
    conn: psycopg.Connection,
    schema_name: str,
    table_name: str,
    where_conditions: dict | None = None,
):
    """
    Select rows from a table with dynamic WHERE conditions.

    **Args:**
        **conn** (*psycopg.Connection*): The database connection object.
        **schema_name** (*str*): The schema name of the table.
        **table_name** (*str*): The name of the table to query.
        **where_conditions** (*dict*): A dictionary of columns and their values to filter by.

    **Returns:**
        **list** (*list*): A list of dictionaries representing the rows that match the conditions.
    """
    try:
        with conn.cursor(row_factory=dict_row) as cursor:
            # Start building the query
            query = sql.SQL("SELECT * FROM {schema}.{table}").format(
                schema=sql.Identifier(schema_name), table=sql.Identifier(table_name)
            )

            # If there are conditions, build the WHERE clause
            if where_conditions:
                conditions = [
                    sql.SQL("{} = %s").format(sql.Identifier(k))
                    for k in where_conditions.keys()
                ]

                query = query + sql.SQL(" WHERE ") + sql.SQL(" AND ").join(conditions)

                # Execute the query
                cursor.execute(query, list(where_conditions.values()))
            else:
                cursor.execute(query)

            # Fetch all the rows
            rows = cursor.fetchall()
            return rows

    except Exception as error:
        raise error


class Parameter:
    """
    Purpose:
    Class for holding paremeter
    Contains:
    parameter -> (str) name of parameter
    value -> (any) value of parameter
    """

    def __init__(self, name: str, value: Any):
        self.parameter = name
        self.value = value


def get_initial_values(appname: str = "", debugging: bool = False):
    """
    Purpose:
    Get constants for application

    Argument:
    appname -->  name of application (id in table row)

    returns a list of class values containing name and value of contsnats/parameters
    """

    if appname is not None and len(appname) > 0:
        config = load_config()
        connection = connect(config)
        if connection:
            parameters = []
            #   Select the values from the database
            where_conditions = {"id": appname, "debugmode": debugging}
            results = select_with_conditions(
                connection, "public", "nkinitvalues", where_conditions
            )
            for result in results:
                parameter = get_parameter(result)
                if parameter:
                    parameters.append(parameter)
            return parameters
    return None


def get_unique_app_names(ini_file: str = "database.ini") -> set[str]:
    """
    Get all unique app names from the database

    Returns:
        set[str]: A set of all unique app names
    """
    config = load_config(filename=ini_file)
    connection = connect(config)
    if connection:
        #   Select the values from the database
        results = select_with_conditions(connection, "public", "nkinitvalues")
        return set([result["id"] for result in results])
    else:
        raise ConnectionError("Failed to connect to the database")


def get_parameter(row: DictRow) -> Parameter:
    """
    Purpose extract class Parameter from database row

    **Args:**
        **row** (*DictRow*): Database record

    **Returns:**
        **parameter** (*Parameter*): Parameter object
    """
    if not row:
        raise RuntimeError("No row supplied")

    try:
        # Create Pydantic model with automatic type conversion
        row_model = Row.model_validate(dict(row))
        return Parameter(name=row_model.name, value=row_model.value)
    except Exception as e:
        raise e


def get_config(
    appname: str = "", debugging: bool = False, ini_file: str = "database.ini"
) -> dict:
    """
    Purpose:
    Get constants for application

    Argument:
    appname -->  name of application (id in table row)
    debugging --> indicates whether values fetched are for production or debugging.   Default is False

    returns a list of class values containing name and value of contsnats/parameters
    """

    if appname is not None and len(appname) > 0:
        # print(f'looking up valujes for {appname}')
        constants = {}
        config = load_config(filename=ini_file)
        connection = connect(config)
        if connection:
            # print(f'connection established')
            #   Select the values from the database
            where_conditions = {"id": appname, "debugmode": debugging}
            rows = select_with_conditions(
                connection, "public", "nkinitvalues", where_conditions
            )
            for row in rows:
                constants[row["name"]] = get_parameter_value(row)
            return constants
    return {}


def get_parameter_value(
    row: dict,
) -> str | int | float | bool | list[str] | list[int] | list[float] | datetime | None:
    """
    Purpose extract typed value from database row

    Args:
        row (DictRow | dict): Database record or dictionary with same structure

    Returns:
        The typed value based on type_id
    """
    if not row:
        return None

    try:
        # Handle both DictRow and dict types
        row_data = dict(row)
        row_model = Row(row=row_data)
        return row_model.value
    except Exception as e:
        raise RuntimeError(f"Value conversion failed: {e}") from e


class ConfigurationModel(BaseModel):  # TODO: to be transferred to "_models"
    """
    Evaluating input values to the Configuration-class
    """

    model_config = ConfigDict(extra="allow")
    appname: str = Field(min_length=5)
    debugging: StrictBool = False
    ini_file: str = Field(default="database.ini")

    @model_validator(mode="after")
    def app_name_must_be_known(self):
        """
        Validating if the app_name is a valid unique app_name
        """
        # Check minimum length first
        if len(self.appname) < 5:
            raise ValueError("app_name is too short (min 5 chars).")
        allowed: set[str] = get_unique_app_names(self.ini_file)
        if self.appname not in allowed:
            raise ValueError(
                f"Invalid app_name '{self.appname}'. Must be one of: {sorted(allowed)}"
            )
        return self
