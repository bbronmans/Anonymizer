from pathlib import Path

from google_drive_downloader import GoogleDriveDownloader as gdd


WEIGHTS_GDRIVE_IDS = {
    '1.0.0': {
        'face': '1CwChAYxJo3mON6rcvXsl82FMSKj82vxF',
        'plate': '1Fls9FYlQdRlLAtw-GVS_ie1oQUYmci9g'
    }
}


def get_weights_path(base_path, kind, version='1.0.0'):
    assert version in WEIGHTS_GDRIVE_IDS.keys(), 'Invalid weights version "{}"'.format(version)
    assert kind in WEIGHTS_GDRIVE_IDS[version].keys(), 'Invalid weights kind "{}"'.format(kind)

    return str(Path(base_path) / 'weights_{}_v{}.pb'.format(kind, version))


def _download_single_model_weights(download_directory, kind, version):
    file_id = WEIGHTS_GDRIVE_IDS[version][kind]
    weights_path = get_weights_path(base_path=download_directory, kind=kind, version=version)
    if Path(weights_path).exists():
        return

    print('Downloading {} weights to {}'.format(kind, weights_path))
    gdd.download_file_from_google_drive(file_id=file_id, dest_path=weights_path, unzip=False)


def download_weights(download_directory, version='1.0.0'):
    for kind in ['face', 'plate']:
        _download_single_model_weights(download_directory=download_directory, kind=kind, version=version)
