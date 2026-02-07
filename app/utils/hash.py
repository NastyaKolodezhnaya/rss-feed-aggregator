import bcrypt


def get_hashed_password(hash_pass):
    return bcrypt.hashpw(hash_pass.encode('utf-8'), bcrypt.gensalt())


def check_password(text_pass, hash_pass):
    return bcrypt.checkpw(text_pass.encode('utf-8'), hash_pass)
