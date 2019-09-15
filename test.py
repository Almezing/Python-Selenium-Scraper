import os


def download_info():
    download_path = "C:\\Users\\Almezing\\Downloads"
    download_file = ""
    row =3
    x = ['1','//*[@id="transaction-list-body"]' ]
    thing = f"{x[1]}/tr[{row}]/td[3]"
    print(thing)

    try:

        try:
            # TODO get latest file downloaded
            download_file = max(
                [file for file in os.listdir(download_path)],
                key=lambda xa: os.path.getctime(os.path.join(download_path, xa)),
            )

            print(download_file)
        except:
            print("Fail to download")
    except:
        print("Fail to get all info")
    return download_file


download_info()

