from tqdm import tqdm
import requests

files = [("Average-prices-2022-05.csv", "."), ("Average-prices-2022-05.csv", "./evidently_service/datasets")]

print(f"Download files:")
for file, path in files:
    url = f"http://publicdata.landregistry.gov.uk/market-trend-data/house-price-index-data/Average-prices-2022-05.csv?utm_medium=GOV.UK&utm_source=datadownload&utm_campaign=average_price&utm_term=9.30_20_07_22"
    resp = requests.get(url, stream=True)
    save_path = f"{path}/{file}"
    with open(save_path, "wb") as handle:
        for data in tqdm(resp.iter_content(),
                         desc=f"{file}",
                         postfix=f"save to {save_path}",
                         total=int(resp.headers["Content-Length"])):
            handle.write(data)