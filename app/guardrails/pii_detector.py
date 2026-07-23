
import re



def detect_pii(text):


    patterns = {

        "iran_national_id":
            r"\b\d{10}\b",


        "bank_card":
            r"\b\d{16}\b",


        "phone_number":
            r"09\d{9}",


        "email":
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",


        "password":
            r"password|رمز عبور|پسورد"

    }



    detected = []



    for name, pattern in patterns.items():

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            detected.append(name)



    return {

        "has_pii": len(detected) > 0,

        "types": detected

    }
