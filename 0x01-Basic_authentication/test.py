#!/usr/bin/env python3
def extract_user_credentials(decoded_base64_authorization_header: str) -> (str, str):
        """
            returns the user email and password from the Base64 decoded value.
        """

        a = decoded_base64_authorization_header
        result = None

        if not a:
            return (None, None)
        elif type(a) != str:
            return (None, None)
        elif len(a.split(':')) == 1:
            return (None, None)
        elif len(a.split(':')) == 2:
            result = (a.split(':')[0], a.split(':')[1])
        else:
            email = a.split(':')[0]
            password = ''
            temp = a.split(':')[1:]
            for i in range(len(temp)):
                if i < len(temp) - 1:
                    password += f'{temp[i]}:'
                else:
                    password += temp[i]
            result = (email, password)
            print(result)
        return result
print(extract_user_credentials('powell:123:123:123:'))
