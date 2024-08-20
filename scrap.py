import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.message import EmailMessage

# Retrieve environment variables for email credentials
email_id = os.getenv("EMAIL_ADDRESS")
email_pass = os.getenv("EMAIL_PASSWORD")

# Check if environment variables are set
if not email_id or not email_pass:
    raise ValueError("Email address or password environment variable not set.")

# URL of the product page to track
URL = "https://www.amazon.in/Apple-iPad-Pro-11%E2%80%B3-Landscape/dp/B0D3J5NGTQ/?_encoding=UTF8&pd_rd_w=PUDYv&content-id=amzn1.sym.b5a625fa-e3eb-4301-a9e2-f9c8b3e7badf%3Aamzn1.symc.36bd837a-d66d-47d1-8457-ffe9a9f3ddab&pf_rd_p=b5a625fa-e3eb-4301-a9e2-f9c8b3e7badf&pf_rd_r=37R9N8P4K61M3AB34A4A&pd_rd_wg=EfKv8&pd_rd_r=67ca2b2d-8ed9-4fd7-a2fd-5be206096c9d&ref_=pd_hp_d_btf_ci_mcx_mr_hp_atf_m"
def check_price():
    
    #Check the price of the product and send an email if the price is below a threshold.
    
    # Set headers to mimic a web browser
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

    # Send a request to the URL and parse the page content
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract the title of the product
    title = soup.find(class_="a-size-large product-title-word-break")
    title_text = title.get_text(strip=True) if title else "Title not found"

    # Extract the price of the product
    price = soup.find(class_="a-price-whole")
    if price:
        price_text = price.get_text(strip=True).replace(",", "")
        try:
            # Convert price to integer
            price_value = int(price_text)
        except ValueError:
            price_value = None
    else:
        price_text = "Price not found"
        price_value = None

    # Print the title and price
    print(title_text)
    print(price_text)

    # Check if the price is below the threshold and send an email if it is
    if price_value is not None and price_value < 119900:
        send_mail()

def send_mail():
    
    #Send an email notification about the price drop.
   
    msg = EmailMessage()
    msg['Subject'] = "Product price has decreased"
    msg['From'] = email_id
    msg['To'] = 'scp76971@gmail.com'  # Replace with your recipient email
    msg.set_content("Check out this amazon link: https://www.amazon.in/Apple-iPad-Pro-11%E2%80%B3-Landscape/dp/B0D3J5NGTQ/?_encoding=UTF8&pd_rd_w=PUDYv&content-id=amzn1.sym.b5a625fa-e3eb-4301-a9e2-f9c8b3e7badf%3Aamzn1.symc.36bd837a-d66d-47d1-8457-ffe9a9f3ddab&pf_rd_p=b5a625fa-e3eb-4301-a9e2-f9c8b3e7badf&pf_rd_r=37R9N8P4K61M3AB34A4A&pd_rd_wg=EfKv8&pd_rd_r=67ca2b2d-8ed9-4fd7-a2fd-5be206096c9d&ref_=pd_hp_d_btf_ci_mcx_mr_hp_atf_m")

    try:
        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_id, email_pass)
            smtp.send_message(msg)
            print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate with the SMTP server. Check your email and password.")
    except smtplib.SMTPConnectError:
        print("Failed to connect to the SMTP server. Check your network connection.")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

# Execute the price check function
check_price()
