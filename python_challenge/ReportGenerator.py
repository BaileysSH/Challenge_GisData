import datetime
import logging


class ReportGenerator(object):
    logger = logging.getLogger("ReportGenerator")

    def __init__(self, users: dict, path: str = '.'):
        self._path = path
        self._users = users

    @property
    def users(self):
        return self._users

    def operations(self, user_id):
        if user_id in self._users:
            return self._users[user_id]['operazioni']
        return []

    @staticmethod
    def _get_max_len(user_oper: list):
        """
        compute the maximum length of the string occupied by the amount
        """
        max_operation = max(user_oper, key=lambda x: x['ammontare'])
        min_operation = min(user_oper, key=lambda x: x['ammontare'])

        return max(len(str(max_operation['ammontare'])), len(str(min_operation['ammontare'])))

    def reportForUser(self, user_id):
        self.logger.info(f"Generating report for user_id = {user_id}...")
        filename = f"{user_id}.txt"

        txt = self._actualReportForUser(user_id=user_id)
        self.savetxt(obj=txt, filename=filename, path=self._path)

    def _actualReportForUser(self, user_id):
        # retrieve only operations for the given user_id
        user_oper = self.operations(user_id=user_id)

        # sort them by date
        user_oper.sort(key=lambda x: x['giorno'])

        # get user name
        user = self._users[user_id]['nome']

        txt = ""
        txt += user

        # return if current user does not have any operations
        if not user_oper:
            return txt

        txt += '\n'

        # compute the maximum length of the string occupied by the amount
        max_len = self._get_max_len(user_oper)

        for oper in user_oper:
            date = oper['giorno']  # type: datetime.date
            amount = str(oper['ammontare']).replace('.', ',')

            txt += '\n' + date.strftime("%d/%m/%Y") + " ** " + "€" + ' ' * (max_len + 1 - len(amount)) + amount

        return txt

    def reportForAll(self):
        self.logger.info("Start generating all reports...")
        for user_id in self._users:
            self.reportForUser(user_id=user_id)
	self.logger.info("Generated all reports")

    def savetxt(self, obj: str, filename: str, path: str):
        """
        generic function to save an object to txt file
        :param obj:
        :param filename:
        :param path:
        :return:
        """
        try:
            with open(f'{path}/{filename}', 'w') as file:
                file.writelines(line for line in obj)
        except (IOError, OSError) as e:
            self.logger.warning(f"Can't write '{filename}' file: {e}")
            return
        self.logger.info(f"'{filename}' file correctly saved")
