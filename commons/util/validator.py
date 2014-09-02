# -*- coding: utf-8 -*-


class Validator():
    @staticmethod
    def password(password):
        import re
        # Check if contains at least one digit
        if re.search(r'\d', password) and \
            re.search(r'[a-zA-Z]', password) and \
            re.search(r'[ÀÁÂÃÄÅàáâãäåÒÓÔÕÖØòóôõöøÈÉÊËèéêëÇçÌÍÎÏìíîïÙÚÛÜùúûüÿÑ&!?*$^+)è(%ñ_-]', password) and \
            len(password) > 6:
                return True
        return False

    @staticmethod
    def mail(mail, check_mx=False, verify=False):
        from validate_email import validate_email
        return validate_email(mail,verify,check_mx)


    @staticmethod
    def zipcode(zipcode):
        import re
        regex = "/^\+?([0-9]{2})\)?[-. ]?([0-9]{4})[-. ]?([0-9]{4})$/";
        return re.search(regex, zipcode)