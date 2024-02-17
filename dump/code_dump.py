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
