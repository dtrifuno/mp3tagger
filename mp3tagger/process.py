def add_album_art(mp3_file_name: str):
    art_file_name = os.path.join(os.path.dirname(mp3_file_name), 'cover.jpg')
    if not os.path.isfile(art_file_name):
        return
    art_data = open(art_file_name, "rb").read()
    file_ = EasyMP3(mp3_file_name, ID3=ID3)
    file_.tags.add(
        APIC(encoding=3,  # UTF-8
             type=3,  # cover
             mime='image/jpeg',
             data=art_data
             )
    )
    file_.save()


def process_file(dir_path: str, file_path: str, regex: re.Pattern, *, delete=False, cover=False):
    # only process mp3s
    if not file_path.endswith('.mp3'):
        return

    # report file paths that don't match formula
    match = regex.match(file_path)
    if not match:
        print(f"{file_path} does not match formula, skipping...")
        return

    tags = match.groupdict()

    full_path = os.path.join(dir_path, file_path)
    file_ = EasyMP3(full_path)

    if delete:
        file_.delete()
    for tag_name, tag_value in tags.items():
        file_[tag_name] = tag_value
    file_.save()

    if cover:
        add_album_art(full_path)