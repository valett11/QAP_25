import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('c:\chromedriver\chromedriver.exe')
   #неявное ожидание
   pytest.driver.implicitly_wait(10)
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()


def test_show_my_pets():
   # Вводим email
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'email')))
   pytest.driver.find_element(By.ID, 'email').send_keys('pvy_84@mail.ru')
   # Вводим пароль
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'pass')))
   pytest.driver.find_element(By.ID, 'pass').send_keys('qwerty123')
   # Нажимаем на кнопку входа в аккаунт
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html > body > nav > button')))
   pytest.driver.find_element(By.CSS_SELECTOR, 'html > body > nav > button').click()
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#navbarNav > ul > li > a')))
   pytest.driver.find_element(By.CSS_SELECTOR, 'div#navbarNav > ul > li > a').click()

   images = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/th/img')
   names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   descriptions = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   quantity_pets = pytest.driver.find_element(By.CSS_SELECTOR, 'html > body > div > div > div').text.split()[2]

   #проверка присутсвия всех питомцев
   assert len(names) == int(quantity_pets)
   count_img = 0
   l_names = []
   l_pets = []

   for i in range(len(names)):
      if images[i].get_attribute('src') != '':
         count_img += 1
      assert names[i].text != ''
      assert descriptions[i].text != ''
      # проверяем наличие имени, породы и возраста у каждого питомца
      parts = descriptions[i].text.split(" ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0
      assert len(parts[2]) > 0
      if len(parts[0]) > 0:
         l_names.append(parts[0])

      l_pets.append(names[i].text)

   assert len(set(l_pets)) == len(l_pets)
   #проверяем уникальность имен
   assert len(set(l_names)) == len(l_names)


   # Хотя бы у половины питомцев есть фото
   if count_img % 2 == 0:
      assert count_img >= len(names) // 2
   else:
      assert count_img > len(names) // 2