import logging
import mysql.connector


class MySQLManager:
    logger = logging.getLogger("MySQLManager")

    def __init__(self, **kwargs):
        self.database = kwargs['database']
        self.db_conn = None
        self.cursor = None

        self.__create_connection(kwargs)
        self.__set_cursor()

    @property
    def connection(self):
        return self.db_conn

    def __create_connection(self, kwargs):
        """ create a database connection to the MySQL database
        :return: Connection object or None
        """

        try:
            self.db_conn = mysql.connector.connect(**kwargs)
            self.logger.info("Connection created!")
        except mysql.connector.Error as e:
            self.logger.error(f"Connection not created: {e}")
            quit()

    def __set_cursor(self):
        self.cursor = self.db_conn.cursor(buffered=True, dictionary=True)

    def execCommand(self, sql, parameters=None, msg=None, msg_fail=None, commit=False):
        if parameters is None:
            parameters = {}
        try:
            self.cursor.execute(sql, parameters)
            if commit:
                self.db_conn.commit()
            if msg is not None:
                self.logger.info(msg)
        except mysql.connector.Error as e:
            if msg_fail is not None:
                self.logger.error(f"{msg_fail}: {e}")
            else:
                self.logger.error(f"Command not executed: {e}")
            quit()

    def close_connection(self):
        """ close a database connection to the MySQL database in self.path
        :return:
        """
        try:
            self.db_conn.close()
            self.logger.info("Connection closed!")
        except mysql.connector.Error as e:
            self.logger.error(f"Connection can't be closed: {e}")

    def select_all_rows(self, table):
        """
        Query all rows in the table
        :return: all rows
        """
        self.execCommand(sql=f"SELECT * FROM {table}",
                         msg_fail=f"Can't select rows from {table}")
        rows = self.cursor.fetchall()
        self.logger.info(f"Selected {len(rows)} rows from {table}")

        return rows

    def commit(self):
        self.db_conn.commit()