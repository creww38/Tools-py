import itertools

def brute_force_password(wordlist, password):
    for L in range(1, len(wordlist) + 1):
        for combo in itertools.combinations(wordlist, L):
            attempt = ''.join(combo)
            if attempt == password:
                return attempt
    return None

wordlist = 'abcdefghijklmnopqrstuvwxyz'
password = 'cat'
found_password = brute_force_password(wordlist, password)
print(f'Found password: {found_password}')
