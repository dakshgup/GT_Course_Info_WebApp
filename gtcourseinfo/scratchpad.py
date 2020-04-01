import requests
from bs4 import BeautifulSoup
course_code = "CS1301"
for i in range(len(course_code)):
    if course_code[i].isdigit():
        num_index = i
        break
#CS1301
sub = course_code[0:num_index]
num = course_code[num_index:]


cat_url = "https://oscar.gatech.edu/pls/bprod/bwckctlg.p_disp_course_detail?cat_term_in=202008&subj_code_in=" + sub + "&crse_numb_in=" + num

doc = requests.get(cat_url)
cat_page = BeautifulSoup(doc.content, "html.parser")
short_des = cat_page.find_all(class_="nttitle")[0].text
long_des = cat_page.find_all(class_="ntdefault")[0].text

#long_des = cat_page.body.find_all('div')[2].table.tbody.find_all('tr')[1].td.text

print(short_des)
print(long_des)