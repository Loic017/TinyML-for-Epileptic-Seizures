def create_labels(raw_edf, epochs, annotations, n_epochs, duration):
    data, time = raw_edf.get_data(return_times=True)
    duration_seconds = time[-1]

    epoch_duration = int(duration_seconds / n_epochs)
    print(epoch_duration)

    duration_seconds = int(time[-1]) + 1
    label_list = []
    for i in range(0, duration_seconds, epoch_duration):
        lower_boundary = i
        upper_boundary = i + epoch_duration

        for j in annotations:
            lower_event_boundary = float(j[0])
            upper_event_boundary = float(j[1])
            curr_event = []

            print(lower_boundary)
            print(upper_boundary)
            print("---")
            print(lower_event_boundary)
            print(upper_event_boundary)
            break

            if (
                lower_boundary <= upper_event_boundary
                and upper_event_boundary <= upper_boundary
            ):
                curr_event.append(j[2])
            print(curr_event)

            if len(curr_event) == 1:
                label_list.append(curr_event[0])
            else:
                label_list.append(curr_event)

        break
    return label_list


print(create_labels(raw_edf, epochs, annotations, 712))

#####


# Get freq points where mel filters will be applied
def get_filter_points(fmin, fmax, mel_filter_num, FFT_size, sample_rate):
    fmin_mel = librosa.hz_to_mel(fmin)  # Formula: 2595 * np.log10(1 + f / 700)
    fmax_mel = librosa.hz_to_mel(fmax)

    print("MEL min: {0}".format(fmin_mel))
    print("MEL max: {0}".format(fmax_mel))

    mels = np.linspace(fmin_mel, fmax_mel, num=mel_filter_num + 2)
    freqs = librosa.mel_to_hz(mels)

    return np.floor((FFT_size + 1) / sample_rate * freqs).astype(int), freqs


filter_points, mel_freqs = get_filter_points(
    freq_min, freq_high, n_mels, fft_size, sample_rate=250
)
filter_points


# Get filters that will be applied
def get_filters(filter_points, FFT_size):
    # amplify lower filters
    filters = np.zeros((len(filter_points) - 2, int(FFT_size / 2 + 1)))

    for n in range(len(filter_points) - 2):
        filters[n, filter_points[n] : filter_points[n + 1]] = np.linspace(
            0, 1, filter_points[n + 1] - filter_points[n]
        )
        filters[n, filter_points[n + 1] : filter_points[n + 2]] = np.linspace(
            1, 0, filter_points[n + 2] - filter_points[n + 1]
        )

    return filters


filters = get_filters(filter_points, fft_size)

plt.figure(figsize=(15, 4))
for n in range(filters.shape[0]):
    plt.plot(filters[n])

enorm = 2.0 / (mel_freqs[2 : mel_filter_num + 2] - mel_freqs[:mel_filter_num])
filters *= enorm[:, np.newaxis]

plt.figure(figsize=(15, 4))
for n in range(filters.shape[0]):
    plt.plot(filters[n])


# image stuff
# %% capture
image_train = []
for i, data in enumerate(train_db_mean):
    f = plt.figure(frameon=False)
    ax = plt.Axes(f, [0.0, 0.0, 1.0, 1.0])
    ax.set_axis_off()
    f.add_axes(ax)
    img = librosa.display.specshow(data, sr=250, x_axis="time", y_axis="mel")
    plt.savefig("image_process.png")

    img = Image.open("image_process.png")
    img = img.resize((120, 160))
    image_train.append(img)
    plt.close("all")
image_train = np.array(image_train)

image_val = []
for i, data in enumerate(val_db_mean):
    f = plt.figure(frameon=False)
    ax = plt.Axes(f, [0.0, 0.0, 1.0, 1.0])
    ax.set_axis_off()
    f.add_axes(ax)
    img = librosa.display.specshow(data, sr=250, x_axis="time", y_axis="mel")
    plt.savefig("image_process.png")

    img = Image.open("image_process.png")
    img = img.resize((120, 160))
    image_val.append(img)
    plt.close("all")
image_val = np.array(image_val)

fix_shape = []
for i, image in enumerate(image_train):
    image = image.transpose((2, 0, 1))
    fix_shape.append(image)
fix_shape = np.array(fix_shape)

fix_shape_val = []
for i, image in enumerate(image_val):
    image = image.transpose((2, 0, 1))
    fix_shape_val.append(image)
fix_shape_val = np.array(fix_shape_val)

image_train = fix_shape
image_val = fix_shape_val

fix_shape.shape, fix_shape_val.shape
