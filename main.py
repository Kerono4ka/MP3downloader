from mp3downloader import load_mp3_files_and_filter_by_genre


def main():
        file_name = input('Enter name of file you want to use: ')
        genre = input('Enter name of genre you want to filter: ')
        load_mp3_files_and_filter_by_genre(file_name, genre)


if __name__ == "__main__":
    main()
