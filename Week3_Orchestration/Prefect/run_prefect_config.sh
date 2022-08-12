prefect config view

### For Prefect ORION
prefect config unset PREFECT_API_URL
prefect config unset PREFECT_ORION_UI_API_URL

prefect config set PREFECT_ORION_UI_API_URL="https://18.132.192.14:4200/api" ### change external IP each time EC2 starts

prefect config set PREFECT_API_URL="https://18.132.192.14:4200/api"  ### change external IP each time EC2 starts

### For Prefect CLoud
prefect cloud login -k pnu_ZTVuCdWhovyAGiAJ3mGMQ9ucZpqZzX2uG2oI