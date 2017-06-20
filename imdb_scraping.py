from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.error
import re

pg_error=False
page_cnt=1

file_name = "movie_details.csv"
while (pg_error==False):


	page_url="http://www.imdb.com/search/title?genres=action&title_type=feature&sort=moviemeter,asc&page=" + str(page_cnt)
	page_cnt = page_cnt + 1
	try:
		imdb_conn=urlopen(page_url)
		imdb_movies_html=imdb_conn.read()
		imdb_conn.close()
	except urllib.error.HTTPError:
		print("Page Not found")
		pg_error=True
		break

	soup = BeautifulSoup(imdb_movies_html, "lxml")

	pg_error = soup.find_all('div', {"class":"error_code_404"})

	if (len(pg_error)==0):
		
		movie_list = soup.find_all('div', {"class":"lister-item mode-advanced"})

		for each_movie in movie_list:
			movie_details = each_movie.find_all('h3',{"class":"lister-item-header"})

			movie_title=movie_details[0].a.string

			try:
				mv_year=movie_details[0].find_all('span',{"class":"lister-item-year text-muted unbold"})[0].string
				mv_year= int(re.findall(r'\d+', mv_year)[0])

			except:
				mv_year=""

			try:
				mv_crtfct=each_movie.find_all('span',{"class":"certificate"})[0].string
			except IndexError:
				mv_crtfct=""

			try:
				mv_len=each_movie.find_all('span',{"class":"runtime"})[0].string
			except IndexError:
				mv_len=""

			try:
				mv_gnr=each_movie.find_all('span',{"class":"genre"})[0].string
			except IndexError:
				mv_gnr=""

			try:
				mv_rating=each_movie.find_all('meta',{"itemprop":"ratingValue"})[0]["content"]
			except IndexError:
				mv_rating=""

			try:
				mv_no_of_rating=each_movie.find_all('meta',{"itemprop":"ratingCount"})[0]["content"]
			except IndexError:
				mv_no_of_rating=""	

			mv_cntnt=each_movie.find_all('div',{"class":"lister-item-content"})

			mv_plot=mv_cntnt[0].find_all('p',{"class":"text-muted"})[1].text

			mv_cast=mv_cntnt[0].find_all('p',)[2]
			mv_dirs=[]
			mv_strs=[]
			for link in mv_cast.find_all('a'):
				if (link.get('href').find('_dr_')>0):
					mv_dirs.append(link.string)
				elif (link.get('href').find('_st_')>0):
					mv_strs.append(link.string)
				else:
					print("no dir/stars:" + link)

			try:
				movie_gross=each_movie.find_all('span',{"name":"nv"})[1]["data-value"]

			except:
				movie_gross=''

			try:
				with open(file_name,'a') as file_open:
					print(movie_title.replace(',', '%') + ',' + str(mv_year) + ',' + mv_crtfct + ',' + mv_len + ',' + mv_gnr.replace(',', '|').strip() + ',' + mv_rating + ',' + mv_no_of_rating + ',' + mv_plot.replace(',','%').strip() + ',' + '|'.join(mv_dirs) + ',' + '|'.join(mv_strs) + ',' + movie_gross.replace(',',''), file=file_open)

			except:
				print(movie_title + ',' + str(mv_year) + ',' + mv_crtfct + ',' + mv_len + ',' + mv_gnr + ',' + mv_rating + ',' + mv_no_of_rating + ',' + str(mv_plot) + ',' + str('|'.join(mv_dirs)) + ',' + str('|'.join(mv_strs)))

	else :
		print("Further Page Not found. Scraping done.")