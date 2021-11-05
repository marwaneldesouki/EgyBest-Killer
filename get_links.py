import string
import random
import threading
from requests_toolbelt import MultipartEncoder
import re
from threading import Thread
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

global await_
movies = []
global movie_details
movie_details = ""
global series_details
series_details = ""

def ShowSuggestions(name):
    try:
        movies.clear()
        headers = {'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   'Sec-Fetch-Site': 'none',
                   'Sec-Fetch-Mode': 'navigate',
                   'Sec-Fetch-Dest': 'document',
                   'Accept-Language': 'en-US,en;q=0.9',}
        req = requests.get(
            f"https://grey.egybest.party/autoComplete.php?q={name}", headers=headers)
        response = req.text
        movie_namelink = f'"t":"(.*?)","u":"(.*?)","i'
        for found in re.finditer(movie_namelink, response):
            print(found)
            movies.append([found.group(1), found.group(2)])
        print(movies)
    except:
        print("Error in :ShowSuggestions")
    return movies


def get_MovieDetails(link):
    link = str(link).replace("\\", "")
    headers = {'Upgrade-Insecure-Requests': '1',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'sec-ch-ua-platform': '"Windows"',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Dest': 'document',
               'Accept-Language': 'en-US,en;q=0.9',
               'Cookie': 'b9bbed5c=TIIIcgeWbdMcIpsnlsssUEsIsnDEsrcIcwOVKIcIpIcHsVImUTadMcpcIcPOwIcIpIcdGodRCEGIshenlWwGsIcIl-e03bb6b7e9f54b639b148d758f919e86; JS_TIMEZONE_OFFSET=-7200; EGUDI=tWoqxusYASZ0yyO7.2d6a5a6c859e0ff242d56689cf5997e6657e568894ceca6b4eff64d85d9b3fb5fb7b6e465e9eba844d4c56b910cdb8ab9f1b383b3daedc136bab32dd26606f2f; 0399132e=OsssxiLFsxstsxzYUXxNOgduZEoTexFsxtxsxFLnmsxstsxDntrevNpeGaekDBDmOxKzEmsUgxtxsxQSUPDgxstEGCEEERxEsEGFFCsC-05f4f56f127c76cf238fb9a532bb5085; TIX34N1xK1LZWQaOn=80K7Jy4HwujLTAXwBUmuc6g32rVRbnml9D7edkflzC29Y3XBjG; 0ws9KhVwrS1EWR2fE=q58JE7qZyNUGWG2ftqv7EZvqwa71FZm7ZlQ5gGzk; daD7p2PnuwJMIt31T=GV6IZwrACpGCcsTQASd3qEFRfNK2SqEmDSFfSLtO9WiSIt0K6; 1mB9dcDaCyPpesB=VN1tlL7ulsq5rGlJiacNJxzbBUsXhaKjgHu6KG8pkh54PWeBJkl2QHVT6; 38DSzjDkXyRdVp8Kb=z4yXQc3uncdj9gmUGsM3Hgh5hInEbgIJKGtX03tQwz4aB8wIjP9EYVU; gojEfm1q2L0pchOVT1d=ySErAEFdFJDloTMOIqs1bEdFnW53cusvFwQyZTyrrMT3msue3uG7pHL0W; rfb0jbaWU57AUClo=chLU7nBbOFsHLjEvjRL3ErrMuLdHuDTN7PisRBFj3d5ydbwvebNOSYduvLW; fZKp4bsGdiMUnQZhwfHN=lmPs0s6wbXzWczlZjFh133zWu2maikgZK3YCG8AgMYTWKIoEindsckH; flwxRXZYP3K40CI=C572rJ2X1uzKU6oXHDT8oDdoy39OgD0PGVLnNMvxFn; push_subscribed=ignore; HHV7gHSzk84fb0hSH0=fRxxAv1aNg6LRrMGuwytwAgc45gLUeQPKWo0kNDTHhGKiNHjIjrFDiOI; PSSID=k9U-VAAZJHyb1Er7%2CloJsdAo2SZjrQnDtLvWo4gsX8muyw1FyUJblybSIV4GcXxM3qiM2VrAkWQNl8H6U0je43dm2CyKI8cSqS%2CvmYh-oyjhRrMdNYvxG35HOqdehW72'}
    req = requests.get(
        f"https://grey.egybest.party/{link}", headers=headers,verify=False)
    response = req.text
    global movie_details
    movie_details = ""
    movie_name_reg = f'<title>(.*?)</title>'
    movie_language_reg = f'">([^<]*)</a> &nbsp; &bull; &nbsp; <a'
    movie_category_reg = f'/">([^<]*)</a> &bull; <'
    movie_rating_reg = f'="ratingValue">(.*?)</span'
    movie_trailer_reg = f'" url="(.*?) data'
    movie_stream_reg = f'<iframe class="auto-size" src="(.*?)" allowfullscreen>'
    for found in re.finditer(movie_name_reg, response):
        movie_details = "MovieName: "+found.group(1)+"\n"
        for found2 in re.finditer(movie_language_reg, response):
            movie_details += "MovieLanguage: " + \
                found2.group(1)+"\nMovieCategory: "
            for found3 in re.finditer(movie_category_reg, response):
                movie_details += found3.group(1)+","
            movie_details = movie_details[:-1]
            for found4 in re.finditer(movie_rating_reg, response):
                movie_details += "\nMovieRating: "+found4.group(1)+"\n"
            for found5 in re.finditer(movie_trailer_reg, response):
                movie_details += "MovieTrailer: "+found5.group(1).replace('"','')+"\n"
            break
        for found6 in re.finditer(movie_stream_reg, response):
            print(found6.group(1))
            thread = threading.Thread(target=short_links(f"https://grey.egybest.party{found6.group(1)}","movie",0))
            thread.start()
            
    return movie_details


def get_dostream(link):
    headers = {'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Dest': 'document',
               'Accept-Language': 'en-US,en;q=0.9',
               'Cookie': 'b9bbed5c=TIIIcgeWbdMcIpsnlsssUEsIsnDEsrcIcwOVKIcIpIcHsVImUTadMcpcIcPOwIcIpIcdGodRCEGIshenlWwGsIcIl-e03bb6b7e9f54b639b148d758f919e86; JS_TIMEZONE_OFFSET=-7200; EGUDI=tWoqxusYASZ0yyO7.2d6a5a6c859e0ff242d56689cf5997e6657e568894ceca6b4eff64d85d9b3fb5fb7b6e465e9eba844d4c56b910cdb8ab9f1b383b3daedc136bab32dd26606f2f; 0399132e=OsssxiLFsxstsxzYUXxNOgduZEoTexFsxtxsxFLnmsxstsxDntrevNpeGaekDBDmOxKzEmsUgxtxsxQSUPDgxstEGCEEERxEsEGFFCsC-05f4f56f127c76cf238fb9a532bb5085; TIX34N1xK1LZWQaOn=80K7Jy4HwujLTAXwBUmuc6g32rVRbnml9D7edkflzC29Y3XBjG; 0ws9KhVwrS1EWR2fE=q58JE7qZyNUGWG2ftqv7EZvqwa71FZm7ZlQ5gGzk; daD7p2PnuwJMIt31T=GV6IZwrACpGCcsTQASd3qEFRfNK2SqEmDSFfSLtO9WiSIt0K6; 1mB9dcDaCyPpesB=VN1tlL7ulsq5rGlJiacNJxzbBUsXhaKjgHu6KG8pkh54PWeBJkl2QHVT6; 38DSzjDkXyRdVp8Kb=z4yXQc3uncdj9gmUGsM3Hgh5hInEbgIJKGtX03tQwz4aB8wIjP9EYVU; gojEfm1q2L0pchOVT1d=ySErAEFdFJDloTMOIqs1bEdFnW53cusvFwQyZTyrrMT3msue3uG7pHL0W; rfb0jbaWU57AUClo=chLU7nBbOFsHLjEvjRL3ErrMuLdHuDTN7PisRBFj3d5ydbwvebNOSYduvLW; fZKp4bsGdiMUnQZhwfHN=lmPs0s6wbXzWczlZjFh133zWu2maikgZK3YCG8AgMYTWKIoEindsckH; flwxRXZYP3K40CI=C572rJ2X1uzKU6oXHDT8oDdoy39OgD0PGVLnNMvxFn; push_subscribed=ignore; PSSID=kDVtfOLIn5LyRpgfWTQpeyxbB7m0sfpxr3iRcRyswIGFzn1geWh0EhtJI5OmCaufwZ%2CzWNMp211c-ynNUNe7JnJycWRPuhEGO9t9e2XKXPI32AcAKB8EtA28bRubVsgs; HHV7gHSzk84fb0hSH0=fRxxAv1aNg6LRrMGuwytwAgc45gLUeQPKWo0kNDTHhGKiNHjIjrFDiOI'}
    req = requests.get(
        f"https://cola.egybest.guru{link}", headers=headers, verify=False)
    response = req.text
    movie_stream_reg = f'<source src="(.*?)" type="'
    for found in re.finditer(movie_stream_reg, response):
        thread = threading.Thread(target=get_Links(found.group(1)))
        thread.start()


def get_Links(link):
    headers = {'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Dest': 'document',
               'Accept-Language': 'en-US,en;q=0.9',
               'Cookie': 'b9bbed5c=TIIIcgeWbdMcIpsnlsssUEsIsnDEsrcIcwOVKIcIpIcHsVImUTadMcpcIcPOwIcIpIcdGodRCEGIshenlWwGsIcIl-e03bb6b7e9f54b639b148d758f919e86; JS_TIMEZONE_OFFSET=-7200; EGUDI=tWoqxusYASZ0yyO7.2d6a5a6c859e0ff242d56689cf5997e6657e568894ceca6b4eff64d85d9b3fb5fb7b6e465e9eba844d4c56b910cdb8ab9f1b383b3daedc136bab32dd26606f2f; 0399132e=OsssxiLFsxstsxzYUXxNOgduZEoTexFsxtxsxFLnmsxstsxDntrevNpeGaekDBDmOxKzEmsUgxtxsxQSUPDgxstEGCEEERxEsEGFFCsC-05f4f56f127c76cf238fb9a532bb5085; TIX34N1xK1LZWQaOn=80K7Jy4HwujLTAXwBUmuc6g32rVRbnml9D7edkflzC29Y3XBjG; 0ws9KhVwrS1EWR2fE=q58JE7qZyNUGWG2ftqv7EZvqwa71FZm7ZlQ5gGzk; daD7p2PnuwJMIt31T=GV6IZwrACpGCcsTQASd3qEFRfNK2SqEmDSFfSLtO9WiSIt0K6; 1mB9dcDaCyPpesB=VN1tlL7ulsq5rGlJiacNJxzbBUsXhaKjgHu6KG8pkh54PWeBJkl2QHVT6; 38DSzjDkXyRdVp8Kb=z4yXQc3uncdj9gmUGsM3Hgh5hInEbgIJKGtX03tQwz4aB8wIjP9EYVU; gojEfm1q2L0pchOVT1d=ySErAEFdFJDloTMOIqs1bEdFnW53cusvFwQyZTyrrMT3msue3uG7pHL0W; rfb0jbaWU57AUClo=chLU7nBbOFsHLjEvjRL3ErrMuLdHuDTN7PisRBFj3d5ydbwvebNOSYduvLW; fZKp4bsGdiMUnQZhwfHN=lmPs0s6wbXzWczlZjFh133zWu2maikgZK3YCG8AgMYTWKIoEindsckH; flwxRXZYP3K40CI=C572rJ2X1uzKU6oXHDT8oDdoy39OgD0PGVLnNMvxFn; push_subscribed=ignore; PSSID=kDVtfOLIn5LyRpgfWTQpeyxbB7m0sfpxr3iRcRyswIGFzn1geWh0EhtJI5OmCaufwZ%2CzWNMp211c-ynNUNe7JnJycWRPuhEGO9t9e2XKXPI32AcAKB8EtA28bRubVsgs; HHV7gHSzk84fb0hSH0=fRxxAv1aNg6LRrMGuwytwAgc45gLUeQPKWo0kNDTHhGKiNHjIjrFDiOI'}

    req = requests.get(
        f"https://cola.egybest.guru{link}", headers=headers, verify=False)
    response = req.text
    movie_watch_reg = f'"\n(.*?)/stream.m3u8'
    for found in re.finditer(movie_watch_reg, response):
        strlink = found.group(1).replace("/stream/", "/watch/")
        thread = threading.Thread(target=short_links(strlink))
        thread.start()


def short_links(link,type,series_num):
    fields = {
        'url': (link),
        'domain': ('0'),
    }
    boundary = '----WebKitFormBoundary' \
        + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    m = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {'Host': 'cutt.ly',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept': '*/*',
               'Connection': 'keep-alive',
               'Content-Length': '845',
               'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
               'DNT': '1',
               'sec-ch-ua-mobile': '?0',
               'X-Bitly-Client': 'bbt2',
               "Content-Type": m.content_type,
               'sec-ch-ua-platform': '"Windows"',
               'Sec-Fetch-Site': 'same-origin',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Dest': 'empty',
               'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
               'Cookie': '_ga=GA1.2.1871486983.1633045811; _gid=GA1.2.454471168.1633045811; PHPSESSID=10vhjqebe90n0km11i7fa63mjk; _gat_gtag_UA_112763434_1=1; cookies_accepted=T',

               }
    req = requests.post(f"https://cutt.ly/scripts/shortenUrl.php",
                        headers=headers, verify=False, data=m)
    response = req.text
    global movie_details
    global series_details
    if(type == "movie"):
      movie_details += '[+]Link:'+response+'\n'
    else:
      series_details += f"[+]Episode_{series_num}:{response}\n"

# 3


def get_SeriesDetails(link):
    link = str(link).replace("\\", "")
    headers = {'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Dest': 'document',
               'Accept-Language': 'en-US,en;q=0.9',
               'Cookie': 'b9bbed5c=TIIIcgeWbdMcIpsnlsssUEsIsnDEsrcIcwOVKIcIpIcHsVImUTadMcpcIcPOwIcIpIcdGodRCEGIshenlWwGsIcIl-e03bb6b7e9f54b639b148d758f919e86; JS_TIMEZONE_OFFSET=-7200; EGUDI=tWoqxusYASZ0yyO7.2d6a5a6c859e0ff242d56689cf5997e6657e568894ceca6b4eff64d85d9b3fb5fb7b6e465e9eba844d4c56b910cdb8ab9f1b383b3daedc136bab32dd26606f2f; 0399132e=OsssxiLFsxstsxzYUXxNOgduZEoTexFsxtxsxFLnmsxstsxDntrevNpeGaekDBDmOxKzEmsUgxtxsxQSUPDgxstEGCEEERxEsEGFFCsC-05f4f56f127c76cf238fb9a532bb5085; TIX34N1xK1LZWQaOn=80K7Jy4HwujLTAXwBUmuc6g32rVRbnml9D7edkflzC29Y3XBjG; 0ws9KhVwrS1EWR2fE=q58JE7qZyNUGWG2ftqv7EZvqwa71FZm7ZlQ5gGzk; daD7p2PnuwJMIt31T=GV6IZwrACpGCcsTQASd3qEFRfNK2SqEmDSFfSLtO9WiSIt0K6; 1mB9dcDaCyPpesB=VN1tlL7ulsq5rGlJiacNJxzbBUsXhaKjgHu6KG8pkh54PWeBJkl2QHVT6; 38DSzjDkXyRdVp8Kb=z4yXQc3uncdj9gmUGsM3Hgh5hInEbgIJKGtX03tQwz4aB8wIjP9EYVU; gojEfm1q2L0pchOVT1d=ySErAEFdFJDloTMOIqs1bEdFnW53cusvFwQyZTyrrMT3msue3uG7pHL0W; rfb0jbaWU57AUClo=chLU7nBbOFsHLjEvjRL3ErrMuLdHuDTN7PisRBFj3d5ydbwvebNOSYduvLW; fZKp4bsGdiMUnQZhwfHN=lmPs0s6wbXzWczlZjFh133zWu2maikgZK3YCG8AgMYTWKIoEindsckH; flwxRXZYP3K40CI=C572rJ2X1uzKU6oXHDT8oDdoy39OgD0PGVLnNMvxFn; push_subscribed=ignore; PSSID=kDVtfOLIn5LyRpgfWTQpeyxbB7m0sfpxr3iRcRyswIGFzn1geWh0EhtJI5OmCaufwZ%2CzWNMp211c-ynNUNe7JnJycWRPuhEGO9t9e2XKXPI32AcAKB8EtA28bRubVsgs; HHV7gHSzk84fb0hSH0=fRxxAv1aNg6LRrMGuwytwAgc45gLUeQPKWo0kNDTHhGKiNHjIjrFDiOI'}

    req = requests.get(
        f"https://cola.egybest.guru/{link}", headers=headers, verify=False)
    response = req.text
    global series_details
    series_details = ""
    series_name_reg = f'<title>(.*?)</title>'
    series_language_reg = f'">([^<]*)</a> &nbsp; &bull; &nbsp; <a'
    series_category_reg = f'/">([^<]*)</a> &bull; <'
    series_rating_reg = f'="ratingValue">(.*?)</span'
    series_trailer_reg = f'" url="(.*?) data'
    series_season_reg = '<a href="([^<]*)" class="movie">'

    for found in re.finditer(series_name_reg, response):
        series_details = "seriesName: "+found.group(1)+"\n"
        for found2 in re.finditer(series_language_reg, response):
            series_details += "seriesLanguage: " + \
                found2.group(1)+"\nseriesCategory: "
            for found3 in re.finditer(series_category_reg, response):
                series_details += found3.group(1)+","
            series_details = series_details[:-1]
            for found4 in re.finditer(series_rating_reg, response):
                series_details += "\nseriesRating: "+found4.group(1)+"\n"
            for found5 in re.finditer(series_trailer_reg, response):
                series_details += "seriesTrailer: "+found5.group(1)+"\n"
            break
        for found6 in re.finditer(series_season_reg, response):
            last = found6.group(1)[-2]
            break
        last2 = last
        while(last2 != 0):
            series_details += "Season"+str(last)+"\n"
            get_episodeslinks(found6.group(1)[:-2]+str(last2))
            last2 = int(last2)-1

    return series_details


def get_episodeslinks(link):
    link = str(link).replace("\\", "")
    headers = {'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Dest': 'document',
               'Accept-Language': 'en-US,en;q=0.9',
               'Cookie': 'b9bbed5c=TIIIcgeWbdMcIpsnlsssUEsIsnDEsrcIcwOVKIcIpIcHsVImUTadMcpcIcPOwIcIpIcdGodRCEGIshenlWwGsIcIl-e03bb6b7e9f54b639b148d758f919e86; JS_TIMEZONE_OFFSET=-7200; EGUDI=tWoqxusYASZ0yyO7.2d6a5a6c859e0ff242d56689cf5997e6657e568894ceca6b4eff64d85d9b3fb5fb7b6e465e9eba844d4c56b910cdb8ab9f1b383b3daedc136bab32dd26606f2f; 0399132e=OsssxiLFsxstsxzYUXxNOgduZEoTexFsxtxsxFLnmsxstsxDntrevNpeGaekDBDmOxKzEmsUgxtxsxQSUPDgxstEGCEEERxEsEGFFCsC-05f4f56f127c76cf238fb9a532bb5085; TIX34N1xK1LZWQaOn=80K7Jy4HwujLTAXwBUmuc6g32rVRbnml9D7edkflzC29Y3XBjG; 0ws9KhVwrS1EWR2fE=q58JE7qZyNUGWG2ftqv7EZvqwa71FZm7ZlQ5gGzk; daD7p2PnuwJMIt31T=GV6IZwrACpGCcsTQASd3qEFRfNK2SqEmDSFfSLtO9WiSIt0K6; 1mB9dcDaCyPpesB=VN1tlL7ulsq5rGlJiacNJxzbBUsXhaKjgHu6KG8pkh54PWeBJkl2QHVT6; 38DSzjDkXyRdVp8Kb=z4yXQc3uncdj9gmUGsM3Hgh5hInEbgIJKGtX03tQwz4aB8wIjP9EYVU; gojEfm1q2L0pchOVT1d=ySErAEFdFJDloTMOIqs1bEdFnW53cusvFwQyZTyrrMT3msue3uG7pHL0W; rfb0jbaWU57AUClo=chLU7nBbOFsHLjEvjRL3ErrMuLdHuDTN7PisRBFj3d5ydbwvebNOSYduvLW; fZKp4bsGdiMUnQZhwfHN=lmPs0s6wbXzWczlZjFh133zWu2maikgZK3YCG8AgMYTWKIoEindsckH; flwxRXZYP3K40CI=C572rJ2X1uzKU6oXHDT8oDdoy39OgD0PGVLnNMvxFn; push_subscribed=ignore; PSSID=kDVtfOLIn5LyRpgfWTQpeyxbB7m0sfpxr3iRcRyswIGFzn1geWh0EhtJI5OmCaufwZ%2CzWNMp211c-ynNUNe7JnJycWRPuhEGO9t9e2XKXPI32AcAKB8EtA28bRubVsgs; HHV7gHSzk84fb0hSH0=fRxxAv1aNg6LRrMGuwytwAgc45gLUeQPKWo0kNDTHhGKiNHjIjrFDiOI'}
    series_episode_reg = '<a href="([^<]*)" class="movie"><span class="r"><i class="i-fav rating"><i>(.*?)</i></'
    req = requests.get(f"{link}", headers=headers, verify=False)
    response = req.text
    for found in re.finditer(series_episode_reg, response):
        series_num = found.group(1)[-2]
        get_series_watch(found.group(1),series_num)


def get_series_watch(link,series_num):
    headers = {'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Dest': 'document',
               'Accept-Language': 'en-US,en;q=0.9',
               'Cookie': 'b9bbed5c=TIIIcgeWbdMcIpsnlsssUEsIsnDEsrcIcwOVKIcIpIcHsVImUTadMcpcIcPOwIcIpIcdGodRCEGIshenlWwGsIcIl-e03bb6b7e9f54b639b148d758f919e86; JS_TIMEZONE_OFFSET=-7200; EGUDI=tWoqxusYASZ0yyO7.2d6a5a6c859e0ff242d56689cf5997e6657e568894ceca6b4eff64d85d9b3fb5fb7b6e465e9eba844d4c56b910cdb8ab9f1b383b3daedc136bab32dd26606f2f; 0399132e=OsssxiLFsxstsxzYUXxNOgduZEoTexFsxtxsxFLnmsxstsxDntrevNpeGaekDBDmOxKzEmsUgxtxsxQSUPDgxstEGCEEERxEsEGFFCsC-05f4f56f127c76cf238fb9a532bb5085; TIX34N1xK1LZWQaOn=80K7Jy4HwujLTAXwBUmuc6g32rVRbnml9D7edkflzC29Y3XBjG; 0ws9KhVwrS1EWR2fE=q58JE7qZyNUGWG2ftqv7EZvqwa71FZm7ZlQ5gGzk; daD7p2PnuwJMIt31T=GV6IZwrACpGCcsTQASd3qEFRfNK2SqEmDSFfSLtO9WiSIt0K6; 1mB9dcDaCyPpesB=VN1tlL7ulsq5rGlJiacNJxzbBUsXhaKjgHu6KG8pkh54PWeBJkl2QHVT6; 38DSzjDkXyRdVp8Kb=z4yXQc3uncdj9gmUGsM3Hgh5hInEbgIJKGtX03tQwz4aB8wIjP9EYVU; gojEfm1q2L0pchOVT1d=ySErAEFdFJDloTMOIqs1bEdFnW53cusvFwQyZTyrrMT3msue3uG7pHL0W; rfb0jbaWU57AUClo=chLU7nBbOFsHLjEvjRL3ErrMuLdHuDTN7PisRBFj3d5ydbwvebNOSYduvLW; fZKp4bsGdiMUnQZhwfHN=lmPs0s6wbXzWczlZjFh133zWu2maikgZK3YCG8AgMYTWKIoEindsckH; flwxRXZYP3K40CI=C572rJ2X1uzKU6oXHDT8oDdoy39OgD0PGVLnNMvxFn; push_subscribed=ignore; PSSID=kDVtfOLIn5LyRpgfWTQpeyxbB7m0sfpxr3iRcRyswIGFzn1geWh0EhtJI5OmCaufwZ%2CzWNMp211c-ynNUNe7JnJycWRPuhEGO9t9e2XKXPI32AcAKB8EtA28bRubVsgs; HHV7gHSzk84fb0hSH0=fRxxAv1aNg6LRrMGuwytwAgc45gLUeQPKWo0kNDTHhGKiNHjIjrFDiOI'}
    req = requests.get(f"{link}", headers=headers, verify=False)
    response = req.text
    movie_stream_reg = f'class="auto-size" src="(.*?)" allowfullscreen'
    for found in re.finditer(movie_stream_reg, response):
        thread = threading.Thread(target=short_links(f"https://cola.egybest.guru{found.group(1)}","series",series_num))
        thread.start()


def get_series_dostream(link):
    headers = {'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Dest': 'document',
               'Accept-Language': 'en-US,en;q=0.9',
               'Cookie': 'b9bbed5c=TIIIcgeWbdMcIpsnlsssUEsIsnDEsrcIcwOVKIcIpIcHsVImUTadMcpcIcPOwIcIpIcdGodRCEGIshenlWwGsIcIl-e03bb6b7e9f54b639b148d758f919e86; JS_TIMEZONE_OFFSET=-7200; EGUDI=tWoqxusYASZ0yyO7.2d6a5a6c859e0ff242d56689cf5997e6657e568894ceca6b4eff64d85d9b3fb5fb7b6e465e9eba844d4c56b910cdb8ab9f1b383b3daedc136bab32dd26606f2f; 0399132e=OsssxiLFsxstsxzYUXxNOgduZEoTexFsxtxsxFLnmsxstsxDntrevNpeGaekDBDmOxKzEmsUgxtxsxQSUPDgxstEGCEEERxEsEGFFCsC-05f4f56f127c76cf238fb9a532bb5085; TIX34N1xK1LZWQaOn=80K7Jy4HwujLTAXwBUmuc6g32rVRbnml9D7edkflzC29Y3XBjG; 0ws9KhVwrS1EWR2fE=q58JE7qZyNUGWG2ftqv7EZvqwa71FZm7ZlQ5gGzk; daD7p2PnuwJMIt31T=GV6IZwrACpGCcsTQASd3qEFRfNK2SqEmDSFfSLtO9WiSIt0K6; 1mB9dcDaCyPpesB=VN1tlL7ulsq5rGlJiacNJxzbBUsXhaKjgHu6KG8pkh54PWeBJkl2QHVT6; 38DSzjDkXyRdVp8Kb=z4yXQc3uncdj9gmUGsM3Hgh5hInEbgIJKGtX03tQwz4aB8wIjP9EYVU; gojEfm1q2L0pchOVT1d=ySErAEFdFJDloTMOIqs1bEdFnW53cusvFwQyZTyrrMT3msue3uG7pHL0W; rfb0jbaWU57AUClo=chLU7nBbOFsHLjEvjRL3ErrMuLdHuDTN7PisRBFj3d5ydbwvebNOSYduvLW; fZKp4bsGdiMUnQZhwfHN=lmPs0s6wbXzWczlZjFh133zWu2maikgZK3YCG8AgMYTWKIoEindsckH; flwxRXZYP3K40CI=C572rJ2X1uzKU6oXHDT8oDdoy39OgD0PGVLnNMvxFn; push_subscribed=ignore; PSSID=kDVtfOLIn5LyRpgfWTQpeyxbB7m0sfpxr3iRcRyswIGFzn1geWh0EhtJI5OmCaufwZ%2CzWNMp211c-ynNUNe7JnJycWRPuhEGO9t9e2XKXPI32AcAKB8EtA28bRubVsgs; HHV7gHSzk84fb0hSH0=fRxxAv1aNg6LRrMGuwytwAgc45gLUeQPKWo0kNDTHhGKiNHjIjrFDiOI'}
    req = requests.get(
        f"https://cola.egybest.guru{link}", headers=headers, verify=False)
    response = req.text
    movie_stream_reg = f'<source src="(.*?)" type="'
    for found in re.finditer(movie_stream_reg, response):
        get_series_Links(found.group(1))


def get_series_Links(link):
    headers = {'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Dest': 'document',
               'Accept-Language': 'en-US,en;q=0.9',
               'Cookie': 'b9bbed5c=TIIIcgeWbdMcIpsnlsssUEsIsnDEsrcIcwOVKIcIpIcHsVImUTadMcpcIcPOwIcIpIcdGodRCEGIshenlWwGsIcIl-e03bb6b7e9f54b639b148d758f919e86; JS_TIMEZONE_OFFSET=-7200; EGUDI=tWoqxusYASZ0yyO7.2d6a5a6c859e0ff242d56689cf5997e6657e568894ceca6b4eff64d85d9b3fb5fb7b6e465e9eba844d4c56b910cdb8ab9f1b383b3daedc136bab32dd26606f2f; 0399132e=OsssxiLFsxstsxzYUXxNOgduZEoTexFsxtxsxFLnmsxstsxDntrevNpeGaekDBDmOxKzEmsUgxtxsxQSUPDgxstEGCEEERxEsEGFFCsC-05f4f56f127c76cf238fb9a532bb5085; TIX34N1xK1LZWQaOn=80K7Jy4HwujLTAXwBUmuc6g32rVRbnml9D7edkflzC29Y3XBjG; 0ws9KhVwrS1EWR2fE=q58JE7qZyNUGWG2ftqv7EZvqwa71FZm7ZlQ5gGzk; daD7p2PnuwJMIt31T=GV6IZwrACpGCcsTQASd3qEFRfNK2SqEmDSFfSLtO9WiSIt0K6; 1mB9dcDaCyPpesB=VN1tlL7ulsq5rGlJiacNJxzbBUsXhaKjgHu6KG8pkh54PWeBJkl2QHVT6; 38DSzjDkXyRdVp8Kb=z4yXQc3uncdj9gmUGsM3Hgh5hInEbgIJKGtX03tQwz4aB8wIjP9EYVU; gojEfm1q2L0pchOVT1d=ySErAEFdFJDloTMOIqs1bEdFnW53cusvFwQyZTyrrMT3msue3uG7pHL0W; rfb0jbaWU57AUClo=chLU7nBbOFsHLjEvjRL3ErrMuLdHuDTN7PisRBFj3d5ydbwvebNOSYduvLW; fZKp4bsGdiMUnQZhwfHN=lmPs0s6wbXzWczlZjFh133zWu2maikgZK3YCG8AgMYTWKIoEindsckH; flwxRXZYP3K40CI=C572rJ2X1uzKU6oXHDT8oDdoy39OgD0PGVLnNMvxFn; push_subscribed=ignore; PSSID=kDVtfOLIn5LyRpgfWTQpeyxbB7m0sfpxr3iRcRyswIGFzn1geWh0EhtJI5OmCaufwZ%2CzWNMp211c-ynNUNe7JnJycWRPuhEGO9t9e2XKXPI32AcAKB8EtA28bRubVsgs; HHV7gHSzk84fb0hSH0=fRxxAv1aNg6LRrMGuwytwAgc45gLUeQPKWo0kNDTHhGKiNHjIjrFDiOI'}

    req = requests.get(
        f"https://cola.egybest.guru{link}", headers=headers, verify=False)
    response = req.text
    movie_watch_reg = f'"\n(.*?)/stream.m3u8'
    for found in re.finditer(movie_watch_reg, response):
        strlink = found.group(1).replace("/stream/", "/watch/")
        short_links(strlink)

thread = threading.Thread(target=print(get_MovieDetails("movie/the-egyptian-1954")))
thread.start()
#thread = threading.Thread(target=print(get_SeriesDetails("series/squid-game")))
#thread.start()


######################################################
