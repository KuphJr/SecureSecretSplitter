# function to decode split keys given the total number of required keys
# list of key pairs and the key encoding base (either 62 or 94)
def splitKeyDecoder(totalKeys, keyPairsList, base):
    keyPairs = [[["" for s in range(2)] for w in range(len(keyPairsList[0]))]
                for k in range(totalKeys)]
    k = 0
    # the first character in each key pair represents x and the rest represents fx
    for key in keyPairsList:
        w = 0
        for subKeyPair in key:
            keyPairs[k][w][0] = subKeyPair[:1]
            keyPairs[k][w][1] = subKeyPair[1:]
            w += 1
        k += 1
    # convert from base-62 (alphanumeric) or base-94 representation to base-10 (standard numbers)
    if base == 62:
        base10keys = convertBase62keysToBase10(keyPairs)
    if base == 94:
        base10keys = convertBase94keysToBase10(keyPairs)
    # construct matricies from keys which are solved using matrix reduction to recreate the message
    matricies = constructMatricies(base10keys)
    # solve the matricies and get the resulting words of the message in base-10 format
    base10words = solve(matricies)
    # convert from base-10 format to ASCII characters
    message = convertBase10listToASCII(base10words)
    # construct a string from the list of words
    messageAsString = ""
    for word in message:
        messageAsString = messageAsString + word + " "
    return messageAsString


def solve(matricies):
    base10words = [0 for m in range(len(matricies))]
    for m in range(len(matricies)):
        base10words[m] = getSolutionFromMatrix(matricies[m])
    return base10words


def convertBase94toBase10(base94):
    if base94 == "":
        return 0
    else:
        lastChar = base94[-1:]
        base10 = ord(lastChar) - ord("!")
        remainingChar = base94[:-1]
        return base10 + 94 * convertBase94toBase10(remainingChar)


def convertBase94keysToBase10(base94keys):
    base10keys = [[["" for s in range(2)] for w in range(len(base94keys[0]))]
                    for k in range(len(base94keys))]
    k = 0
    for key in base94keys:
        w = 0
        for keyPair in key:
            # values in keyPair are stored in the format [x, fx]
            base10keys[k][w] = [convertBase94toBase10(keyPair[0]),
                                convertBase94toBase10(keyPair[1])]
            w += 1
        k += 1
    return base10keys


def convertBase62toBase10(base62):
    # converts single input from base-62 (alphanumeric) representation to base-10 representation
    base62table = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S",
                    "T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l",
                    "m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4",
                    "5","6","7","8","9"]
    if base62 == "":
        return 0
    else:
        lastChar = base62[-1:]
        base10 = base62table.index(lastChar)
        remainingChar = base62[:-1]
        return base10 + 62 * convertBase62toBase10(remainingChar)


def convertBase62keysToBase10(base62keys):
    # converts list of keyst from base-62 (alphanumeric) representation to base-10 representation
    base10keys = [[["" for s in range(2)] for w in range(len(base62keys[0]))]
                      for k in range(len(base62keys))]
    k = 0
    for key in base62keys:
        w = 0
        for keyPair in key:
            # values in keyPair are stored in the format [x, fx]
            base10keys[k][w] = [convertBase62toBase10(keyPair[0]),
                                convertBase62toBase10(keyPair[1])]
            w += 1
        k += 1
    return base10keys


def convertBase10toASCII(base10):
    # Converts from base-10 representation back to ASCII string
    q = base10 // 95
    r = base10 % 95
    if q == 0:
        return chr(ord(" ") + r)
    else:
        return convertBase10toASCII(q) + chr(ord(" ") + r)


def convertBase10listToASCII(base10list):
    # Converts a list of words from base-10 representation back to ASCII string
    words = [""] * len(base10list)
    i = 0
    for base10 in base10list:
        words[i] = convertBase10toASCII(base10)
        i += 1
    return words


def constructMatricies(splitKeys):
    # matricies are constructed from the list of keys so they can be solved with matrix reduction
    matricies = [[[0 for r in range(len(splitKeys)+1)] for c in range(len(splitKeys))]
                 for m in range(len(splitKeys[0]))]
    # for each word, construct the matrix
    for w in range(len(splitKeys[0])):
        # constructs the matricies for each word according to the formula:
        # f(x) = c1*x^n + c2*x^(n-1) + ... + cn*x^1 + C
        # The matricies have the following format:
        # key 1: [ x1^n  x1^n-1  ... x1^0 | fx1 ]
        # key 2: [ x2^n  x2^n-1  ... x2^0 | fx2 ]
        #   :    [  :       :     :    :  |  :  ]
        #   :    [  :       :     :    :  |  :  ]
        for k in range(len(splitKeys)):
            [x, fx] = splitKeys[k][w]
            for c in range(len(splitKeys)+1):
                if c < len(splitKeys):
                    matricies[w][k][c] = x ** (len(splitKeys) - c - 1)
                else:
                    matricies[w][k][c] = fx
    return matricies


def lowestGCDinList(row):
    from math import gcd
    if len(row) < 2:
        return 1
    lowestGCD = gcd(row[0],row[1])
    for j in range(1,len(row)-1):
        g = gcd(row[j], row[j+1])
        if (lowestGCD > g) and g != 0:
            lowestGCD = g
    if lowestGCD == 0:
        lowestGCD = 1
    return lowestGCD


# returns new mat with r2 = r2 - s*r1
# where s is the gcd of r1 and r2 for the specified col
def rowSubtract(mat, col, r2, r1):
    newMat = [[0 for c in range(len(mat[0]))] for c in range(len(mat))]
    for r in range(len(newMat)):
        for c in range(len(newMat[0])):
            newMat[r][c] = mat[r][c]
    scaledR1 = [0 for c in range(len(mat[0]))]
    scaledR2 = [0 for c in range(len(mat[0]))]
    newR2 = [0 for c in range(len(mat[0]))]
    for i in range(len(newR2)):
        scaledR1[i] = mat[r1][i] * mat[r2][col]
        scaledR2[i] = mat[r2][i] * mat[r1][col]
        newR2[i] = scaledR2[i] - scaledR1[i]
    lowestGCD = lowestGCDinList(newR2)
    for k in range(len(newR2)):
        newR2[k] = newR2[k] // lowestGCD
    newMat[r2] = newR2
    return newMat


def getSolutionFromMatrix(mat):
    newMat = [[0 for c in range(len(mat[0]))] for c in range(len(mat))]
    for r in range(len(newMat)):
        for c in range(len(newMat[0])):
            newMat[r][c] = mat[r][c]
    alreadyUsedRows = []
    for c in range(len(mat[0])-1):
        reducingRow = -1
        # find a valid reducing row
        for r in range(0,len(mat)):
            if (newMat[r][c] != 0) and not (r in alreadyUsedRows):
                reducingRow = r
                alreadyUsedRows.append(r)
                break
        # if a valid reducing row is found (ie: not all the rows are 0)
        if reducingRow != -1:
            for r in range(len(mat)):
                if (r != reducingRow) and (mat[r][c] != 0):
                    newMat = rowSubtract(newMat, c, r, reducingRow)     
    for r in range(len(newMat)):
        if newMat[r][-2] != 0:
            return newMat[r][-1] // newMat[r][-2]
