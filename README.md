# whatsapp-spam
This a Selenium and Django based automation project
To run this install python the run the command
! pip install -r requirement.txt
make sure to update chrome
then Download the chrome web driver from this link
# https://chromedriver.chromium.org/downloads
replace the folder directory with your directory of chromewebdriver inside views.py file inside app/ directory
run the command inside wap/ folder
! python manage.py runserver
a chrome popup will come login with your whatsapp
Enter the username (Case Sensitive)
wait until everything gets done
if it couldn't predict please try again by relogin with your whatsapp account
use these codes to relogin time to time use these codes inside views.py file inside app/ directory
# Windows
options.add_argument("C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default")
options.add_argument('--profile-directory=Default')

# Mac OS X El Capitan: 
options.add_argument('Users/<username>/Library/Application Support/Google/Chrome/Default')
  
# Linux: 
options.add_argument('/home/<username>/.config/google-chrome/default')

# If you're facing any problem please
  
  
