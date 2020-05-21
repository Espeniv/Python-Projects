# Done?
# Known problems: importing (reload needed)
# --> Run persons.py, not this file

import random
import persons  # Module cointaining person and hacker classes
import crypto_utils  # Module containing various operations for RSA
# from importlib import reload  # Used to avoid a bug occuring when importing persons
# reload(persons)

# Superclass for all other ciphers


class Cypher():

    # List and length of list containing all possible ASCII Values
    characters = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    characters_length = 95

    # Placeholder methods
    def encode(self, text):
        pass

    def decode(self, text):
        pass

    # Used for testing during development
    def verify(self, cleartext):
        ciphertext = self.encode(cleartext)
        decodedtext = self.decode(ciphertext)
        if cleartext == decodedtext:
            return True
        else:
            return False

    def generate_keys(self):
        pass

    # Find the modulo inverse of A, given M possible start-keys
    def modulo_inverse(self, A, M):
        for i in range(0, M):
            if (A*i) % M == 1:
                return i
        return -1


# A simple cipher where encoding = textvalue + key
class Caesar(Cypher):

    # All constructors set a sender and receiver for the cipher
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver
        self.generate_keys()

    # Encodes the message, given as text
    def encode(self, text):
        encoded_message = ''
        for character in text:
            clear_number = self.characters.find(character)
            if clear_number+self.sender.key < self.characters_length:
                encoded_message += self.characters[clear_number +
                                                   self.sender.key]
            else:
                encoded_message += self.characters[(clear_number +
                                                    self.sender.key) % self.characters_length]
        print("Encoded message:", encoded_message)
        return encoded_message

    # Decodes the encoded message, given as text
    def decode(self, text):
        decoded_message = ''
        for character in text:
            code_number = self.characters.find(character)
            if code_number+self.receiver.key < self.characters_length:
                decoded_message += self.characters[code_number +
                                                   self.receiver.key]
            else:
                decoded_message += self.characters[(code_number +
                                                    self.receiver.key) % self.characters_length]
        print("Decoded message:", decoded_message)
        return decoded_message

    # Generetas senderkey and receiverkey as two random integers
    def generate_keys(self):
        key = random.randint(0, self.characters_length)
        self.sender.set_key(key)
        self.receiver.set_key(self.characters_length-key)
        print("Caesar-cipher - Senderkey:", key,
              "Receiverkey:", self.characters_length-key)

    # Used in all classes to make the hackers job a little bit easier
    def possible_keys(self):
        return range(0, self.characters_length)


# Works similarly to the caesar, but now encoding = textvalue*key
class Multiplicative(Cypher):

    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver
        self.generate_keys()

    def encode(self, text):
        encoded_message = ''
        for character in text:
            clear_number = self.characters.find(character)
            if clear_number*self.sender.key < self.characters_length:
                encoded_message += self.characters[clear_number *
                                                   self.sender.key]
            else:
                encoded_message += self.characters[(clear_number *
                                                    self.sender.key) % self.characters_length]
        print("Encoded message:", encoded_message)
        return encoded_message

    def decode(self, text):
        decoded_message = ''
        for character in text:
            code_number = self.characters.find(character)
            if code_number*self.receiver.key < self.characters_length:
                decoded_message += self.characters[code_number *
                                                   self.receiver.key]
            else:
                decoded_message += self.characters[(code_number *
                                                    self.receiver.key) % self.characters_length]
        print("Decoded message:", decoded_message)
        return decoded_message

    def generate_keys(self):
        while self.sender.get_key() == None:
            key = random.randint(0, self.characters_length)
            if self.modulo_inverse(key, self.characters_length) != -1:
                self.sender.set_key(key)
                self.receiver.set_key(self.modulo_inverse(
                    key, self.characters_length))
                print("Multiplicative-cipher - Senderkey:", key,
                      "Receiverkey:", self.receiver.get_key())

    def possible_keys(self):
        return range(0, self.characters_length)


# Combines caesar and multiplicative
class Affine(Cypher):

    # Sets up a caesar and multiplicative cipher for encoding the message
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver
        self.caesar = Caesar(persons.Sender(), persons.Receiver())
        self.multiplicative = Multiplicative(
            persons.Sender(), persons.Receiver())
        self.generate_keys()

    def encode(self, text):
        encoded_message = self.caesar.encode(self.multiplicative.encode(text))
        return encoded_message

    def decode(self, text):
        decoded_message = self.multiplicative.decode(self.caesar.decode(text))
        return decoded_message

    # Keys for caesar and multiplicative are generated as a tuple
    def generate_keys(self):
        senderkey = ()
        receiverkey = ()
        self.multiplicative.generate_keys()
        self.caesar.generate_keys()
        senderkey = senderkey + \
            (self.multiplicative.sender.get_key(), self.caesar.sender.get_key())
        receiverkey = receiverkey + (self.multiplicative.receiver.get_key(),
                                     self.caesar.receiver.get_key())
        print("Affine-cipher - Senderkey:",
              senderkey, "Receiverkey:", receiverkey)

    def possible_keys(self):
        return range(0, self.characters_length)


# Uses a code-word to encode the message
class Unbreakable(Cypher):

    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver
        self.generate_keys()

    # Generates a list  of the given key to match the message length, is then used to encode
    def encode(self, text):
        encoded_message = ''
        key_repeated = ''
        i = 0
        for char in text:
            if i < len(self.sender.get_key()):
                key_repeated += self.sender.get_key()[i]
                i += 1
            else:
                i = 0
                key_repeated += self.sender.get_key()[i]
                i += 1
        n = 0
        for char in text:
            encoded_message += self.characters[((self.characters.find(char)
                                                 + self.characters.find(key_repeated[n])) % self.characters_length)]
            n += 1
        print("Encoded message:", encoded_message)
        return encoded_message

    # Reversed the operation from encode()
    def decode(self, text):
        decoded_message = ''
        decode_key_repeated = ''
        i = 0
        for char in text:
            if i < len(self.receiver.get_key()):
                decode_key_repeated += self.receiver.get_key()[i]
                i += 1
            else:
                i = 0
                decode_key_repeated += self.receiver.get_key()[i]
                i += 1
        n = 0
        for char in text:
            decoded_message += self.characters[((self.characters.find(char) +
                                                 self.characters.find(decode_key_repeated[n])) % self.characters_length)]
            n += 1
        print("Decoded message:", decoded_message)
        return decoded_message

    # Picks a random word from a list of english words for the encoding key
    def generate_keys(self):
        key = random.choice(
            open("/Users/espen/Desktop/Studier/PLab/Prosjekt3/Filer/english_words.txt").read().split())
        self.sender.set_key(key)
        receiverkey = ''
        for char in key:
            verdi = self.characters.find(char)
            newchar = self.characters[(
                self.characters_length - (verdi % self.characters_length))]
            receiverkey += newchar
        self.receiver.set_key(receiverkey)
        print("Unbreakable-cipher - Senderkey:", self.sender.get_key(),
              "Receiverkey:", self.receiver.get_key())

    def possible_keys(self):
        return open("/Users/espen/Desktop/Studier/PLab/Prosjekt3/Filer/english_words.txt").read().split()


# Secure cipher that is extremely hard to brute force by computation
class RSA(Cypher):

    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver
        self.generate_keys()

    # Encodes a single int
    def encode_one_integer(self, text):
        encoded_integer = pow(text, self.sender.get_key()[
                              1], self.sender.get_key()[0])
        return encoded_integer

    # Decodes a single int
    def decode_one_integer(self, text):
        decoded_integer = pow(text, self.receiver.get_key()[
                              1], self.receiver.get_key()[0])
        return decoded_integer

    # Encodes every block of ints, using encode_one_integer
    def encode_message(self, text):
        encoded_message = []
        blocks = crypto_utils.blocks_from_text(text, 1)  # From crypto_utils
        for block in blocks:
            encoded_block = self.encode_one_integer(block)
            encoded_message.append(encoded_block)
        encoded_message_formatted = ''
        for block in encoded_message:
            encoded_message_formatted += str(block)
        print("Encoded message:", encoded_message_formatted)
        return encoded_message

    # Reverses the process, done in the encoding
    def decode_message(self, text):
        decoded_blocks = []
        for block in text:
            decoded_blocks.append(self.decode_one_integer(block))
        decoded_message = crypto_utils.text_from_blocks(
            decoded_blocks, 8)  # From crypto_utils
        print("Decoded message:", decoded_message)
        return decoded_message

    # Generates keys based on an algorithm involving random primes
    def generate_keys(self):
        p = crypto_utils.generate_random_prime(8)  # From crypto_utils
        q = crypto_utils.generate_random_prime(8)
        if p != q:
            n = p*q
            o = (p-1)*(q-1)
            d = -1
            while d == -1:
                e = random.randint(3, o-1)
                d = self.modulo_inverse(e, o)
            sender_key = ()
            # Sender and receiver keys set as tuples
            sender_key = sender_key + (n, e)
            receiver_key = ()
            receiver_key = receiver_key + (n, d)
            self.sender.set_key(sender_key)
            self.receiver.set_key(receiver_key)
            print("RSA-cipher - Senderkey:", self.sender.get_key(),
                  "Receiverkey:", self.receiver.get_key())
        else:
            print(p, q, "- Wow! Dette ble like primtall!")
            return -1


###########Tester############

def test_ciphers():
    # Testing Caesar
    s1 = persons.Sender()
    r1 = persons.Receiver()
    c1 = Caesar(s1, r1)
    encodedmessage1 = c1.encode("Caesar-cipheret funker!")
    c1.decode(encodedmessage1)
    print("---------------")

    # Testing Multiplicative
    s2 = persons.Sender()
    r2 = persons.Receiver()
    m1 = Multiplicative(s2, r2)
    encodedmessage2 = m1.encode("Multiplicative-cipheret funker!")
    m1.decode(encodedmessage2)
    print("---------------")

    # Testing Affine
    s3 = persons.Sender()
    r3 = persons.Receiver()
    a1 = Affine(s3, r3)
    encodedmessage3 = a1.encode("Affine-cipheret funker!")
    a1.decode(encodedmessage3)
    print("---------------")

    # Testing Unbreakable
    s4 = persons.Sender()
    r4 = persons.Receiver()
    u1 = Unbreakable(s4, r4)
    encodedmessage4 = u1.encode("Unbreakable-cipheret funker!")
    u1.decode(encodedmessage4)
    print("---------------")

    # Testing RSA
    s5 = persons.Sender()
    r5 = persons.Receiver()
    rsa1 = RSA(s5, r5)
    encodedmessage5 = rsa1.encode_message("RSA-cipheret funker!")
    rsa1.decode_message(encodedmessage5)
    print("---------------")


def test_hacker():
    # Testing Hacker
    h1 = persons.Hacker()

    # Caesar brute force
    c2 = Caesar(persons.Sender(), persons.Receiver())
    encodedhackermessage = c2.encode("Hello World")
    h1.brute_force(encodedhackermessage, c2)
    print("---------------")

    # Multiplicative brute force
    m2 = Multiplicative(persons.Sender(), persons.Receiver())
    encodedhackermessage2 = m2.encode("Brute forcing a multiplicative-cipher")
    h1.brute_force(encodedhackermessage2, m2)
    print("---------------")

    # Affine brute force
    a2 = Affine(persons.Sender(), persons.Receiver())
    encodedhackermessage3 = a2.encode("Easy Peasy")
    h1.brute_force(encodedhackermessage3, a2)
    print("---------------")

    # Unbreakable brute force
    u2 = Unbreakable(persons.Sender(), persons.Receiver())
    encodedhackermessage4 = u2.encode("Maniac Moffi")
    h1.brute_force(encodedhackermessage4, u2)


# test_ciphers()

test_hacker()
