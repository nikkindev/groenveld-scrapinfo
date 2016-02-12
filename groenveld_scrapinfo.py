import requests,getpass,re,sys,os

print 'This application will download the Groenveld residents info and store it locally\nEnter your groenveld user credentials to continue...\n'
USERNAME=raw_input('Enter your Groenveld username : ')
PASSWORD=getpass.getpass('Password (Your password will not be visible when you are typing): ')     #Password is shown as asterisk

with requests.Session() as c:
    url='http://groenveld.studentenweb.org/en/auth/'
    c.get(url)
    login_data=dict(username=USERNAME,password=PASSWORD,remember_me=1, submit='LOGIN')
    c.post(url, data=login_data)

    test=c.get('http://groenveld.studentenweb.org/en/user/residents/room/1-00-01')  #Tests if the credentials are right
    if len(test.history)!= 0:                                                       #Shows that there are no redirects
        print 'Your username or password is incorrect. The program is exiting.'
        sys.exit()

    os.makedirs('Groenveld_res_info')   #Makes a new directory
    os.makedirs('Groenveld_res_info/images')
    fhand=open('Groenveld_res_info/Residents_info.csv','w')
    fhand.write('Room,Name,Study,City,Birthday\n')
    count=1
    for blok in range(1,5):
        for floor in range(0,5):
            for room in range(1,17):
                url_segment=str(blok)+'-'+str(floor).zfill(2)+'-'+str(room).zfill(2)
                page = c.get('http://groenveld.studentenweb.org/en/user/residents/room/'+url_segment)
                name=re.findall('<h2>(.*)</h2>',page.content)
                study=re.findall('<span class="label">Study:</span> <span class="content">(.*)</span>',page.content) #Use regex to extract information
                city=re.findall('<span class="label">City:</span> <span class="content">(.*)</span>',page.content)
                birthday=re.findall('<span class="label">Birthday:</span> <span class="content">(.*)</span>',page.content)
                room_ext=str(blok)+'.'+str(floor).zfill(2)+'.'+str(room).zfill(2)
                fhand.write(room_ext+','+name[0]+',')
                if len(study)!=0:   fhand.write(study[0])   #Making sure that the list has an element to prevent index mismatch
                fhand.write(',')
                if len(city)!=0:    fhand.write(city[0])
                fhand.write(',')
                if len(birthday)!=0:    fhand.write(birthday[0])
                fhand.write('\n')                

                imgstr=re.findall('<img src="/en/account/profileimage/(.*)/" />',page.content)
                if len(imgstr)==1:  #To make sure that the following code is skipped when no image source is found
                    imgobj=c.get('http://groenveld.studentenweb.org/en/account/profileimage/'+imgstr[0])
                    img_name=room_ext+'_'+name[0]+'.jpg'             
                    out_img=open('Groenveld_res_info/images/'+img_name,'wb')    #Open the file to write binary information of image
                    out_img.write(imgobj.content)   #write the binary info of image
                    out_img.close()

                print 'Resident info retrieved...%d/320' %(count)
                count+=1

    print 'Sucessful!'
    fhand.close()
