
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import re


def extraire_email_rapide(html_of_):
    soup2 = BeautifulSoup(html_of_, "html.parser")

    #  Chercher les liens mailto
    mailtos = soup2.select('a[href^="mailto:"]')
    if mailtos:
        href = mailtos[0].get('href')
        if href:
            email = href.replace("mailto:", "").split("?")[0].strip()
            return email

    #  Chercher dans header, footer, et aussi les balises <p>, <div>, <span>
    sections = soup2.find_all(['header', 'footer', 'p', 'div', 'span'])
    for section in sections:
        text = section.get_text()
        match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        if match:
            return match.group(0).strip()

    # Chercher dans les mots-clés "contact", "recrutement"
    contact_sections = soup2.find_all(string=re.compile("(contact|recrutement)", re.I))
    for section in contact_sections:
        parent_text = section.parent.get_text()
        match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", parent_text)
        if match:
            return match.group(0).strip()

    #  Chercher partout dans le HTML (fallback)
    all_text = soup2.get_text()
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", all_text)
    if match:
        return match.group(0).strip()

    # Aucun email trouvé
    return None


def trouver_email(website_text, eemail_of_business):
    eemails = extraire_email_rapide(website_text)
    if eemails:
        print(" Email trouvé avec regex :", eemails)
        eemail_of_business.append(eemails)
        return eemails

    maail = "pas de site"
    eemail_of_business.append(maail)
    return maail



 #   else:
  #      return "pas d'adresses e-mail"


def go_to_website(website, page2):
    if website.startswith("http"):
        print("ca commence bien par http")

        page2.route("**/*", lambda route:
        route.abort() if route.request.resource_type in ["image", "stylesheet", "font"]
        else route.continue_()
                   )

        page2.goto(
            website,
            timeout=70000,
            wait_until="domcontentloaded"
        )
        print("html du site copié ")
        return page2.content()
    else:
        return None

def go_to_business(name_name_name, paaage) :

        try:
            paaage.get_by_role("link", name=name_name_name).first.click()
        except Exception as e:
          print(f"Erreur lors du chargement : {e}")
          return None

        else:
            paaage.wait_for_load_state("load")
            paaage.mouse.wheel(0, 2000)  # scroll vertical
            time.sleep(1)
            paaage.wait_for_load_state("load")
            paaage.mouse.wheel(0, 2000)  # scroll vertical
            time.sleep(1)
            paaage.wait_for_load_state("load")
            paaage.mouse.wheel(0, 2000)  # scroll vertical
            time.sleep(1)
            paaage.mouse.wheel(0, 2000)  # scroll vertical
            time.sleep(1)
            paaage.mouse.wheel(0, 2000)  # scroll vertical
            time.sleep(1)

            htmls = paaage.content()
            return htmls



def scrape_business(name0,html_of_another_page, paage, paage2, wwebsites_of_business, eemails, nnnumber_of_business,aadresses_of_business) :

    aaddress = []
    nuumbers = []
    i = 0
    j = 0

    soup1 = BeautifulSoup(html_of_another_page, "html.parser")

    all_info_button = soup1.find_all("button", class_="CsEnBe")
    for info in all_info_button :

          one_info = info.get("aria-label")
          if one_info.startswith("Adresse") :
              address_one = one_info.split("Adresse: ")[1].strip()
              aaddress.append(address_one)

              i+=1


          elif one_info.startswith("Numéro de téléphone") :
              number_one = one_info.split("Numéro de téléphone: ")[1].strip()
              nuumbers.append(number_one)

              j+=1

    if j==0 :
      nuumbers.append("pas de numero")

    if i==0  :
        aaddress.append("pas de localisation")

    element = paage.query_selector('a[data-item-id="authority"]')
    try:

       href = element.get_attribute('href')
    except AttributeError:
       href = "pas de site"
       wwebsites_of_business.append(href)
       pass
    else:

        wwebsites_of_business.append(href)
    html_website = go_to_website(href, paage2)

    if html_website is not None:
        email = trouver_email(html_website, eemails)
    else:
        email = "pas de mail"
    eemails.append(email)
    print("Email :")
    print(email)

    print("websites : ")
    print(href)
    print("Address : ")
    aadresses_of_business.append(aaddress)
    print(aaddress)
    nnnumber_of_business.append(nuumbers)
    print("numbers : ")
    print(nuumbers)
    entreprise = {
        'nom': name0,
        'telephone': nuumbers,
        'adresse': aaddress,
        'email': email,
        'website': href,
        'id': i + 1  # identifiant unique optionnel
    }
    return entreprise




def take_names_of_business(name_of_business_2, name_name_name):


    for name1 in name_of_business_2:
        try:
            name_of_business_2 = name1.get("aria-label")

        except AttributeError :
              continue
        else:
            name_name_name.append(name_of_business_2.strip())


    return name_name_name




def scroll(paage , endd_selector):
    """Scroll jusqu'à ce que le message de fin apparaisse."""
    end_selector = endd_selector
    max_scroll_attempts = 70 # sécurité pour éviter une boucle infinie

    for i in range(max_scroll_attempts):
        # Vérifier si l'élément de fin est déjà visible
        if paage.locator(end_selector).nth(-1).is_visible():
            print(" Fin de liste atteinte.")
            print(i)
            break

        # Scroller vers le bas
        paage.mouse.wheel(0, 2000)  # scroll vertical
        time.sleep(1)  # laisser le temps au contenu de charger

    else:
        print("⚠️ Nombre max de scroll atteint sans trouver la fin.")


def main(keywordd) :
    name_name =[]
    websites_of_business = []
    numbers_of_business = []
    addresses_of_business = []
    emails = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(
                "https://www.google.com/maps",
                timeout=70000,

            )

            print("Page chargée avec succès !")

        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
        else:

            page.get_by_role("combobox", name="Rechercher dans Google Maps").click()
            page.get_by_role("combobox", name="Rechercher dans Google Maps").fill(keywordd)
            page.get_by_role("button", name="Rechercher").click()

            page.wait_for_timeout(5000)
            page.get_by_role("heading", name="Résultats").click()
            scroll(page, "span.HlvSq")

            html = page.content()

            soup = BeautifulSoup(html, "html.parser")

            names_of_business_1 = soup.find_all("a", class_="hfpxzc")
            names = take_names_of_business(names_of_business_1, name_name)
            print( names)
            print(len( names))
            page1 = browser.new_page()
            entreprises = []
            for name in names:

                html_one_page = go_to_business(name, page)
                entreprise1 = scrape_business(name,html_one_page, page, page1, websites_of_business,emails, numbers_of_business,addresses_of_business )
                entreprises.append(entreprise1)
            print(entreprises)
            return entreprises




            ###print(all_name_of_business)


if __name__ == "__main__":
    keyword = input("quel type ?")
    main(keyword)