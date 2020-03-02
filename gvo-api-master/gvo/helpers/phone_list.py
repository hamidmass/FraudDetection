ADDRESS_REQUIREMENTS = {"none": 0, "any": 1, "foreign": 3, "local": 4}


class PhoneList:
    @staticmethod
    def json(phone_list):
        phone_list.sort(key=lambda phone: ADDRESS_REQUIREMENTS[phone.address_requirements])
        return [{"phone_number": phone.phone_number,
                 "address_requirements": phone.address_requirements,
                 "region": phone.region,
                 "capabilities": phone.capabilities} for phone in phone_list]
