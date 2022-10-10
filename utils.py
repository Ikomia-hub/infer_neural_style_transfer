import requests
import os

model_zoo = {
    "eccv16": {
        "the_wave": {
            "model": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/the_wave.t7",
            "img": "the_wave.jpg"},
        "la_muse": {
            "model": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/la_muse.t7",
            "img": "la_muse.jpg"},
        "starry_night": {
            "model": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/starry_night.t7",
            "img": "starry_night.jpg"},
        "composition_vii": {
            "model": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/composition_vii.t7",
            "img": "composition_vii.jpg"},

    },
    "instance_norm": {"candy": {
        "model": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models"
                 "/instance_norm/candy.t7",
        "img": "candy.jpg"},
        "mosaic": {
            "model": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm"
                     "/mosaic.t7",
            "img": "mosaic.jpg"},
        "the_scream": {
            "model": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm"
                     "/the_scream.t7",
            "img": "the_scream.jpg"},
        "udnie": {
            "model": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm"
                     "/udnie.t7",
            "img": "udnie.jpg"},
        "feathers": {
            "model": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm"
                     "/feathers.t7",
            "img": "feathers.jpg"},
        "la_muse": {
            "model": "http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm"
                     "/la_muse.t7",
            "img": "la_muse.jpg"}
    }
}


def download_model(method, name, models_folder):
    URL = model_zoo[method][name]["model"]
    response = requests.get(URL)
    model_folder = os.path.join(models_folder, method)
    os.makedirs(model_folder, exist_ok=True)

    with open(os.path.join(model_folder, f"{name}.t7"), "wb") as f:
        f.write(response.content)
