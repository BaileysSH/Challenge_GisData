
from MySQLManager import MySQLManager
import logging
from ReportGenerator import ReportGenerator

logger = logging.getLogger("Main")
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    logger.info("Start program")

    logger.info("Create connection...")
    database = MySQLManager(host="localhost", user="user", password="resu", database="batch")

    logger.info("Retrieve user data...")
    users = database.select_all_rows(table='utenti')
    users = {us['id']: {**us} for us in users}

    logger.info("Retrieve operations data...")
    operations = database.select_all_rows(table='operazioni')
    operations = {op['id']: {**op} for op in operations}

    for user_id, vals in users.items():
        first_dep = vals['primo_deposito']
        vals['operazioni'] = [vals for _, vals in operations.items() if vals['utente_id'] == user_id]

        final_delta = sum([operation['ammontare'] for operation in vals['operazioni']])

        # update and retrieve again the value
        database.execCommand(sql=f"UPDATE utenti SET saldo = %s WHERE id = %s",
                             parameters=(first_dep + final_delta, user_id))
        database.execCommand(sql=f"SELECT saldo FROM utenti WHERE id = %s",
                             parameters=(user_id, ))
        amount = database.cursor.fetchall()[0]['saldo']

        logger.info(f"User {user_id}: "
                    f"Primo deposito: {first_dep}, "
                    f"Saldo Iniziale: {vals['saldo']}, "
                    f"Totale Operazioni: {final_delta}, "
                    f"Saldo in Database Updated: {amount}")

    database.commit()
    database.close_connection()

    rep = ReportGenerator(users=users)
    rep.reportForAll()


