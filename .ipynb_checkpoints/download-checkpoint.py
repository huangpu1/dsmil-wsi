import urllib.request
import argparse
from tqdm import tqdm
import zipfile
import shutil
import os


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)
        
def unzip_data(zip_path, data_path):
    if os.path.exists(data_path): shutil.rmtree(data_path) 
    os.mkdir(data_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(data_path)
    
        
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='mil', help='Dataset to be downloaded: mil, tcga')
    args = parser.parse_args()
    
    if args.dataset == "mil":
        print('downloading MIL benchmark datasets')
        download_url('https://uwmadison.box.com/shared/static/arvv7f1k8c2m8e2hugqltxgt9zbbpbh2.zip', 'mil-dataset.zip')
        unzip_data('mil-dataset.zip', 'datasets')
        os.remove('mil-dataset.zip')
    if args.dataset == "tcga":
        print('downloading TCGA Lung Cancer datasets (pre-computed features)')
        download_url('https://uwmadison.box.com/shared/static/tze4yqclajbdzjwxyb8b1umfwk9vcdwq.zip', 'tcga-dataset.zip')
        unzip_data('tcga-dataset.zip', 'datasets')
        os.remove('tcga-dataset.zip')
    
if __name__ == '__main__':
    main()