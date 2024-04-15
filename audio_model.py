import numpy as np

from json_tricks import dump, load

from pydub import AudioSegment, effects
import librosa
import noisereduce as nr
import os
import tensorflow as tf
from keras.models import model_from_json
from keras.models import load_model



def test():
    total_length = 314818 
    frame_length = 2048
    hop_length = 512

    folder_path = os.path.join(os.getcwd(), 'audio_repository')

    for subdir, dir, files in os.walk(folder_path):
        for file in files:
            file_path=os.path.join(folder_path,file)

    # print(file_path)

    _, sr = librosa.load(path = file_path, sr = None) # sr (the sample rate) is used for librosa's MFCCs. '_' is irrelevant.
    # Load the audio file.
    rawsound = AudioSegment.from_file(file_path)
    # Normalize the audio to +5.0 dBFS.
    normalizedsound = effects.normalize(rawsound, headroom = 0)
    # Transform the normalized audio to np.array of samples.
    normal_x = np.array(normalizedsound.get_array_of_samples(), dtype = 'float32')
    # Trim silence from the beginning and the end.
    xt, index = librosa.effects.trim(normal_x, top_db=30)
    # Pad for duration equalization.
    padded_x = np.pad(xt, (0, total_length-len(xt)), 'constant')
    # Noise reduction.
    final_x = nr.reduce_noise(padded_x, sr=sr) 

    f1 = librosa.feature.rms(y=final_x, frame_length=frame_length, hop_length=hop_length) # Energy - Root Mean Square
    f2 = librosa.feature.zero_crossing_rate(final_x , frame_length=frame_length, hop_length=hop_length, center=True) # ZCR
    f3 = librosa.feature.mfcc(y=final_x, sr=sr, n_mfcc=13, hop_length = hop_length) # MFCC
    rms = []
    zcr = []
    mfcc = []

    rms.append(f1)
    zcr.append(f2)
    mfcc.append(f3)

    f_rms = np.asarray(rms).astype('float32')
    f_rms = np.swapaxes(f_rms,1,2)
    f_zcr = np.asarray(zcr).astype('float32')
    f_zcr = np.swapaxes(f_zcr,1,2)
    f_mfccs = np.asarray(mfcc).astype('float32')
    f_mfccs = np.swapaxes(f_mfccs,1,2)

    print('ZCR shape:',f_zcr.shape)
    print('RMS shape:',f_rms.shape)
    print('MFCCs shape:',f_mfccs.shape)

    X = np.concatenate((f_zcr, f_rms, f_mfccs), axis=2)

    print(np.shape(X))

    saved_model_path = './model.json'
    saved_weights_path = './model_weights.h5'

    with open(saved_model_path , 'r') as json_file:
        json_savedModel = json_file.read()

    model = tf.keras.models.model_from_json(json_savedModel)
    model.load_weights(saved_weights_path)

    model.compile(loss='categorical_crossentropy',
                    optimizer='RMSProp',
                    metrics=['categorical_accuracy'])

    predictions = model.predict(X)
    y_pred_class = np.argmax(predictions, axis=1)
    pred=y_pred_class[0]
    print(predictions)
    print(pred)

    labels={0: 'happy', 1: 'happy', 2: 'sad', 3:'fear', 4:'fear', 5:'sad', 6: 'happy'}

    output=labels[pred]

    os.remove(file_path)
    return output