import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.firefox.options import Options
import json

import yaml

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# email credentials
conf = yaml.load(open('conf/application.yml'))
sender_id = conf['user']['email']
pwd = conf['user']['password']
receiver_email = "devwamaitha@gmail.com"




def Scrape():
  # selenium options

  title_arr = []
  country_arr = []
  all_obj = {}
  specific = {}


  options = Options()
  options.headless = True
  driver = webdriver.Firefox(options=options)

  #initiate
  driver.get("https://www.ungm.org/Shared/KnowledgeCenter/Pages/WFP")
  # driver.set_window_size(1880, 1049)


  # elements
  table = driver.find_elements_by_id("tblNotices")[0]
  tableBody = table.find_element_by_class_name('tableBody')
  tableRows = tableBody.find_elements_by_class_name('tableRow')



  for row in tableRows:
    all_obj.update({row.find_elements_by_class_name('tableCell')[7].find_element_by_tag_name('span').text:row.find_element_by_class_name('ungm-title').text})
    
    # country_arr.append(row.find_elements_by_class_name('tableCell')[7].find_element_by_tag_name('span').text)
    # title_arr.append(row.find_element_by_class_name('ungm-title').text)
    
  
  for item in all_obj.items():
    if 'Kenya' in all_obj.keys():
      specific.update({'Kenya':all_obj.get('Kenya')})
    
    if "Transport" in all_obj.values():
      specific.update({'Transport':all_obj.get('Transport')})

  

  # print("all objects ",all_obj)

  # print("specific is ,",specific)





  driver.close()

  return all_obj

# sendemail
def sendEmail():
  specific = {}
  message = MIMEMultipart("alternative")
  message["Subject"] = "UNITED NATIONS"
  message["From"] = sender_id
  message["To"] = receiver_email

  details = Scrape()
  print("details",details)


  if 'Kenya' in details.keys():
    specific.update({'Kenya':details.get('Kenya')})
  
  if "Transport" in details.values():
    specific.update({'Transport':details.get('Transport')})





  # Create the plain-text and HTML version of your message
  text = """\
  Hi,
  How are you?
  Real Python has many great tutorials:
  www.realpython.com"""
  html = """\
  
  <!doctype html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <title>For Edu or Org Design</title>
      <style>
          @media screen and (max-width: 600px) {
              .remove-flex-mobile {
                  display: block !important;
              }
              .remove-flex-basis-mobile {
                  flex-basis: unset !important;
                  padding-left: 0 !important;
              }
              .display-grid-mobile {
                  grid-template-columns: 1fr !important;
              }
              .reminders-list {
                  padding-left: 15px !important;
                  margin-top: 10px !important;
              }
              .reminders-table td {
                  float: unset !important;
                  display: block !important;
                  width: unset !important;
                  margin-left: 0 !important;
              }
              .second-item-order {
                  flex-direction: column !important;
                  align-items: flex-start !important;
              }
              .flex-order {
                  order: 2 !important;
              }
              .list-header {
                  padding-top: 20px !important;
              }
              .navigation-footer {
                  text-align: center !important;
              }
              .navigation-footer li {
                  display: list-item !important;
                  padding: 10px 0 !important;
              }
              .social-media img {
                  width: 30px !important;
              }
              .social-media a {
                  padding: 0 3px 0 0 !important;
              }
              .social-media a:last-of-type {
                  padding-right: 0 !important;
              }
          }
      </style>
  </head>
  <body style="margin:0;">
  <table style="border: none; margin: 0 auto ; padding: 0;">
      <tr>
          <td style="padding: 0; background-color: #FFFFFF;">
              <div style="max-width: 600px; min-width: 200px; font-family: 'Arial', sans-serif; font-size: 16px; background-color: #FFFFFF; line-height: 1.4; color: #4A4A4A; border: 1px solid #DFDFDF; border-radius: 10px; overflow: hidden;">
                  <div style="background-color: #76AEDC; height: 60px;">
                  </div>
            
                  <h2 style="font-size: 32px; padding: 30px 20px 0 20px; margin-bottom: 0; text-transform: uppercase; color: #4A4A4A;">UNITED NATIONS</h2>
                  <div style="padding: 0 20px;" ></div>
                  <p>These are all the tables </p>
                  <table style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
                      <tr>
                          <th>Country</th>
                            <th>Title</th>
                      </tr>
                      """
  for key,value in details.items():
    html = html + """ 
    <tr>
      <td>
          """ + key + """
      </td>
      <td>
      """ + value + """
      </td>

    </tr>"""
  html = html + """
                </table>

<p> These are the filtered results <p>
                  <table style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
                      <tr>
                          <th>Country</th>
                            <th>Title</th>
                      </tr>
                      """
  for key,value in specific.items():
    html = html + """ 
    <tr>
      <td>
          """ + key + """
      </td>
      <td>
      """ + value + """
      </td>

    </tr>"""
  html = html + """
                </table>
                
              <!-- START FOOTER -->
              <div class="footer" style="clear: both; Margin-top: 10px; text-align: center; width: 100%;">
                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
                     
                      <tr>
                          <td class="content-block powered-by" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; font-size: 12px; color: #999999; text-align: center;">
                              Powered by <a href="https://devngecuportfolio.netlify.app/" style="color: #999999; font-size: 12px;
                                  text-align: center; text-decoration: none;">Dev Ngecu</a>.
                          </td>
                      </tr>
                  </table>
              </div>
              <!-- END FOOTER -->
          </td>
      </tr>
  </table>
  </body>
  </html>
  """
  # Turn these into plain/html MIMEText objects
  part1 = MIMEText(text, "plain")
  part2 = MIMEText(html, "html")

  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(part1)
  message.attach(part2)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_id, pwd)
      server.sendmail(
          sender_id, receiver_email, message.as_string()
      )


sendEmail()






