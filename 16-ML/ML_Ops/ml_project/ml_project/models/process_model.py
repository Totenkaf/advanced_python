"""Copyright 2022 by Artem Ustsov"""
import pickle


def serialize_model(model: object, output_obj: str) -> str:
    with open(output_obj, "wb") as f:
        pickle.dump(model, f)
    return output_obj


def deserialize_model(input_obj: str) -> object:
    with open(input_obj, "rb") as f:
        model = pickle.load(f)
    return model
