import crypto  # Needed for the Hackers brute_force method

# Superclass for Sender, Receiver og Hacker


class Person():

    key = None
    cypher = None

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def operate_cypher(self):
        pass

# Only contains operate_cypher, encodes


class Sender(Person):

    def operate_cypher(self):
        self.cypher.encode()

# Only contains operate_cypher, decodes


class Receiver(Person):

    def operate_cypher(self):
        self.cypher.decode()

# Brute_forces tries all possible keys to decode the message


class Hacker(Person):

    checklist = open(
        "/Users/espen/Desktop/Studier/PLab/Prosjekt3/Filer/english_words.txt").read().split()

    def brute_force(self, encoded_message, cipher):
        # Ceasar and Multiplicative share the same keys/pattern to decode
        if isinstance(cipher, (crypto.Caesar, crypto.Multiplicative)):
            for x in cipher.possible_keys():
                cipher.receiver.key = x
                decode_attempt = cipher.decode(encoded_message).split()
                # Checks if word in checklist, and plausible(len>3)
                for word in decode_attempt:
                    if word.lower() in self.checklist and len(word) > 3:
                        correct_message = ''
                        for word in decode_attempt:
                            correct_message += word + " "
                        print("Muhaha! Message:", correct_message,
                              "- Dekrypterings-nokkelen var:", x)
                        return decode_attempt
        # Affine uses two keys in a tuple to decode
        elif isinstance(cipher, crypto.Affine):
            for x in cipher.possible_keys():
                for y in cipher.possible_keys():
                    cipher.caesar.receiver.key = x
                    cipher.multiplicative.receiver.key = y
                    decode_attempt = cipher.decode(encoded_message).split()
                    # Checks if word in checklist, and plausible(len>3)
                    for word in decode_attempt:
                        if word.lower() in self.checklist and len(word) > 3:
                            key_tuple = (x, y)
                            correct_message = ''
                            for word in decode_attempt:
                                correct_message += word + " "
                            print("Muhaha! Message:", correct_message,
                                  "- Dekrypterings-nokkelen var:", key_tuple)
                            return decode_attempt
        # Unbreakable needs the "inverse" of a word to decode
        elif isinstance(cipher, crypto.Unbreakable):
            for x in cipher.possible_keys():
                testkey = ''
                for char in x:
                    verdi = crypto.Cypher.characters.find(char)
                    newchar = crypto.Cypher.characters[crypto.Cypher.characters_length - (
                        verdi % crypto.Cypher.characters_length)]  # Calculates the "inverse" word
                    testkey += newchar
                #print("Testing key:",testkey)
                cipher.receiver.key = testkey
                decode_attempt = cipher.decode(encoded_message).split()
                # Checks if word in checklist, and plausible(len>3)
                for word in decode_attempt:
                    if word.lower() in self.checklist and len(word) > 5:
                        correct_message = ''
                        for word in decode_attempt:
                            correct_message += word + " "
                        print("Muhaha! Message:", correct_message,
                              "- Krypterings-nokkelen var:", x)
                        return decode_attempt
