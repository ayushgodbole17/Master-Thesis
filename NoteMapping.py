import os
import librosa
import numpy as np
import pandas as pd
import textgrid
import warnings

# Base directories
audio_base_dir = "dataset_for_mfa/rapper_songs"
textgrid_base_dir = "dataset_for_mfa/new_aligned"

# List to store all results
all_results = []

# C major scale in terms of MIDI numbers
c_major_scale = [0, 2, 4, 5, 7, 9, 11]  # C, D, E, F, G, A, B

# Define the note to MIDI number mapping
note_to_midi = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, 
    "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
}

# Reverse mapping for transposed notes
midi_to_note = {v: k for k, v in note_to_midi.items()}

# Function to find the closest note in the C major scale
def closest_note_in_c_major(midi_value):
    differences = [(abs((midi_value % 12) - note), note) for note in c_major_scale]
    closest_note = min(differences, key=lambda x: x[0])[1]
    return closest_note

# Function to transpose a note to C major
def transpose_note_to_c(note):
    if note == "Rest":
        return note
    if note[:-1] in note_to_midi:
        midi_value = note_to_midi[note[:-1]]  # Remove the octave number
        octave = int(note[-1])
        closest_c_major_note = closest_note_in_c_major(midi_value)
        transposed_note = midi_to_note[closest_c_major_note]
        return f"{transposed_note}{octave}"
    else:
        return note

# Function to calculate the average pitch for each interval
def calculate_average_pitch(y, sr, start_time, end_time):
    start_sample = int(start_time * sr)
    end_sample = int(end_time * sr)
    segment = y[start_sample:end_sample]

    if len(segment) < sr * 0.05:  # Skip segments shorter than 50ms
        return np.nan

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        pitches, magnitudes = librosa.piptrack(y=segment, sr=sr, n_fft=2048, hop_length=512, fmin=50, fmax=2000)

        pitch_indices = magnitudes.argmax(axis=0)
        pitch_values = pitches[pitch_indices, range(pitches.shape[1])]
        non_zero_pitches = pitch_values[pitch_values > 0]

        if len(non_zero_pitches) == 0:
            return np.nan
        return np.mean(non_zero_pitches)

# Function to map pitch (Hz) to the nearest musical note
def pitch_to_note_name(pitch):
    if np.isnan(pitch) or pitch == 0:
        return "Rest"

    A4_freq = 440.0
    semitones_from_A4 = 12 * np.log2(pitch / A4_freq)
    midi_note = int(round(semitones_from_A4)) + 69  # 69 is the MIDI note number for A4
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_name = note_names[midi_note % 12]
    octave = midi_note // 12 - 1  # MIDI note 0 is C-1
    return f"{note_name}{octave}"

# Find the corresponding word for each phone interval
def find_word_for_phone(start_time, end_time, word_intervals):
    for word_start, word_end, word in word_intervals:
        if word_start <= start_time and word_end >= end_time:
            return word
    return ""

# Process each subdirectory
for rapper in range(1, 16):  # Assuming you have 15 subdirectories named rapper1 to rapper15
    for song in range(1, 16):  # Assuming each rapper has 15 songs
        audio_file = os.path.join(audio_base_dir, f"rapper{rapper}", f"rapper{rapper}_song{song}.wav")
        textgrid_file = os.path.join(textgrid_base_dir, f"rapper{rapper}", f"rapper{rapper}_song{song}.TextGrid")

        # Check if both files exist
        if not os.path.isfile(audio_file) or not os.path.isfile(textgrid_file):
            continue

        # Load the audio file with librosa
        try:
            y, sr = librosa.load(audio_file, sr=None)
        except Exception as e:
            print(f"Failed to load audio file {audio_file}: {e}")
            continue

        # Ensure the audio is mono
        if y.ndim > 1:
            y = np.mean(y, axis=1)

        # Remove non-finite values
        y = np.nan_to_num(y)

        # Load the TextGrid file
        try:
            tg = textgrid.TextGrid.fromFile(textgrid_file)
        except Exception as e:
            print(f"Failed to load TextGrid file {textgrid_file}: {e}")
            continue

        # Add a start marker for the song
        all_results.append((None, None, None, None, '<START>', f'rapper{rapper}_song{song}'))

        # Extract intervals from the TextGrid
        phone_intervals = []
        word_intervals = []
        for tier in tg.tiers:
            if tier.name == 'phones':
                for interval in tier.intervals:
                    start_time = interval.minTime
                    end_time = interval.maxTime
                    mark = interval.mark.strip()
                    if not mark:
                        mark = "empty"  # Mark empty intervals
                    phone_intervals.append((start_time, end_time, mark))
            elif tier.name == 'words':
                for interval in tier.intervals:
                    start_time = interval.minTime
                    end_time = interval.maxTime
                    mark = interval.mark.strip()
                    word_intervals.append((start_time, end_time, mark))

        # Calculate average pitch for each interval and determine the note
        results = []
        for i, (start_time, end_time, phone) in enumerate(phone_intervals):
            avg_pitch = calculate_average_pitch(y, sr, start_time, end_time)
            if phone == "empty":
                avg_pitch = 0.0  # Assign pitch value of zero to empty intervals
            note_name = pitch_to_note_name(avg_pitch)
            note_name_transposed = transpose_note_to_c(note_name)  # Transpose the note to C major
            word = find_word_for_phone(start_time, end_time, word_intervals)
            results.append((start_time, end_time, avg_pitch, phone, note_name_transposed, word))

        all_results.extend(results)

        # Add an end marker for the song
        all_results.append((None, None, None, None, '<END>', f'rapper{rapper}_song{song}'))
        print(f"Processed {textgrid_file}")

# Convert all results to a DataFrame
df = pd.DataFrame(all_results, columns=['Start Time', 'End Time', 'Average Pitch', 'Phone', 'Note', 'Word'])

# Replace NaN values in 'Average Pitch' with zero
df['Average Pitch'].fillna(0, inplace=True)

# Apply special tokens to 'Note'
df['Note'] = df['Note'].apply(lambda x: f'<NOTE>{x}' if x not in ['<START>', '<END>', 'Rest'] else x)

# Replace NaN values in 'Word' with 'REST'
df['Word'].fillna('REST', inplace=True)

# Save the final DataFrame to a CSV file
output_csv = "final_melody_data.csv"
df.to_csv(output_csv, index=False)
print("Final DataFrame:")
print(df)
print(f"Processed data saved to {output_csv}")

# Load the original CSV file
csv_file_path = 'final_melody_data.csv'
df = pd.read_csv(csv_file_path)

# Initialize variables to store concatenated notes and words
concatenated_notes = []
concatenated_words = []
sentence_counter = 0
rows = []

# Iterate through the dataframe
for index, row in df.iterrows():
    word = row['Word']
    note = row['Note']

    # Check for <START> and <END> tokens and directly copy them
    if note in ['<START>', '<END>']:
        if concatenated_notes:
            sentence_id = f"sentence_{sentence_counter}"
            rows.append([sentence_id, ' '.join(concatenated_notes), ' '.join(concatenated_words)])
            concatenated_notes = []
            concatenated_words = []
            sentence_counter += 1
        rows.append([None, note, word])
        continue

    # If the note is 'Rest', this signals the end of a sentence
    if note == 'Rest':
        if concatenated_notes:
            sentence_id = f"sentence_{sentence_counter}"
            rows.append([sentence_id, ' '.join(concatenated_notes), ' '.join(concatenated_words)])
            concatenated_notes = []
            concatenated_words = []
            sentence_counter += 1
    else:
        concatenated_notes.append(note)
        if word and not pd.isna(word):
            if not concatenated_words or word != concatenated_words[-1]:
                concatenated_words.append(word)

# Ensure the last sequence is added if it wasn't followed by a Rest
if concatenated_notes:
    sentence_id = f"sentence_{sentence_counter}"
    rows.append([sentence_id, ' '.join(concatenated_notes), ' '.join(concatenated_words)])

# Create a new DataFrame for the concatenated sequences
new_df = pd.DataFrame(rows, columns=['Sentence ID', 'Concatenated Notes', 'Concatenated Words'])

# Save the new DataFrame to a CSV file
output_csv_path = 'concatenated_melody_sentences.csv'
new_df.to_csv(output_csv_path, index=False)
print(f"New CSV file saved to {output_csv_path}")
print(new_df.head(50))