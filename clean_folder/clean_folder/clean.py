import re
import sys
from pathlib import Path
import shutil

CYRILLIC_SYMBOLS = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "h", "g", "d", "e", "ie", "zh", "z", "y", "i", "yi", "j", "k", "l",
               "m", "n", "o", "p", "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "shch", "", "yu", "ya")

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()


def normalize(name: str) -> str:
    translate_name = re.sub(r'[^0-9a-zA-Z\.]', '_', name.translate(TRANS))
    return translate_name


JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
XLS_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPT_DOCUMENTS = []
PPTX_DOCUMENTS = []
PDF_DOCUMENTS = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []
ISO_IMAGE = []
IMG_IMAGE = []
MY_OTHER = []


REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_DOCUMENTS,
    'DOCX': DOCX_DOCUMENTS,
    'TXT': TXT_DOCUMENTS,
    'XLS': XLS_DOCUMENTS,
    'XLSX': XLSX_DOCUMENTS,
    'PPT': PPT_DOCUMENTS,
    'PPTX': PPTX_DOCUMENTS,
    'PDF': PDF_DOCUMENTS,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ZIP_ARCHIVES,
    'GZ': GZ_ARCHIVES,
    'TAR': TAR_ARCHIVES,
    'ISO': ISO_IMAGE,
    'IMG': IMG_IMAGE,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()


def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER', 'image'):
                FOLDERS.append(item)
                scan(item)
            continue

        extension = get_extension(item.name)
        full_name = folder / item.name
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                extension_registration = REGISTER_EXTENSION[extension]
                extension_registration.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                MY_OTHER.append(full_name)


def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))


def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / \
        normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()),
                              str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()


def main(folder: Path):
    scan(folder)
    # MOVE FILES TO THE DESTINATION FOLDER BY FORMAT
    # IMAGES:
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    # VIDEO:
    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')
    # DOCUMENTS:
    for file in DOC_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in TXT_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in DOCX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in XLSX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in XLS_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'XLS')
    for file in PPT_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PPT')
    for file in PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PPTX')
    for file in PDF_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PDF')
    # AUDIO:
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')
    # ARCHIVES:
    for file in ZIP_ARCHIVES:
        handle_archive(file, folder / 'ZIP_ARCHIVES')
    for file in GZ_ARCHIVES:
        handle_archive(file, folder / 'GZ_ARCHIVES')
    for file in TAR_ARCHIVES:
        handle_archive(file, folder / 'TAR_ARCHIVES')
    # IMAGE:
    for file in ISO_IMAGE:
        handle_media(file, folder / 'image' / 'ISO')
    for file in IMG_IMAGE:
        handle_media(file, folder / 'image' / 'IMG')
    # MY OTHER FILES WITH NOT REGISTERED EXTENSIONS
    for file in MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')

    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')


def clean():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)
