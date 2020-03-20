from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import requests
import math
import pickle

class RateMyProfScraper:
        def __init__(self,schoolid):
            self.UniversityId = schoolid
            #self.professorlist = self.createprofessorlist()
            with open("gtcourseinfo\profList.pkl", 'rb') as pickle_file:
                content = pickle.load(pickle_file)
            self.professorlist = content
            self.indexnumber = False

        def createprofessorlist(self):#creates List object that include basic information on all Professors from the IDed University
            tempprofessorlist = []
            num_of_prof = self.GetNumOfProfessors(self.UniversityId)
            num_of_pages = math.ceil(num_of_prof / 20)
            i = 1
            
            while (i <= num_of_pages):# the loop insert all professor into list
                page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page=" + str(
                    i) + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                    self.UniversityId))
                temp_jsonpage = json.loads(page.content)
                temp_list = temp_jsonpage['professors']
                tempprofessorlist.extend(temp_list)
                i += 1
            #print(tempprofessorlist)
            return tempprofessorlist

        def GetNumOfProfessors(self,id):  # function returns the number of professors in the university of the given ID.
            page = requests.get(
                "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                    id))  # get request for page
            temp_jsonpage = json.loads(page.content)
            num_of_prof = temp_jsonpage[
                              'remaining'] + 20  # get the number of professors at Georgia Tech
            return num_of_prof

        def SearchProfessor(self, ProfessorName):
            self.indexnumber = self.GetProfessorIndex(ProfessorName)
            #self.PrintProfessorInfo()
            return self.indexnumber

        def GetProfessorIndex(self,ProfessorName):  # function searches for professor in list
            for i in range(0, len(self.professorlist)):
                if (ProfessorName == (self.professorlist[i]['tFname'] + " " + self.professorlist[i]['tLname'])):
                    return i
            return False  # Return False is not found

        def PrintProfessorInfo(self):  # print search professor's name and RMP score
            if self.indexnumber == False:
                print("error")
            else:
                print(self.professorlist[self.indexnumber])

        def PrintProfessorDetail(self,key):  # print search professor's name and RMP score
            if self.indexnumber == False:
                print("error")
                return "error"
            else:
                print(self.professorlist[self.indexnumber][key])
                return self.professorlist[self.indexnumber][key]

def nameFixer(inp):
    try:
        index = inp.index(",")
        name = inp[index + 2:] + " " + inp[0:index]
    except:
        return (inp)
    return name


def getInfoPro(course_code):
    #print("check")
    index = 0
    course_code = course_code.replace(" ", "")
    course_code = course_code.upper()
        
    

    url = "https://critique.gatech.edu/course.php?id="
    doc = requests.get(url + course_code)
    page = BeautifulSoup(doc.content, "html.parser")

    gpa = page.body.div.div.div.table.tbody.tr.find_all('td')[1].text

    #profs = page.body.div.find_all('div')[1].table.tbody.find_all('tr')

    #profs = page.body.div
    profs_list_temp = page.find_all("a")
    profs = []
    for i in range(1, 30):
        try:
            profs.append(profs_list_temp[i].text)
        except:
            break
    
    profs = profs[0:-3]


    for i in range(len(profs)):
        profs[i] = nameFixer(profs[i])

    gt = RateMyProfScraper(361)

    out = "Average GPA: " + gpa + "\n\n" + "RateMyProfessor.com Ratings: \n\n"
    for index in range(len(profs)):
        l = gt.SearchProfessor(nameFixer(profs[index]))
        if l != False:

            out += (gt.professorlist[l]['tFname']   + " "  +   gt.professorlist[l]['tLname']   + ": " +   gt.professorlist[l]['overall_rating'] + "\n")
        #else:
            #print(profs[index] + ": " + "No rating found")
    return (out)





# Create your views here.

def form(request):
    return render(request, "gtcourseinfo/form.html")

def result(request):
    coursename = request.GET["coursename"]
    res = getInfoPro(coursename)
    return render(request, "gtcourseinfo/result.html", {'result':res})
