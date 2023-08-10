import requests
import os

model_zoo = {
    "eccv16": {
        "the_wave": {
            "model": "https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/the_wave.t7",
            "img": "the_wave.jpg"},
        "la_muse": {
            "model": "https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/la_muse.t7",
            "img": "la_muse.jpg"},
        "starry_night": {
            "model": "https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/starry_night.t7",
            "img": "starry_night.jpg"},
        "composition_vii": {
            "model": "https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/composition_vii.t7",
            "img": "composition_vii.jpg"},

    },
    "instance_norm": {"candy": {
        "model": "https://cs.stanford.edu/people/jcjohns/fast-neural-style/models"
                 "/instance_norm/candy.t7",
        "img": "candy.jpg"},
        "mosaic": {
            "model": "https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm"
                     "/mosaic.t7",
            "img": "mosaic.jpg"},
        "the_scream": {
            "model": "https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm"
                     "/the_scream.t7",
            "img": "the_scream.jpg"},
        "udnie": {
            "model": "https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm"
                     "/udnie.t7",
            "img": "udnie.jpg"},
        "feathers": {
            "model": "https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm"
                     "/feathers.t7",
            "img": "feathers.jpg"},
        "la_muse": {
            "model": "https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm"
                     "/la_muse.t7",
            "img": "la_muse.jpg"}
    }
}


def download_model(method, name, models_folder):
    URL = model_zoo[method][name]["model"]

# Download the dataset
    model_folder = os.path.join(models_folder, method)
    print(URL)
    response = requests.get(URL, stream=True)
    with open(os.path.join(model_folder, f"{name}.t7"), "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

