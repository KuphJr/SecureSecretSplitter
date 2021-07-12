from secrets import randbelow
import random

# function to create split keys given the key encoding base (either 62 or 94),
# required number of keys to recreate the message, total number of keys to be generated,
# and the message to be split
# keyFormat indicates if the keys should be encoded in base62 or base94
def splitKeyCreator(base, reqNumKeys, totalNumKeys, message):
    # Create a list where each element is a single word for the original message
    words = message.split(" ")
    # Convert the words from ASCII into base-10 numbers
    base10words = convertWordListToBase10(words)
    # Use the Shamir Secret Sharing Algorithm to generate the keys in base-10 format
    base10keys = shamirSplit(reqNumKeys, totalNumKeys, base10words)
    # Convert the base10keys to alphanumerical characters (base-62 characters)
    # or alphanumerical characters and symbols (base-94) and return
    if base == 62:
        formattedkeys = convertKeyListToBase62(base10keys)
    else:
        formattedkeys = convertKeyListToBase94(base10keys)
    # The first element in each key contains information about the total number of keys that
    # are required to recreate the original message. This is required to combine the keys
    keys = [["" for w in range(len(words)+1)] for k in range(totalNumKeys)]
    for keyNum in range(totalNumKeys):
        keys[keyNum][0] = "k" + str(reqNumKeys) + "b" + str(base)
        for wordNum in range(len(words)):
            keys[keyNum][wordNum+1] = formattedkeys[wordNum][keyNum]
    keysAsStrings = [""] * totalNumKeys
    k = 0
    for key in keys:
        for word in key:
            keysAsStrings[k] = keysAsStrings[k] + " " + word
        keysAsStrings[k] = keysAsStrings[k][1:]
        k += 1        
    return keysAsStrings


def convertWordListToBase10(wordList):
    # Convert from base-95 (valid ASCII characters) to base-10 (traditional numbers)
    # Valid ASCII characters are from ' ' to '~'
    # See ASCII table here: https://www.rapidtables.com/code/text/ascii-table.html
    base10 = [0] * len(wordList)
    i = 0
    for word in wordList:
        base10word = 0
        exp = len(word) - 1
        for character in word:
            base10word += (ord(character) - ord(" ")) * 95 ** exp
            exp -= 1
        base10[i] = base10word
        i += 1
    return base10


def shamirSplit(requiredKeys, totalKeys, base10words):
    # Implementation of the Shamir Secret Sharing algorithm
    maxDeg = requiredKeys - 1
    # This is the degree of the randomly generated polynomials
    keys = [[[0 for c in range(2)] for k in range(totalKeys)] for w in range(len(base10words))]
    wordNum = 0
    # Generate the random polynomial for each word
    for base10word in base10words:
        coeffs = [0 for c in range(maxDeg)]
        # coeffs is the list of coefficents
        for coeffNum in range(maxDeg):
            coeffs[coeffNum] = randbelow(18446744073709551616) + 1
        for keyNum in range(totalKeys):
            # Ensure x is notused to generate a previous key
            xIsInvalid = True
            while xIsInvalid:
                # x is between 1-61 so it can be represented as one non-zero character in base-62
                x = random.randint(1,61)
                xIsInvalid = False
                for [existingX, _] in keys[wordNum]:
                    if x == existingX:
                        xIsInvalid = True
            # keys stores the values in the form:
            # [word1: [key1: [x, fx], key2: [x, fx], ...], word2: [key1: [x, fx], ...], ...]
            keys[wordNum][keyNum][0] = x
            # Use the coefficents to calculate the result of the polynomial at x
            # Formula: f(x) = c1*x^n + c2*x^(n-1) + ... + cn*x^1 + C
            # where C is the word (expressed in base-10) which must be split
            exp = maxDeg
            for coeff in coeffs:
                keys[wordNum][keyNum][1] += coeff * x ** exp
                exp += -1
            keys[wordNum][keyNum][1] += base10word
        wordNum += 1
    return keys


def convertKeyListToBase62(base10keys):
    # Converts the base-10 keys into base-62 (alphanumeric) keys.
    # For the subkey (x, fx) corresponding to each word, x is stored as the first character and the
    # remaining characters represent fx which is the result of the random polynomial at point x
    base62 = [["" for w in range(len(base10keys[0]))] for k in range(len(base10keys))]
    wordNum = 0
    for keysPerWord in base10keys:
        keyNum = 0
        for [x, fx] in keysPerWord:
            base62[wordNum][keyNum] = convertBase10toBase62(x) + convertBase10toBase62(fx)
            keyNum += 1
        wordNum += 1
    return base62


def convertBase10toBase62(x):
    # Convert x from base-10 to base-62 where:
    # 0 = A, 1 = B, ... , 25 = Z, 26 = a, 27 = b, ... , 51 = z, 52 = 0, 53 = 1, ... , 61 = 9
    base62table = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S",
                    "T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l",
                    "m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4",
                    "5","6","7","8","9"]
    q = x // 62
    r = x % 62
    if q == 0:
        return base62table[r]
    else:
        return convertBase10toBase62(q) + base62table[r]


def convertKeyListToBase94(base10keys):
    # Converts the base-10 keys into base-94 (ASCII) keys w/o SPACE character
    # For the subkey (x, fx) corresponding to each word, x is stored as the first character and the
    # remaining characters represent fx which is the result of the random polynomial at point x
    base94 = [["" for w in range(len(base10keys[0]))] for k in range(len(base10keys))]
    wordNum = 0
    for keysPerWord in base10keys:
        keyNum = 0
        for [x, fx] in keysPerWord:
            base94[wordNum][keyNum] = convertBase10toBase94(x) + convertBase10toBase94(fx)
            keyNum += 1
        wordNum += 1
    return base94


def convertBase10toBase94(x):
    q = x // 94
    r = x % 94
    if q == 0:
        return chr(r+ord("!"))
    else:
        return convertBase10toBase94(q) + chr(r+ord("!"))
