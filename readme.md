requirement.txt file should contain:
reportlab
reportlab

pip install -r requirements.txt

brew install python-tk



HOw to create dmg file:
- python setup.py py2app
- create-dmg 'dist/main.app' 'dist/YourApp.dmg'
- if encounter error: create-dmg --verbose 'dist/main.app' 'dist/YourApp.dmg'

Alternate method:
- mkdir /Users/v/PycharmProjects/invoice_generator/temp
- cp -R dist/main.app /Users/v/PycharmProjects/invoice_generator/temp/
- hdiutil create -volname "YourApp" -srcfolder /Users/v/PycharmProjects/invoice_generator/temp -ov -format UDZO /Users/v/PycharmProjects/invoice_generator/dist/YourApp.dmg
- rm -rf /Users/v/PycharmProjects/invoice_generator/temp


Make windows file:
- pip install pyinstaller
 
- pyinstaller --onefile --add-data "logo.png:." --add-data "invoice_number.json:." main.py

- pyinstaller --onefile --add-data "logo.png:." --add-data "invoice_number.json:." --icon=icon.ico main.py

-  pyinstaller --add-data="logo.png:." --add-data="invoice_number.json:." main.py







