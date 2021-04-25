import pickle


def pkl_load(path: str):
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data


def pkl_save(data, path: str):
    pickle.dump(data, open(path, "wb"))
